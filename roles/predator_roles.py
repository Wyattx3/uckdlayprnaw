from typing import Dict, List, Any, Optional
from roles.base_role import BaseRole

class Leopard(BaseRole):
    def get_role_name(self) -> str:
        return "Leopard"

    def get_role_emoji(self) -> str:
        return "🐆"

    def get_team(self) -> str:
        return "predator"

    def get_win_condition(self) -> str:
        return "Predators eliminate all Villagers and hostile Neutrals until they achieve majority."

    def get_role_description(self) -> str:
        return "Leader of the Jackal pack. Fast and decisive. Chooses targets for Jackal attacks and can command the Vulture."

    def has_night_action(self) -> bool:
        return True

    async def get_night_action_prompt(self, game_manager, available_targets: List[int]) -> Optional[Dict[str, Any]]:
        if not available_targets:
            return None
        
        vulture_command_used = self.get_role_data('vulture_command_used', False)
        
        buttons = [{'text': f"🎯 Choose Kill Target", 'callback_data': f"leopard_kill_{self.game_id}"}]
        
        if not vulture_command_used:
            buttons.append({'text': f"🐦‍⬛ Command Vulture", 'callback_data': f"leopard_vulture_{self.game_id}"})
        
        return {
            'message': "Leopard, what is your command tonight?",
            'buttons': buttons
        }

    async def process_night_action(self, action_data: Dict[str, Any], game_manager) -> Dict[str, Any]:
        action_type = action_data.get('action_type')
        
        if action_type == 'kill':
            target_id = action_data.get('target_id')
            return {
                'type': 'predator_kill',
                'target_id': target_id,
                'killer_role': 'Leopard'
            }
        elif action_type == 'vulture_command':
            self.update_role_data('vulture_command_used', True)
            return {
                'type': 'vulture_command'
            }
        
        return {}

class Tiger(BaseRole):
    def get_role_name(self) -> str:
        return "Tiger"

    def get_role_emoji(self) -> str:
        return "🐅"

    def get_team(self) -> str:
        return "predator"

    def get_win_condition(self) -> str:
        return "Predators eliminate all Villagers and hostile Neutrals until they achieve majority."

    def get_role_description(self) -> str:
        return "Intelligent second-in-command. Takes over leadership if Leopard dies."

    def has_night_action(self) -> bool:
        return True

    async def get_night_action_prompt(self, game_manager, available_targets: List[int]) -> Optional[Dict[str, Any]]:
        leopard_alive = await game_manager.is_role_alive(self.game_id, 'Leopard')
        
        if leopard_alive:
            return None
        
        if not available_targets:
            return None
        
        vulture_command_used = self.get_role_data('vulture_command_used', False)
        
        buttons = [{'text': f"🎯 Choose Kill Target", 'callback_data': f"tiger_kill_{self.game_id}"}]
        
        if not vulture_command_used:
            buttons.append({'text': f"🐦‍⬛ Command Vulture", 'callback_data': f"tiger_vulture_{self.game_id}"})
        
        return {
            'message': "Tiger, the Leopard has fallen! What is your command tonight?",
            'buttons': buttons
        }

    async def process_night_action(self, action_data: Dict[str, Any], game_manager) -> Dict[str, Any]:
        action_type = action_data.get('action_type')
        
        if action_type == 'kill':
            target_id = action_data.get('target_id')
            return {
                'type': 'predator_kill',
                'target_id': target_id,
                'killer_role': 'Tiger'
            }
        elif action_type == 'vulture_command':
            self.update_role_data('vulture_command_used', True)
            return {
                'type': 'vulture_command'
            }
        
        return {}

class Jackal(BaseRole):
    def get_role_name(self) -> str:
        return "Jackal"

    def get_role_emoji(self) -> str:
        return "🐕"

    def get_team(self) -> str:
        return "predator"

    def get_win_condition(self) -> str:
        return "Predators eliminate all Villagers and hostile Neutrals until they achieve majority."

    def get_role_description(self) -> str:
        return "Pack hunter loyal to Leopard/Tiger. Carries out kill orders."

    def has_night_action(self) -> bool:
        return False

    async def get_night_action_prompt(self, game_manager, available_targets: List[int]) -> Optional[Dict[str, Any]]:
        return None

    async def process_night_action(self, action_data: Dict[str, Any], game_manager) -> Dict[str, Any]:
        return {}

class WildBoar(BaseRole):
    def get_role_name(self) -> str:
        return "Wild Boar"

    def get_role_emoji(self) -> str:
        return "🐗"

    def get_team(self) -> str:
        return "predator"

    def get_win_condition(self) -> str:
        return "Predators eliminate all Villagers and hostile Neutrals until they achieve majority."

    def get_role_description(self) -> str:
        return "Aggressive and territorial. Chooses locations to forage and can block Herbivores or attack."

    def has_night_action(self) -> bool:
        return True

    async def get_night_action_prompt(self, game_manager, available_targets: List[int]) -> Optional[Dict[str, Any]]:
        locations = ['North', 'South', 'East', 'West']
        
        return {
            'message': "Wild Boar, choose a location to forage tonight:",
            'buttons': [{'text': loc, 'callback_data': f"wildboar_{loc.lower()}_{self.game_id}"} for loc in locations]
        }

    async def process_night_action(self, action_data: Dict[str, Any], game_manager) -> Dict[str, Any]:
        location = action_data.get('location')
        
        return {
            'type': 'wild_boar_forage',
            'location': location
        }
