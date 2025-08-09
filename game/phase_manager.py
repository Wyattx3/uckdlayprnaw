import asyncio
import logging
from typing import Dict, List, Any, Optional
from database.models import GamePlayer
from roles.role_factory import RoleFactory

logger = logging.getLogger(__name__)

class PhaseManager:
    def __init__(self, game_manager, game_id: str):
        self.game_manager = game_manager
        self.game_id = game_id
        self.role_factory = RoleFactory()
        self.night_actions = {}
        self.pending_actions = set()

    async def start_night_phase(self):
        game = await self.game_manager.db_manager.get_game(self.game_id)
        if not game:
            return
        
        game.current_phase = 'night'
        await self.game_manager.db_manager.update_game(game)
        
        await self.game_manager.send_group_message(
            game.chat_id,
            "Night falls... 🌃 All villagers seek shelter. Those with night duties, check your PMs for instructions."
        )
        
        await self.collect_night_actions()

    async def collect_night_actions(self):
        game_players = await self.game_manager.db_manager.get_game_players(self.game_id)
        active_players = [p for p in game_players if not p.eliminated]
        
        for player in active_players:
            if player.role:
                role_instance = self.role_factory.create_role(player.role, player.user_id, self.game_id)
                
                if role_instance.has_night_action():
                    available_targets = [p.user_id for p in active_players if p.user_id != player.user_id]
                    action_prompt = await role_instance.get_night_action_prompt(self.game_manager, available_targets)
                    
                    if action_prompt:
                        self.pending_actions.add(player.user_id)
                        await self.send_night_action_prompt(player.user_id, role_instance, action_prompt)

        if not self.pending_actions:
            await self.resolve_night_phase()

    async def send_night_action_prompt(self, player_id: int, role_instance, action_prompt: Dict[str, Any]):
        message = f"It's your turn, {role_instance.get_role_name()} {role_instance.get_role_emoji()}.\n\n{action_prompt['message']}"
        
        if 'buttons' in action_prompt:
            await self.game_manager.send_pm_with_buttons(player_id, message, action_prompt['buttons'])
        elif 'targets' in action_prompt:
            buttons = []
            for target_id in action_prompt['targets']:
                target_ign = await self.game_manager.get_player_ign(target_id)
                if target_id == player_id:
                    target_ign = "Yourself"
                buttons.append({
                    'text': target_ign,
                    'callback_data': f"night_target_{target_id}_{self.game_id}"
                })
            await self.game_manager.send_pm_with_buttons(player_id, message, buttons)

    async def handle_night_action(self, player_id: int, action_data: Dict[str, Any]):
        if player_id not in self.pending_actions:
            return False
        
        game_player = await self.game_manager.db_manager.get_game_player(self.game_id, player_id)
        if not game_player or not game_player.role:
            return False
        
        role_instance = self.role_factory.create_role(game_player.role, player_id, self.game_id)
        
        processed_action = await role_instance.process_night_action(action_data, self.game_manager)
        
        if processed_action:
            self.night_actions[player_id] = processed_action
            self.pending_actions.discard(player_id)
            
            await self.game_manager.send_pm(player_id, "Your action has been recorded. ✅")
            
            if not self.pending_actions:
                await self.resolve_night_phase()
            
            return True
        
        return False

    async def resolve_night_phase(self):
        logger.info(f"Resolving night phase for game {self.game_id}")
        
        deaths = []
        notifications = []
        
        kills = [action for action in self.night_actions.values() if action.get('type') == 'kill' or action.get('type') == 'predator_kill' or action.get('type') == 'crocodile_attack']
        heals = [action for action in self.night_actions.values() if action.get('type') == 'heal']
        role_blocks = [action for action in self.night_actions.values() if action.get('type') == 'role_block']
        
        healed_players = {heal['target_id'] for heal in heals}
        blocked_players = {block['target_id'] for block in role_blocks}
        
        for kill_action in kills:
            target_id = kill_action.get('target_id')
            if not target_id:
                continue
            
            target_player = await self.game_manager.db_manager.get_game_player(self.game_id, target_id)
            if not target_player or target_player.eliminated:
                continue
            
            target_role_instance = self.role_factory.create_role(target_player.role, target_id, self.game_id)
            
            if target_id in healed_players:
                target_ign = await self.game_manager.get_player_ign(target_id)
                notifications.append(f"{target_ign} was attacked but saved by the Owl! 🦉")
                continue
            
            if target_player.role == 'Turtle':
                shell_cracked = target_player.role_data.get('shell_cracked', False)
                if not shell_cracked:
                    target_player.role_data['shell_cracked'] = True
                    await self.game_manager.db_manager.update_game_player(target_player)
                    target_ign = await self.game_manager.get_player_ign(target_id)
                    notifications.append(f"A loud crack was heard from the West Lake! {target_ign} (The Turtle) was attacked, but its shell held! It won't be so lucky next time. 🐢")
                    continue
            
            if target_player.role == 'Lion':
                injured = target_player.role_data.get('injured', False)
                killer_role = kill_action.get('killer_role', '')
                
                if not injured and killer_role not in ['Crocodile', 'Hunter']:
                    target_player.role_data['injured'] = True
                    await self.game_manager.db_manager.update_game_player(target_player)
                    target_ign = await self.game_manager.get_player_ign(target_id)
                    notifications.append(f"The Lion was targeted but its mighty roar scared off the attacker! 🦁")
                    continue
                elif killer_role == 'Crocodile':
                    target_player.role_data['injured'] = True
                    await self.game_manager.db_manager.update_game_player(target_player)
                    target_ign = await self.game_manager.get_player_ign(target_id)
                    notifications.append(f"The Crocodile ambushed the Lion! The Lion is now injured. 🐊")
                    continue
            
            if target_player.role == 'Hedgehog':
                killer_id = None
                for player_id, action in self.night_actions.items():
                    if action == kill_action:
                        killer_id = player_id
                        break
                
                if killer_id:
                    killer_player = await self.game_manager.db_manager.get_game_player(self.game_id, killer_id)
                    if killer_player:
                        killer_player.eliminated = True
                        await self.game_manager.db_manager.update_game_player(killer_player)
                        
                        killer_ign = await self.game_manager.get_player_ign(killer_id)
                        target_ign = await self.game_manager.get_player_ign(target_id)
                        deaths.append((target_id, target_player.role))
                        deaths.append((killer_id, killer_player.role))
                        notifications.append(f"{target_ign} (The Hedgehog 🦔) was attacked by {killer_ign}! The attacker also died from the Hedgehog's sharp quills!")
                        continue
            
            if target_player.role == 'Bat':
                killer_id = None
                for player_id, action in self.night_actions.items():
                    if action == kill_action:
                        killer_id = player_id
                        break
                
                if killer_id:
                    killer_ign = await self.game_manager.get_player_ign(killer_id)
                    target_player.role_data['attacker_identified'] = killer_ign
                    target_player.role_data['homeless'] = True
                    await self.game_manager.db_manager.update_game_player(target_player)
                    
                    await self.game_manager.send_pm(
                        target_id,
                        f"You were attacked in your cave! Using your senses, you identified {killer_ign} as they fled. However, your cave is destroyed. You have nowhere to go..."
                    )
                    continue
            
            target_player.eliminated = True
            await self.game_manager.db_manager.update_game_player(target_player)
            deaths.append((target_id, target_player.role))

        game = await self.game_manager.db_manager.get_game(self.game_id)
        game.current_phase = 'day'
        game.round_number += 1
        await self.game_manager.db_manager.update_game(game)
        
        await self.announce_night_results(deaths, notifications)
        
        self.night_actions.clear()
        self.pending_actions.clear()
        
        await self.game_manager.start_day_phase(self.game_id)

    async def announce_night_results(self, deaths: List[tuple], notifications: List[str]):
        game = await self.game_manager.db_manager.get_game(self.game_id)
        if not game:
            return
        
        message = "The sun rises... ☀️ Let's see who survived the night.\n\n"
        
        if deaths:
            for death in deaths:
                player_id, role = death
                player_ign = await self.game_manager.get_player_ign(player_id)
                role_instance = self.role_factory.create_role(role, player_id, self.game_id)
                message += f"{player_ign} ({role_instance.get_role_name()} {role_instance.get_role_emoji()}) was found dead.\n"
        else:
            message += "No one died during the night. 🌅\n"
        
        if notifications:
            message += "\n" + "\n".join(notifications)
        
        await self.game_manager.send_group_message(game.chat_id, message)
