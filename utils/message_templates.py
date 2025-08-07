def get_role_assignment_message(role_name: str, role_emoji: str, description: str, team: str, win_condition: str) -> str:
    message = f"🎭 **UC Kingdom - Role Assignment** 🎭\n\n"
    message += f"**Your Role:** {role_name} {role_emoji}\n\n"
    message += f"**Description:** {description}\n\n"
    message += f"**Team:** {team.title()}\n\n"
    message += f"**Win Condition:** {win_condition}\n\n"
    message += "Good luck! 🍀"
    return message

def get_game_start_message(player_count: int) -> str:
    message = "🎭 **A new game of UC Kingdom is starting!** 🎭\n\n"
    message += f"Registered players, click the button below to join within 90 seconds!\n\n"
    message += f"👥 Players needed: 7-20\n"
    message += f"🎮 Current players: {player_count}"
    return message

def get_night_phase_message() -> str:
    return "Night falls... 🌃 All villagers seek shelter. Those with night duties, check your PMs for instructions."

def get_day_phase_message(discussion_time: int) -> str:
    return f"The sun rises... ☀️ Let's see who survived the night.\n\nDiscuss the night's events. You have {discussion_time} seconds. 💬"

def get_voting_message() -> str:
    return "Time to vote! Who is suspicious? You have 15 seconds. ⚖️"

def get_game_end_message(winning_team: str, survivors: list) -> str:
    if winning_team == 'Villagers':
        message = "The last predator has been vanquished! The village is safe once more! 🎉\n\n"
        message += "**Survivors:**\n"
        message += "\n".join(survivors)
    elif winning_team == 'Predators':
        message = "The predators have overwhelmed the village! Darkness reigns... 👑\n\n"
        message += "**Victorious Predators:**\n"
        message += "\n".join(survivors)
    elif winning_team == 'Fox':
        message = "The Fox has achieved its cunning victory! 🦊\n\n"
        message += "\n".join(survivors)
    else:
        message = "The game has ended in a draw. 🤝"
    
    return message

def get_performance_message(winning_team: str) -> str:
    if winning_team == 'Villagers':
        return "Peace has returned to the village:"
    elif winning_team == 'Predators':
        return "The village has fallen to darkness:"
    else:
        return "A cunning victory:"
