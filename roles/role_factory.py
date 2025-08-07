from typing import Dict, Any
from roles.base_role import BaseRole
from roles.villager_roles import (
    Lion, Hunter, Owl, Turtle, Monkey, Bat, Hedgehog,
    Deer, Giraffe, Buffalo, Cow, Sheep
)
from roles.predator_roles import Leopard, Tiger, Jackal, WildBoar
from roles.predator_aligned_roles import Vulture, Crocodile
from roles.neutral_roles import Fox

class RoleFactory:
    def __init__(self):
        self.role_classes = {
            'Lion': Lion,
            'Hunter': Hunter,
            'Owl': Owl,
            'Turtle': Turtle,
            'Monkey': Monkey,
            'Bat': Bat,
            'Hedgehog': Hedgehog,
            'Deer': Deer,
            'Giraffe': Giraffe,
            'Buffalo': Buffalo,
            'Cow': Cow,
            'Sheep': Sheep,
            'Leopard': Leopard,
            'Tiger': Tiger,
            'Jackal': Jackal,
            'Wild Boar': WildBoar,
            'Vulture': Vulture,
            'Crocodile': Crocodile,
            'Fox': Fox
        }

    def create_role(self, role_name: str, player_id: int, game_id: str) -> BaseRole:
        if role_name not in self.role_classes:
            raise ValueError(f"Unknown role: {role_name}")
        
        role_class = self.role_classes[role_name]
        return role_class(player_id, game_id)

    def get_available_roles(self) -> list:
        return list(self.role_classes.keys())

    def get_team_for_role(self, role_name: str) -> str:
        if role_name not in self.role_classes:
            return "unknown"
        
        temp_role = self.role_classes[role_name](0, "temp")
        return temp_role.get_team()
