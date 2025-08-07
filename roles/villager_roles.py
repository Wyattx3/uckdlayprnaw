from typing import Dict, List, Any, Optional
from roles.base_role import BaseRole
import random

class Lion(BaseRole):
    def get_role_name(self) -> str:
        return "Lion"

    def get_role_emoji(self) -> str:
        return "🦁"

    def get_team(self) -> str:
        return "villager"

    def get_win_condition(self) -> str:
        return "Eliminate all Predators and hostile Neutrals, and survive."

    def get_role_description(self) -> str:
        return "Leader of the good animals. Immune to first predator attack each night (except from Crocodile or Hunter). If attacked by Crocodile, gets injured and vulnerable to subsequent attacks."

    def has_night_action(self) -> bool:
        return False

    async def get_night_action_prompt(self, game_manager, available_targets: List[int]) -> Optional[Dict[str, Any]]:
        return None

    async def process_night_action(self, action_data: Dict[str, Any], game_manager) -> Dict[str, Any]:
        return {}

class Hunter(BaseRole):
    def get_role_name(self) -> str:
        return "Hunter"

    def get_role_emoji(self) -> str:
        return "🏹"

    def get_team(self) -> str:
        return "villager"

    def get_win_condition(self) -> str:
        return "Eliminate all Predators and hostile Neutrals, and survive."

    def get_role_description(self) -> str:
        return "The last uninfected human. Can investigate or kill one player each night."

    def has_night_action(self) -> bool:
        return True

    async def get_night_action_prompt(self, game_manager, available_targets: List[int]) -> Optional[Dict[str, Any]]:
        if not available_targets:
            return None
        
        return {
            'message': "Hunter, choose your action:",
            'buttons': [
                {'text': f"🔍 Investigate", 'callback_data': f"hunter_investigate_{self.game_id}"},
                {'text': f"🏹 Kill", 'callback_data': f"hunter_kill_{self.game_id}"}
            ]
        }

    async def process_night_action(self, action_data: Dict[str, Any], game_manager) -> Dict[str, Any]:
        action_type = action_data.get('action_type')
        target_id = action_data.get('target_id')
        
        if action_type == 'investigate':
            target_player = await game_manager.db_manager.get_game_player(self.game_id, target_id)
            if target_player and target_player.role:
                role_instance = game_manager.role_factory.create_role(target_player.role, target_id, self.game_id)
                return {
                    'type': 'investigation',
                    'result': f"You scouted {await game_manager.get_player_ign(target_id)}. They are a {role_instance.get_role_name()}."
                }
        elif action_type == 'kill':
            return {
                'type': 'kill',
                'target_id': target_id,
                'killer_role': 'Hunter'
            }
        
        return {}

class Owl(BaseRole):
    def get_role_name(self) -> str:
        return "Owl"

    def get_role_emoji(self) -> str:
        return "🦉"

    def get_team(self) -> str:
        return "villager"

    def get_win_condition(self) -> str:
        return "Eliminate all Predators and hostile Neutrals, and survive."

    def get_role_description(self) -> str:
        return "Wise nocturnal healer. Can heal/protect one player each night. Cannot heal the same player two nights in a row. Can heal itself once per game."

    def has_night_action(self) -> bool:
        return True

    async def get_night_action_prompt(self, game_manager, available_targets: List[int]) -> Optional[Dict[str, Any]]:
        last_healed = self.get_role_data('last_healed')
        self_healed = self.get_role_data('self_healed', False)
        
        valid_targets = []
        for target_id in available_targets:
            if target_id != last_healed:
                valid_targets.append(target_id)
        
        if not self_healed:
            valid_targets.append(self.player_id)
        
        if not valid_targets:
            return None
        
        return {
            'message': "Owl, choose who to heal tonight:",
            'targets': valid_targets
        }

    async def process_night_action(self, action_data: Dict[str, Any], game_manager) -> Dict[str, Any]:
        target_id = action_data.get('target_id')
        
        if target_id == self.player_id:
            self.update_role_data('self_healed', True)
        
        self.update_role_data('last_healed', target_id)
        
        return {
            'type': 'heal',
            'target_id': target_id
        }

class Turtle(BaseRole):
    def get_role_name(self) -> str:
        return "Turtle"

    def get_role_emoji(self) -> str:
        return "🐢"

    def get_team(self) -> str:
        return "villager"

    def get_win_condition(self) -> str:
        return "Eliminate all Predators and hostile Neutrals, and survive."

    def get_role_description(self) -> str:
        return "Slow and defensive. Survives the first attack due to hard shell, but becomes vulnerable after shell cracks."

    def has_night_action(self) -> bool:
        return False

    async def get_night_action_prompt(self, game_manager, available_targets: List[int]) -> Optional[Dict[str, Any]]:
        return None

    async def process_night_action(self, action_data: Dict[str, Any], game_manager) -> Dict[str, Any]:
        return {}

