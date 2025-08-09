import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8384463880:AAEJpcYfOFDkiUeWSbvouqbK_P-kEiT_9IU")
APPWRITE_ENDPOINT = os.environ.get("APPWRITE_ENDPOINT", "https://nyc.cloud.appwrite.io/v1")
APPWRITE_PROJECT_ID = os.environ.get("APPWRITE_PROJECT_ID", "68949b6b0037a2951a75")
APPWRITE_API_KEY = os.environ.get("APPWRITE_API_KEY", "standard_5db2f28a61872116743dd7f3448d0288723fa72e129cd7e5c4e93d9e6d03a9d61839eb2ad7093bac7574f1146c2b0b02ea9a4a8e8060da75cc790e31c99acd55d2f1b3382834a412bacb56d34f5e16c34ea1a6fddf03d103228a671cff336e9a5fd85f8e4457774212d397b3bb17cd2b6c9550141e83dde4a8d0cf3337ff2fba")

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
