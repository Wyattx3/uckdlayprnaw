import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
APPWRITE_ENDPOINT = os.getenv('APPWRITE_ENDPOINT')
APPWRITE_PROJECT_ID = os.getenv('APPWRITE_PROJECT_ID')
APPWRITE_API_KEY = os.getenv('APPWRITE_API_KEY')

MIN_PLAYERS = 7
MAX_PLAYERS = 20

INITIAL_DISCUSSION_TIME = 60
DAY_DISCUSSION_TIME = 45
VOTING_TIME = 15
LOBBY_TIMEOUT = 90

LUCKY_DRAW_COST = 1000
PERFORMANCE_BRICK_MULTIPLIER = 10

ITEM_PROBABILITIES = {
    'immortality_pill': 0.13,
    'reflection_mirror': 0.08,
    'sigma_banana': 0.15,
    'hecking_mask': 0.12,
    'mystic_eyes_amulet': 0.09,
    'transformation_wand': 0.05,
    'magic_gold_pot': 0.08,
    'bricks_900': 0.15,
    'bricks_800': 0.10,
    'bricks_700': 0.05
}

RANKS = [
    {'name': 'Beginner', 'name_mm': 'လေ့လာဆဲ', 'emoji': '⭐️', 'max_stars': 5},
    {'name': 'Player', 'name_mm': 'ကစားသမား', 'emoji': '🌟', 'max_stars': 5},
    {'name': 'Expert', 'name_mm': 'ကျွမ်းကျင်သူ', 'emoji': '💫', 'max_stars': 5},
    {'name': 'Adept', 'name_mm': 'အထာကျသူ', 'emoji': '✨', 'max_stars': 5},
    {'name': 'Master', 'name_mm': 'ဆရာကြီး', 'emoji': '⚡️', 'max_stars': 5}
]

ROLE_DISTRIBUTIONS = {
    7: ['Leopard', 'Jackal', 'Owl', 'Fox', 'Turtle', 'Deer', 'Hunter'],
    8: ['Leopard', 'Jackal', 'Owl', 'Fox', 'Turtle', 'Deer', 'Hunter', 'Buffalo'],
    9: ['Leopard', 'Jackal', 'Tiger', 'Owl', 'Fox', 'Turtle', 'Deer', 'Hunter', 'Buffalo'],
    10: ['Leopard', 'Jackal', 'Tiger', 'Owl', 'Fox', 'Turtle', 'Deer', 'Hunter', 'Buffalo', 'Monkey'],
    11: ['Leopard', 'Jackal', 'Tiger', 'Owl', 'Fox', 'Turtle', 'Deer', 'Hunter', 'Buffalo', 'Monkey', 'Hedgehog'],
    12: ['Leopard', 'Jackal', 'Tiger', 'Owl', 'Fox', 'Turtle', 'Deer', 'Hunter', 'Buffalo', 'Monkey', 'Hedgehog', 'Giraffe'],
    13: ['Leopard', 'Jackal', 'Tiger', 'Owl', 'Fox', 'Turtle', 'Deer', 'Hunter', 'Buffalo', 'Monkey', 'Hedgehog', 'Giraffe', 'Cow'],
    14: ['Leopard', 'Jackal', 'Tiger', 'Owl', 'Fox', 'Turtle', 'Deer', 'Hunter', 'Monkey', 'Hedgehog', 'Cow', 'Lion', 'Crocodile', 'Vulture'],
    15: ['Leopard', 'Jackal', 'Tiger', 'Owl', 'Fox', 'Turtle', 'Deer', 'Hunter', 'Monkey', 'Hedgehog', 'Cow', 'Lion', 'Crocodile', 'Vulture', 'Buffalo'],
    16: ['Leopard', 'Jackal', 'Tiger', 'Owl', 'Fox', 'Turtle', 'Deer', 'Hunter', 'Monkey', 'Hedgehog', 'Cow', 'Lion', 'Crocodile', 'Vulture', 'Buffalo', 'Giraffe'],
    17: ['Leopard', 'Jackal', 'Tiger', 'Wild Boar', 'Owl', 'Fox', 'Turtle', 'Deer', 'Hunter', 'Monkey', 'Hedgehog', 'Cow', 'Lion', 'Crocodile', 'Vulture', 'Buffalo', 'Giraffe'],
    18: ['Leopard', 'Jackal', 'Tiger', 'Wild Boar', 'Owl', 'Fox', 'Turtle', 'Deer', 'Hunter', 'Monkey', 'Hedgehog', 'Cow', 'Lion', 'Crocodile', 'Vulture', 'Buffalo', 'Giraffe', 'Bat'],
    19: ['Leopard', 'Jackal', 'Tiger', 'Wild Boar', 'Owl', 'Fox', 'Turtle', 'Deer', 'Hunter', 'Monkey', 'Hedgehog', 'Cow', 'Lion', 'Crocodile', 'Vulture', 'Buffalo', 'Giraffe', 'Bat', 'Sheep'],
    20: ['Leopard', 'Jackal', 'Jackal', 'Tiger', 'Wild Boar', 'Owl', 'Fox', 'Turtle', 'Deer', 'Hunter', 'Monkey', 'Hedgehog', 'Cow', 'Lion', 'Crocodile', 'Vulture', 'Buffalo', 'Giraffe', 'Bat', 'Sheep']
}

MAX_ROUNDS = 8
