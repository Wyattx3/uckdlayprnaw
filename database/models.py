import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class User:
    def __init__(self, telegram_id: int, ign: str, rank_stars: int = 1, bricks: int = 0, 
                 items: List[str] = None, games_played: int = 0, games_won: int = 0, 
                 joined_date: str = None, last_ign_change: str = None):
        self.telegram_id = telegram_id
        self.ign = ign
        self.rank_stars = rank_stars
        self.bricks = bricks
        self.items = items or []
        self.games_played = games_played
        self.games_won = games_won
        self.joined_date = joined_date or datetime.now().strftime('%d/%m/%Y')
        self.last_ign_change = last_ign_change

    def to_dict(self) -> Dict[str, Any]:
        return {
            'telegram_id': self.telegram_id,
            'ign': self.ign,
            'rank_stars': self.rank_stars,
            'bricks': self.bricks,
            'items': json.dumps(self.items),
            'games_played': self.games_played,
            'games_won': self.games_won,
            'joined_date': self.joined_date,
            'last_ign_change': self.last_ign_change
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        items = json.loads(data.get('items', '[]')) if isinstance(data.get('items'), str) else data.get('items', [])
        return cls(
            telegram_id=data['telegram_id'],
            ign=data['ign'],
            rank_stars=data.get('rank_stars', 1),
            bricks=data.get('bricks', 0),
            items=items,
            games_played=data.get('games_played', 0),
            games_won=data.get('games_won', 0),
            joined_date=data.get('joined_date'),
            last_ign_change=data.get('last_ign_change')
        )

    def get_win_rate(self) -> float:
        if self.games_played == 0:
            return 0.0
        return (self.games_won / self.games_played) * 100

    def get_rank_info(self) -> Dict[str, Any]:
        from config import RANKS
        
        total_stars = self.rank_stars
        rank_index = 0
        stars_used = 0
        
        for i, rank in enumerate(RANKS):
            if total_stars > stars_used + rank['max_stars']:
                stars_used += rank['max_stars']
                continue
            else:
                rank_index = i
                current_stars = total_stars - stars_used
                break
        else:
            rank_index = len(RANKS) - 1
            current_stars = min(total_stars - stars_used, RANKS[rank_index]['max_stars'])
        
        return {
            'rank': RANKS[rank_index],
            'current_stars': current_stars,
            'rank_index': rank_index
        }
    
    def add_performance_stars(self, stars: int):
        """Add performance stars to user's total"""
        self.rank_stars += stars
    
    def subtract_performance_stars(self, stars: int):
        """Subtract performance stars from user's total"""
        self.rank_stars = max(0, self.rank_stars - stars)
    
    def calculate_brick_reward(self, performance_stars: int) -> int:
        """Calculate brick reward based on performance stars (1 star = 10 bricks)"""
        return performance_stars * 10

class Game:
    def __init__(self, game_id: str, chat_id: int, creator_id: int, current_phase: str = 'lobby',
                 players: List[int] = None, eliminated_players: List[int] = None,
                 game_data: Dict[str, Any] = None, round_number: int = 1, created_at: str = None):
        self.game_id = game_id
        self.chat_id = chat_id
        self.creator_id = creator_id
        self.current_phase = current_phase
        self.players = players or []
        self.eliminated_players = eliminated_players or []
        self.game_data = game_data or {}
        self.round_number = round_number
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'game_id': self.game_id,
            'chat_id': self.chat_id,
            'creator_id': self.creator_id,
            'current_phase': self.current_phase,
            'players': json.dumps(self.players),
            'eliminated_players': json.dumps(self.eliminated_players),
            'game_data': json.dumps(self.game_data),
            'round_number': self.round_number,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Game':
        players = json.loads(data.get('players', '[]')) if isinstance(data.get('players'), str) else data.get('players', [])
        eliminated_players = json.loads(data.get('eliminated_players', '[]')) if isinstance(data.get('eliminated_players'), str) else data.get('eliminated_players', [])
        game_data = json.loads(data.get('game_data', '{}')) if isinstance(data.get('game_data'), str) else data.get('game_data', {})
        
        return cls(
            game_id=data['game_id'],
            chat_id=data['chat_id'],
            creator_id=data['creator_id'],
            current_phase=data.get('current_phase', 'lobby'),
            players=players,
            eliminated_players=eliminated_players,
            game_data=game_data,
            round_number=data.get('round_number', 1),
            created_at=data.get('created_at')
        )

class GamePlayer:
    def __init__(self, game_id: str, user_id: int, role: str = None, role_data: Dict[str, Any] = None,
                 eliminated: bool = False, night_actions: Dict[str, Any] = None, votes: Dict[str, Any] = None,
                 performance_stars: int = 0, equipped_item: str = None):
        self.game_id = game_id
        self.user_id = user_id
        self.role = role
        self.role_data = role_data or {}
        self.eliminated = eliminated
        self.night_actions = night_actions or {}
        self.votes = votes or {}
        self.performance_stars = performance_stars
        self.equipped_item = equipped_item

    def to_dict(self) -> Dict[str, Any]:
        return {
            'game_id': self.game_id,
            'user_id': self.user_id,
            'role': self.role,
            'role_data': json.dumps(self.role_data),
            'eliminated': self.eliminated,
            'night_actions': json.dumps(self.night_actions),
            'votes': json.dumps(self.votes),
            'performance_stars': self.performance_stars,
            'equipped_item': self.equipped_item
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GamePlayer':
        role_data = json.loads(data.get('role_data', '{}')) if isinstance(data.get('role_data'), str) else data.get('role_data', {})
        night_actions = json.loads(data.get('night_actions', '{}')) if isinstance(data.get('night_actions'), str) else data.get('night_actions', {})
        votes = json.loads(data.get('votes', '{}')) if isinstance(data.get('votes'), str) else data.get('votes', {})
        
        return cls(
            game_id=data['game_id'],
            user_id=data['user_id'],
            role=data.get('role'),
            role_data=role_data,
            eliminated=data.get('eliminated', False),
            night_actions=night_actions,
            votes=votes,
            performance_stars=data.get('performance_stars', 0),
            equipped_item=data.get('equipped_item')
        )
