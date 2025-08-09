import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter

logger = logging.getLogger(__name__)

class VotingSystem:
    def __init__(self, game_manager, game_id: str):
        self.game_manager = game_manager
        self.game_id = game_id
        self.votes = {}
        self.voters = set()

    async def start_voting_phase(self):
        game = await self.game_manager.db_manager.get_game(self.game_id)
        if not game:
            return
        
        game.current_phase = 'voting'
        await self.game_manager.db_manager.update_game(game)
        
        game_players = await self.game_manager.db_manager.get_game_players(self.game_id)
        active_players = [p for p in game_players if not p.eliminated]
        
        if len(active_players) <= 1:
            await self.game_manager.check_win_condition(self.game_id)
            return
        
        message = "Time to vote! Who is suspicious? You have 15 seconds. ⚖️\n\n"
        
        buttons = []
        for player in active_players:
            player_ign = await self.game_manager.get_player_ign(player.user_id)
            buttons.append({
                'text': f"Vote for {player_ign}",
                'callback_data': f"vote_{player.user_id}_{self.game_id}"
            })
        
        await self.game_manager.send_group_message_with_buttons(game.chat_id, message, buttons)
        
        await asyncio.sleep(15)
        await self.resolve_voting()

    async def cast_vote(self, voter_id: int, target_id: int) -> bool:
        game_player = await self.game_manager.db_manager.get_game_player(self.game_id, voter_id)
        if not game_player or game_player.eliminated:
            return False
        
        if voter_id in self.voters:
            return False
        
        target_player = await self.game_manager.db_manager.get_game_player(self.game_id, target_id)
        if not target_player or target_player.eliminated:
            return False
        
        self.votes[target_id] = self.votes.get(target_id, 0) + 1
        self.voters.add(voter_id)
        
        voter_ign = await self.game_manager.get_player_ign(voter_id)
        target_ign = await self.game_manager.get_player_ign(target_id)
        
        await self.game_manager.send_pm(voter_id, f"You voted for {target_ign}. ✅")
        
        return True

    async def resolve_voting(self):
        game = await self.game_manager.db_manager.get_game(self.game_id)
        if not game:
            return
        
        if not self.votes:
            await self.game_manager.send_group_message(
                game.chat_id,
                "No votes were cast. The village remains divided. 🤷‍♂️"
            )
            await self.game_manager.check_win_condition(self.game_id)
            return
        
        vote_counts = Counter(self.votes)
        max_votes = max(vote_counts.values())
        tied_players = [player_id for player_id, votes in vote_counts.items() if votes == max_votes]
        
        message = "Voting has ended.\n\n"
        message += "📊 **First Day's Council** ⚖️\n\n"
        
        for player_id, vote_count in vote_counts.most_common():
            player_ign = await self.game_manager.get_player_ign(player_id)
            vote_emoji = "📨 " + "(*)" * vote_count
            message += f"{player_ign} received {vote_emoji} vote{'s' if vote_count != 1 else ''}.\n"
        
        if len(tied_players) > 1:
            eliminated_player_id = tied_players[0]
        else:
            eliminated_player_id = tied_players[0]
        
        eliminated_player = await self.game_manager.db_manager.get_game_player(self.game_id, eliminated_player_id)
        if eliminated_player:
            eliminated_player.eliminated = True
            await self.game_manager.db_manager.update_game_player(eliminated_player)
            
            eliminated_ign = await self.game_manager.get_player_ign(eliminated_player_id)
            role_instance = self.game_manager.role_factory.create_role(eliminated_player.role, eliminated_player_id, self.game_id)
            
            message += f"\n{eliminated_ign} is being banished from the village! Their role was... The {role_instance.get_role_name()} {role_instance.get_role_emoji()}!\n"
            
            if eliminated_player.role == 'Fox':
                message += f"\nThe village decided to eliminate {eliminated_ign}... It was the Fox! 🦊 Deceived until the end, the Fox wins its cunning game!"
                await self.game_manager.end_game(self.game_id, 'Fox', [eliminated_player_id])
                return
        
        await self.game_manager.send_group_message(game.chat_id, message)
        
        self.votes.clear()
        self.voters.clear()
        
        await self.game_manager.check_win_condition(self.game_id)

    def get_vote_count(self, player_id: int) -> int:
        return self.votes.get(player_id, 0)

    def has_voted(self, voter_id: int) -> bool:
        return voter_id in self.voters

    def get_all_votes(self) -> Dict[int, int]:
        return self.votes.copy()
