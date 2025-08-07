import random
from typing import List
from config import ROLE_DISTRIBUTIONS

def assign_roles(player_count: int) -> List[str]:
    if player_count < 7 or player_count > 20:
        raise ValueError(f"Invalid player count: {player_count}. Must be between 7 and 20.")
    
    if player_count not in ROLE_DISTRIBUTIONS:
        raise ValueError(f"No role distribution defined for {player_count} players.")
    
    roles = ROLE_DISTRIBUTIONS[player_count].copy()
    random.shuffle(roles)
    return roles

def get_team_for_role(role_name: str) -> str:
    villager_roles = ['Lion', 'Hunter', 'Owl', 'Turtle', 'Monkey', 'Bat', 'Hedgehog', 
                     'Deer', 'Giraffe', 'Buffalo', 'Cow', 'Sheep']
    predator_roles = ['Leopard', 'Tiger', 'Jackal', 'Wild Boar']
    predator_aligned_roles = ['Vulture', 'Crocodile']
    neutral_roles = ['Fox']
    
    if role_name in villager_roles:
        return 'villager'
    elif role_name in predator_roles:
        return 'predator'
    elif role_name in predator_aligned_roles:
        return 'predator_aligned'
    elif role_name in neutral_roles:
        return 'neutral'
    else:
        return 'unknown'

def get_predator_roles() -> List[str]:
    return ['Leopard', 'Tiger', 'Jackal', 'Wild Boar']

def get_villager_roles() -> List[str]:
    return ['Lion', 'Hunter', 'Owl', 'Turtle', 'Monkey', 'Bat', 'Hedgehog', 
            'Deer', 'Giraffe', 'Buffalo', 'Cow', 'Sheep']

def get_neutral_roles() -> List[str]:
    return ['Fox']

def get_predator_aligned_roles() -> List[str]:
    return ['Vulture', 'Crocodile']
