import random
from typing import Dict, List, Any, Optional
from config import ITEM_PROBABILITIES, LUCKY_DRAW_COST

class ItemSystem:
    def __init__(self):
        self.items = {
            'immortality_pill': {
                'name': 'Immortality Pill',
                'name_mm': 'မသေဆေးဓာတ်လုံး',
                'emoji': '💊',
                'description': 'Survive one lethal attack during the night. Consumed after use.',
                'type': 'defensive',
                'one_time': True
            },
            'reflection_mirror': {
                'name': 'Reflection Mirror',
                'name_mm': 'တန်ပြန်မှော်မှန်',
                'emoji': '🪞',
                'description': 'Reflect any harmful night action back to the attacker. One-time use.',
                'type': 'defensive',
                'one_time': True
            },
            'sigma_banana': {
                'name': 'Sigma Banana',
                'name_mm': 'ငှက်ပျောသီး',
                'emoji': '🍌',
                'description': 'Monkey cannot role-block you. Passive protection while held.',
                'type': 'passive',
                'one_time': False
            },
            'hecking_mask': {
                'name': 'Hecking Mask',
                'name_mm': 'ငတက်ပြား',
                'emoji': '🎭',
                'description': 'Use target\'s night ability instead of your own for one night.',
                'type': 'active',
                'one_time': True
            },
            'mystic_eyes_amulet': {
                'name': 'Mystic Eyes Amulet',
                'name_mm': 'ပဥ္စလက်မျက်လုံး',
                'emoji': '🪬',
                'description': 'Appear as "Non-Threatening Villager" to investigations. Passive while held.',
                'type': 'passive',
                'one_time': False
            },
            'transformation_wand': {
                'name': 'Transformation Wand',
                'name_mm': 'အသွင်းပြောင်းတောင်ဝှေ့',
                'emoji': '🪄',
                'description': 'Swap roles with target for one night. One-time use.',
                'type': 'active',
                'one_time': True
            },
            'magic_gold_pot': {
                'name': 'Magic Gold Pot (x2)',
                'name_mm': 'မှော်ဝင်ရွှေအိုး',
                'emoji': '🏺',
                'description': 'Receive double Rank Stars and Bricks if your team wins.',
                'type': 'passive',
                'one_time': False
            }
        }

    def perform_lucky_draw(self) -> Dict[str, Any]:
        rand = random.random()
        cumulative_prob = 0
        
        for item_key, probability in ITEM_PROBABILITIES.items():
            cumulative_prob += probability
            if rand <= cumulative_prob:
                if item_key.startswith('bricks_'):
                    amount = int(item_key.split('_')[1])
                    return {
                        'type': 'bricks',
                        'amount': amount,
                        'display': f"{amount} Bricks 🧱"
                    }
                else:
                    item = self.items[item_key]
                    return {
                        'type': 'item',
                        'item_key': item_key,
                        'item': item,
                        'display': f"{item['name']} {item['emoji']}"
                    }
        
        return {
            'type': 'bricks',
            'amount': 700,
            'display': "700 Bricks 🧱"
        }

    def get_item_info(self, item_key: str) -> Optional[Dict[str, Any]]:
        return self.items.get(item_key)

    def can_use_item(self, item_key: str, game_phase: str, player_role: str) -> bool:
        item = self.get_item_info(item_key)
        if not item:
            return False
        
        if item['type'] == 'passive':
            return True
        elif item['type'] == 'active' and game_phase == 'night':
            return True
        elif item['type'] == 'defensive':
            return True
        
        return False

    def apply_item_effect(self, item_key: str, player_id: int, game_data: Dict[str, Any], 
                         action_data: Dict[str, Any] = None) -> Dict[str, Any]:
        item = self.get_item_info(item_key)
        if not item:
            return {}
        
        effect_result = {'item_used': item_key, 'effect_applied': True}
        
        if item_key == 'immortality_pill':
            effect_result['type'] = 'immunity'
            effect_result['message'] = "The Immortality Pill protected you from death!"
        
        elif item_key == 'reflection_mirror':
            effect_result['type'] = 'reflection'
            effect_result['message'] = "The Reflection Mirror sent the attack back to the attacker!"
        
        elif item_key == 'sigma_banana':
            effect_result['type'] = 'role_block_immunity'
            effect_result['message'] = "The Sigma Banana protects you from the Monkey's chatter!"
        
        elif item_key == 'hecking_mask':
            effect_result['type'] = 'ability_steal'
            effect_result['target_id'] = action_data.get('target_id') if action_data else None
        
        elif item_key == 'mystic_eyes_amulet':
            effect_result['type'] = 'investigation_immunity'
            effect_result['fake_result'] = 'Non-Threatening Villager'
        
        elif item_key == 'transformation_wand':
            effect_result['type'] = 'role_swap'
            effect_result['target_id'] = action_data.get('target_id') if action_data else None
        
        elif item_key == 'magic_gold_pot':
            effect_result['type'] = 'reward_multiplier'
            effect_result['multiplier'] = 2
        
        return effect_result

    def get_all_items(self) -> Dict[str, Dict[str, Any]]:
        return self.items.copy()