class Monkey(BaseRole):
    def get_role_name(self) -> str:
        return "Monkey"

    def get_role_emoji(self) -> str:
        return "🐒"

    def get_team(self) -> str:
        return "villager"

    def get_win_condition(self) -> str:
        return "Eliminate all Predators and hostile Neutrals, and survive."

    def get_role_description(self) -> str:
        return "Intelligent and talkative. Can role-block one player each night by engaging them in conversation."

    def has_night_action(self) -> bool:
        return True

    async def get_night_action_prompt(self, game_manager, available_targets: List[int]) -> Optional[Dict[str, Any]]:
        if not available_targets:
            return None
        
        return {
            'message': "Monkey, choose who to engage in conversation tonight:",
            'targets': available_targets
        }

    async def process_night_action(self, action_data: Dict[str, Any], game_manager) -> Dict[str, Any]:
        target_id = action_data.get('target_id')
        
        return {
            'type': 'role_block',
            'target_id': target_id
        }

class Bat(BaseRole):
    def get_role_name(self) -> str:
        return "Bat"

    def get_role_emoji(self) -> str:
        return "🦇"

    def get_team(self) -> str:
        return "villager"

    def get_win_condition(self) -> str:
        return "Eliminate all Predators and hostile Neutrals, and survive."

    def get_role_description(self) -> str:
        return "Uses echolocation. If attacked, identifies the attacker but loses cave and dies next night."

    def has_night_action(self) -> bool:
        return False

    async def get_night_action_prompt(self, game_manager, available_targets: List[int]) -> Optional[Dict[str, Any]]:
        return None

    async def process_night_action(self, action_data: Dict[str, Any], game_manager) -> Dict[str, Any]:
        return {}

class Hedgehog(BaseRole):
    def get_role_name(self) -> str:
        return "Hedgehog"

    def get_role_emoji(self) -> str:
        return "🦔"

    def get_team(self) -> str:
        return "villager"

    def get_win_condition(self) -> str:
        return "Eliminate all Predators and hostile Neutrals, and survive."

    def get_role_description(self) -> str:
        return "Spiny and dangerous. If attacked at night, the attacker dies along with the Hedgehog."

    def has_night_action(self) -> bool:
        return False

    async def get_night_action_prompt(self, game_manager, available_targets: List[int]) -> Optional[Dict[str, Any]]:
        return None

    async def process_night_action(self, action_data: Dict[str, Any], game_manager) -> Dict[str, Any]:
        return {}

class Herbivore(BaseRole):
    def __init__(self, player_id: int, game_id: str, animal_type: str):
        super().__init__(player_id, game_id)
        self.animal_type = animal_type

    def get_team(self) -> str:
        return "villager"

    def get_win_condition(self) -> str:
        return "Eliminate all Predators and hostile Neutrals, and survive."

    def get_role_description(self) -> str:
        return f"Grazer and cautious. Can visit locations each night and witness incidents. Cannot visit South Stream twice."

    def has_night_action(self) -> bool:
        return True

    async def get_night_action_prompt(self, game_manager, available_targets: List[int]) -> Optional[Dict[str, Any]]:
        south_visits = self.get_role_data('south_visits', 0)
        
        locations = ['North', 'East', 'West']
        if south_visits < 1:
            locations.append('South')
        
        return {
            'message': f"{self.animal_type}, choose a location to visit tonight:",
            'buttons': [{'text': loc, 'callback_data': f"herbivore_{loc.lower()}_{self.game_id}"} for loc in locations]
        }

    async def process_night_action(self, action_data: Dict[str, Any], game_manager) -> Dict[str, Any]:
        location = action_data.get('location')
        
        if location == 'south':
            south_visits = self.get_role_data('south_visits', 0)
            self.update_role_data('south_visits', south_visits + 1)
        
        return {
            'type': 'visit_location',
            'location': location
        }

class Deer(Herbivore):
    def __init__(self, player_id: int, game_id: str):
        super().__init__(player_id, game_id, "Deer")

    def get_role_name(self) -> str:
        return "Deer"

    def get_role_emoji(self) -> str:
        return "🦌"

class Giraffe(Herbivore):
    def __init__(self, player_id: int, game_id: str):
        super().__init__(player_id, game_id, "Giraffe")

    def get_role_name(self) -> str:
        return "Giraffe"

    def get_role_emoji(self) -> str:
        return "🦒"

class Buffalo(Herbivore):
    def __init__(self, player_id: int, game_id: str):
        super().__init__(player_id, game_id, "Buffalo")

    def get_role_name(self) -> str:
        return "Buffalo"

    def get_role_emoji(self) -> str:
        return "🐃"

class Cow(Herbivore):
    def __init__(self, player_id: int, game_id: str):
        super().__init__(player_id, game_id, "Cow")

    def get_role_name(self) -> str:
        return "Cow"

    def get_role_emoji(self) -> str:
        return "🐄"

class Sheep(Herbivore):
    def __init__(self, player_id: int, game_id: str):
        super().__init__(player_id, game_id, "Sheep")

    def get_role_name(self) -> str:
        return "Sheep"

    def get_role_emoji(self) -> str:
        return "🐑"
