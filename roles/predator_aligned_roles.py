from typing import Dict, List, Any, Optional
from roles.base_role import BaseRole

class Vulture(BaseRole):
    def get_role_name(self) -> str:
        return "Vulture"

    def get_role_emoji(self) -> str:
        return "🐦‍⬛"

    def get_team(self) -> str:
        return "predator_aligned"

    def get_win_condition(self) -> str:
        return "Successfully sacrifice self as ordered and Predator team wins, OR Predator team wins and Vulture survives."

    def get_role_description(self) -> str:
        return "Scavenger sided with predators. Can be ordered by Leopard/Tiger to sacrifice itself to protect or disrupt."

    def has_night_action(self) -> bool:
        return False

    async def get_night_action_prompt(self, game_manager, available_targets: List[int]) -> Optional[Dict[str, Any]]:
        return None

    async def process_night_action(self, action_data: Dict[str, Any], game_manager) -> Dict[str, Any]:
        return {}

class Crocodile(BaseRole):
    def get_role_name(self) -> str:
        return "Crocodile"

    def get_role_emoji(self) -> str:
        return "🐊"

    def get_team(self) -> str:
        return "predator_aligned"

    def get_win_condition(self) -> str:
        return "Successfully attack the Lion AND Predator team wins."

    def get_role_description(self) -> str:
        return "Ambush predator. Only animal that can injure Lion on first attack. Has two attack chances total."

    def has_night_action(self) -> bool:
        return True

    async def get_night_action_prompt(self, game_manager, available_targets: List[int]) -> Optional[Dict[str, Any]]:
        attacks_used = self.get_role_data('attacks_used', 0)
        
        if attacks_used >= 2:
            return None
        
        if not available_targets:
            return None
        
        return {
            'message': f"Crocodile, choose your target (Attack {attacks_used + 1}/2):",
            'targets': available_targets
        }

    async def process_night_action(self, action_data: Dict[str, Any], game_manager) -> Dict[str, Any]:
        target_id = action_data.get('target_id')
        attacks_used = self.get_role_data('attacks_used', 0)
        
        self.update_role_data('attacks_used', attacks_used + 1)
        
        return {
            'type': 'crocodile_attack',
            'target_id': target_id
        }
