from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class BaseRole(ABC):
    def __init__(self, player_id: int, game_id: str):
        self.player_id = player_id
        self.game_id = game_id
        self.role_data = {}

    @abstractmethod
    def get_role_name(self) -> str:
        pass

    @abstractmethod
    def get_role_emoji(self) -> str:
        pass

    @abstractmethod
    def get_team(self) -> str:
        pass

    @abstractmethod
    def get_win_condition(self) -> str:
        pass

    @abstractmethod
    def get_role_description(self) -> str:
        pass

    @abstractmethod
    def has_night_action(self) -> bool:
        pass

    @abstractmethod
    async def get_night_action_prompt(self, game_manager, available_targets: List[int]) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def process_night_action(self, action_data: Dict[str, Any], game_manager) -> Dict[str, Any]:
        pass

    def can_be_targeted(self) -> bool:
        return True

    def get_investigation_result(self) -> str:
        if self.get_team() in ['predator', 'predator_aligned']:
            return 'Suspicious'
        return 'Non-Threatening Villager'

    def update_role_data(self, key: str, value: Any):
        self.role_data[key] = value

    def get_role_data(self, key: str, default: Any = None) -> Any:
        return self.role_data.get(key, default)
