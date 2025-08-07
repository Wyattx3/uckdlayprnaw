from typing import Dict, List, Any, Optional
from roles.base_role import BaseRole

class Fox(BaseRole):
    def get_role_name(self) -> str:
        return "Fox"

    def get_role_emoji(self) -> str:
        return "🦊"

    def get_team(self) -> str:
        return "neutral"

    def get_win_condition(self) -> str:
        return "Get eliminated (voted out or killed) by players who believe the Fox is a Predator."

    def get_role_description(self) -> str:
        return "Cunning and deceptive. Wants to be misjudged. Appears suspicious to investigations."

    def has_night_action(self) -> bool:
        return False

    async def get_night_action_prompt(self, game_manager, available_targets: List[int]) -> Optional[Dict[str, Any]]:
        return None

    async def process_night_action(self, action_data: Dict[str, Any], game_manager) -> Dict[str, Any]:
        return {}

    def get_investigation_result(self) -> str:
        return 'Suspicious'
