import asyncio
import logging
import uuid
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from database.db_manager import DatabaseManager
from database.models import User, Game, GamePlayer
from game.role_distribution import assign_roles, get_team_for_role
from game.phase_manager import PhaseManager
from game.voting_system import VotingSystem
from game.items import ItemSystem
from roles.role_factory import RoleFactory
from config import MIN_PLAYERS, MAX_PLAYERS, MAX_ROUNDS, INITIAL_DISCUSSION_TIME, DAY_DISCUSSION_TIME

logger = logging.getLogger(__name__)

class GameManager:
    def __init__(self, db_manager: DatabaseManager, bot):
        self.db_manager = db_manager
        self.bot = bot
        self.active_games = {}
        self.phase_managers = {}
        self.voting_systems = {}
        self.role_factory = RoleFactory()
        self.item_system = ItemSystem()

    async def create_game(self, chat_id: int, creator_id: int) -> Optional[str]:
        existing_game = await self.db_manager.get_active_game_by_chat(chat_id)
        if existing_game:
            return None
        
        game_id = str(uuid.uuid4())
        game = Game(
            game_id=game_id,
            chat_id=chat_id,
            creator_id=creator_id,
            current_phase='lobby',
            players=[creator_id]
        )
        
        success = await self.db_manager.create_game(game)
        if success:
            self.active_games[game_id] = game
            return game_id
        
        return None

    async def join_game(self, game_id: str, user_id: int) -> bool:
        game = await self.db_manager.get_game(game_id)
        if not game or game.current_phase != 'lobby':
            return False
        
        if user_id in game.players:
            return False
        
        if len(game.players) >= MAX_PLAYERS:
            return False
        
        game.players.append(user_id)
        success = await self.db_manager.update_game(game)
        
        if success:
            self.active_games[game_id] = game
        
        return success

    async def start_game(self, game_id: str) -> bool:
        game = await self.db_manager.get_game(game_id)
        if not game or game.current_phase != 'lobby':
            return False
        
        if len(game.players) < MIN_PLAYERS:
            return False
        
        roles = assign_roles(len(game.players))
        
        for i, player_id in enumerate(game.players):
            game_player = GamePlayer(
                game_id=game_id,
                user_id=player_id,
                role=roles[i]
            )
            await self.db_manager.create_game_player(game_player)
        
        game.current_phase = 'role_assignment'
        await self.db_manager.update_game(game)
        
        await self.send_role_assignments(game_id)
        
        await asyncio.sleep(5)
        
        game.current_phase = 'initial_discussion'
        await self.db_manager.update_game(game)
        
        await self.send_group_message(
            game.chat_id,
            f"Roles have been assigned! Check your PMs! 📨\n\nThe night is young. You have {INITIAL_DISCUSSION_TIME} seconds to talk before darkness falls. 🌙"
        )
        
        await asyncio.sleep(INITIAL_DISCUSSION_TIME)
        
        phase_manager = PhaseManager(self, game_id)
        self.phase_managers[game_id] = phase_manager
        
        await phase_manager.start_night_phase()
        
        return True

    async def send_role_assignments(self, game_id: str):
        game_players = await self.db_manager.get_game_players(game_id)
        
        for player in game_players:
            if player.role:
                role_instance = self.role_factory.create_role(player.role, player.user_id, game_id)
                
                message = f"🎭 **UC Kingdom - Role Assignment** 🎭\n\n"
                message += f"**Your Role:** {role_instance.get_role_name()} {role_instance.get_role_emoji()}\n\n"
                message += f"**Description:** {role_instance.get_role_description()}\n\n"
                message += f"**Team:** {role_instance.get_team().title()}\n\n"
                message += f"**Win Condition:** {role_instance.get_win_condition()}\n\n"
                message += "Good luck! 🍀"
                
                await self.send_pm(player.user_id, message)

    async def start_day_phase(self):
        game = await self.db_manager.get_game(self.game_id)
        if not game:
            return
        
        game.current_phase = 'day'
        await self.db_manager.update_game(game)
        
        if game.round_number >= MAX_ROUNDS:
            await self.send_group_message(
                game.chat_id,
                "The situation is dire! Some beasts still roam. If they are not found within the next two nights, the entire village will be lost! ⚠️"
            )
        
        await self.send_group_message(
            game.chat_id,
            f"Discuss the night's events. You have {DAY_DISCUSSION_TIME} seconds. 💬"
        )
        
        await asyncio.sleep(DAY_DISCUSSION_TIME)
        
        voting_system = VotingSystem(self, self.game_id)
        self.voting_systems[self.game_id] = voting_system
        
        await voting_system.start_voting_phase()

    async def check_win_condition(self) -> Optional[str]:
        game_players = await self.db_manager.get_game_players(self.game_id)
        active_players = [p for p in game_players if not p.eliminated]
        
        if not active_players:
            await self.end_game('Draw', [])
            return 'Draw'
        
        team_counts = {}
        for player in active_players:
            team = get_team_for_role(player.role)
            team_counts[team] = team_counts.get(team, 0) + 1
        
        predator_count = team_counts.get('predator', 0) + team_counts.get('predator_aligned', 0)
        villager_count = team_counts.get('villager', 0)
        neutral_count = team_counts.get('neutral', 0)
        
        if predator_count == 0:
            winners = [p.user_id for p in active_players if get_team_for_role(p.role) == 'villager']
            await self.end_game('Villagers', winners)
            return 'Villagers'
        
        if predator_count >= villager_count:
            winners = [p.user_id for p in active_players if get_team_for_role(p.role) in ['predator', 'predator_aligned']]
            await self.end_game('Predators', winners)
            return 'Predators'
        
        game = await self.db_manager.get_game(self.game_id)
        if game and game.round_number >= MAX_ROUNDS:
            winners = [p.user_id for p in active_players if get_team_for_role(p.role) in ['predator', 'predator_aligned']]
            await self.end_game('Predators', winners)
            return 'Predators'
        
        if game:
            phase_manager = self.phase_managers.get(self.game_id)
            if phase_manager:
                await phase_manager.start_night_phase()
        
        return None

    async def end_game(self, winning_team: str, winners: List[int]):
        game = await self.db_manager.get_game(self.game_id)
        if not game:
            return
        
        game.current_phase = 'finished'
        await self.db_manager.update_game(game)
        
        game_players = await self.db_manager.get_game_players(self.game_id)
        
        message = ""
        if winning_team == 'Villagers':
            message = "The last predator has been vanquished! The village is safe once more! 🎉\n\n"
            message += "**Survivors:**\n"
            for player in game_players:
                if not player.eliminated and get_team_for_role(player.role) == 'villager':
                    player_ign = await self.get_player_ign(player.user_id)
                    role_instance = self.role_factory.create_role(player.role, player.user_id, self.game_id)
                    message += f"{role_instance.get_role_emoji()} {player_ign} ({role_instance.get_role_name()})\n"
        
        elif winning_team == 'Predators':
            message = "The predators have overwhelmed the village! Darkness reigns... 👑\n\n"
            message += "**Victorious Predators:**\n"
            for player in game_players:
                if not player.eliminated and get_team_for_role(player.role) in ['predator', 'predator_aligned']:
                    player_ign = await self.get_player_ign(player.user_id)
                    role_instance = self.role_factory.create_role(player.role, player.user_id, self.game_id)
                    message += f"{role_instance.get_role_emoji()} {player_ign} ({role_instance.get_role_name()})\n"
        
        elif winning_team == 'Fox':
            message = "The Fox has achieved its cunning victory! 🦊\n\n"
            for winner_id in winners:
                player_ign = await self.get_player_ign(winner_id)
                message += f"🦊 {player_ign} (Fox) - Master of Deception!\n"
        
        await self.send_group_message(game.chat_id, message)
        
        await self.calculate_performance_and_rewards(winning_team, winners)
        
        await self.cleanup_game()

    async def calculate_performance_and_rewards(self, winning_team: str, winners: List[int]):
        game_players = await self.db_manager.get_game_players(self.game_id)
        
        performance_message = "\n--- **Performance** ---\n"
        if winning_team == 'Villagers':
            performance_message += "Peace has returned to the village:\n"
        elif winning_team == 'Predators':
            performance_message += "The village has fallen to darkness:\n"
        else:
            performance_message += "A cunning victory:\n"
        
        for player in game_players:
            user = await self.db_manager.get_user(player.user_id)
            if not user:
                continue
            
            player_ign = user.ign
            role_instance = self.role_factory.create_role(player.role, player.user_id, self.game_id)
            
            stars = 1
            bricks_earned = 0
            
            if player.user_id in winners:
                stars = 3
                user.games_won += 1
                user.rank_stars += 1
            else:
                stars = 1
                if user.rank_stars > 1:
                    user.rank_stars -= 1
            
            bricks_earned = stars * 10
            user.bricks += bricks_earned
            user.games_played += 1
            
            await self.db_manager.update_user(user)
            
            star_display = "✨" * stars
            performance_message += f"{role_instance.get_role_emoji()} {player_ign} {star_display} (Bricks: +{bricks_earned})\n"
        
        game = await self.db_manager.get_game(self.game_id)
        if game:
            await self.send_group_message(game.chat_id, performance_message)

    async def cleanup_game(self):
        await self.db_manager.delete_game_players(self.game_id)
        await self.db_manager.delete_game(self.game_id)
        
        self.active_games.pop(self.game_id, None)
        self.phase_managers.pop(self.game_id, None)
        self.voting_systems.pop(self.game_id, None)

    async def get_player_ign(self, user_id: int) -> str:
        user = await self.db_manager.get_user(user_id)
        return user.ign if user else f"User{user_id}"

    async def is_role_alive(self, role_name: str) -> bool:
        game_players = await self.db_manager.get_game_players(self.game_id)
        for player in game_players:
            if player.role == role_name and not player.eliminated:
                return True
        return False

    async def send_pm(self, user_id: int, message: str):
        try:
            await self.bot.send_message(chat_id=user_id, text=message, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Failed to send PM to {user_id}: {e}")

    async def send_pm_with_buttons(self, user_id: int, message: str, buttons: List[Dict[str, str]]):
        try:
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup
            
            keyboard = []
            for button in buttons:
                keyboard.append([InlineKeyboardButton(button['text'], callback_data=button['callback_data'])])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await self.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Failed to send PM with buttons to {user_id}: {e}")

    async def send_group_message(self, chat_id: int, message: str):
        try:
            await self.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Failed to send group message to {chat_id}: {e}")

    async def send_group_message_with_buttons(self, chat_id: int, message: str, buttons: List[Dict[str, str]]):
        try:
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup
            
            keyboard = []
            for button in buttons:
                keyboard.append([InlineKeyboardButton(button['text'], callback_data=button['callback_data'])])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await self.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Failed to send group message with buttons to {chat_id}: {e}")
