import random
from typing import List, Dict, Any

def generate_game_id() -> str:
    import uuid
    return str(uuid.uuid4())

def shuffle_players(players: List[int]) -> List[int]:
    shuffled = players.copy()
    random.shuffle(shuffled)
    return shuffled

def format_player_list(players: List[str]) -> str:
    return "\n".join([f"• {name}" for name in players])

def calculate_team_balance(roles: List[str]) -> Dict[str, int]:
    from game.role_distribution import get_team_for_role
    
    team_counts = {}
    for role in roles:
        team = get_team_for_role(role)
        team_counts[team] = team_counts.get(team, 0) + 1
    
    return team_counts

def format_time_remaining(seconds: int) -> str:
    if seconds >= 60:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds}s"
    else:
        return f"{seconds}s"

def get_random_elimination_message() -> str:
    messages = [
        "The village council has made their decision...",
        "After much deliberation, the verdict is...",
        "The votes have been counted...",
        "Justice will be served...",
        "The accused stands before the village..."
    ]
    return random.choice(messages)

def format_vote_results(vote_counts: Dict[int, int], get_player_name_func) -> str:
    message = "📊 **Voting Results** ⚖️\n\n"
    
    sorted_votes = sorted(vote_counts.items(), key=lambda x: x[1], reverse=True)
    
    for player_id, votes in sorted_votes:
        player_name = get_player_name_func(player_id)
        vote_emoji = "📨 " + "(*)" * votes
        message += f"{player_name} received {vote_emoji} vote{'s' if votes != 1 else ''}.\n"
    
    return message

def get_location_emoji(location: str) -> str:
    location_emojis = {
        'north': '🏔️',
        'south': '🏞️',
        'east': '🕳️',
        'west': '🏞️'
    }
    return location_emojis.get(location.lower(), '📍')
