# UC Kingdom - Telegram Bot Game

A complex multiplayer social deduction game (similar to Mafia/Werewolf) featuring 19 animal roles across 4 teams, supporting 7-20 players with day/night cycles, voting mechanics, item system, ranking system, and performance tracking.

## Features

- **19 Animal Roles** across 4 teams (Villager, Predator, Predator-Aligned, Neutral)
- **7-20 Player Support** with dynamic role distribution
- **Day/Night Cycle Gameplay** with phase-based mechanics
- **Item System** with Lucky Draw mechanics (7 unique items)
- **Ranking System** with 5 ranks and star progression
- **Performance Tracking** with brick rewards
- **Appwrite Cloud Database** integration for data persistence

## Game Roles

### Villager Team
- **Lion** 🦁 - Leader, immune to first predator attack
- **Hunter** 🏹 - Can investigate or kill each night
- **Owl** 🦉 - Healer, protects players from attacks
- **Turtle** 🐢 - Survives first attack with shell
- **Monkey** 🐒 - Role-blocks players with conversation
- **Bat** 🦇 - Identifies attackers with echolocation
- **Hedgehog** 🦔 - Kills attackers with spines
- **Herbivores** (Deer 🦌, Giraffe 🦒, Buffalo 🐃, Cow 🐄, Sheep 🐑) - Witness incidents at locations

### Predator Team
- **Leopard** 🐆 - Pack leader, orders kills
- **Tiger** 🐅 - Second-in-command, takes over if Leopard dies
- **Jackal** 🐕 - Executes kill orders
- **Wild Boar** 🐗 - Territorial forager, blocks herbivores

### Predator-Aligned
- **Vulture** 🐦‍⬛ - Can sacrifice itself on command
- **Crocodile** 🐊 - Only role that can injure Lion

### Neutral
- **Fox** 🦊 - Wins by being eliminated while appearing suspicious

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your bot token and Appwrite credentials
```

3. Run the bot:
```bash
python main.py
```

## Environment Variables

- `BOT_TOKEN` - Your Telegram bot token
- `APPWRITE_ENDPOINT` - Appwrite API endpoint
- `APPWRITE_PROJECT_ID` - Appwrite project ID
- `APPWRITE_API_KEY` - Appwrite API key

## Game Flow

1. **Registration** - Players register with IGN (In-Game Name)
2. **Lobby** - Creator starts game, players join (90-second timer)
3. **Role Assignment** - Roles distributed based on player count
4. **Initial Discussion** - 60 seconds to talk before first night
5. **Night Phase** - Role actions via PM
6. **Day Phase** - 45 seconds discussion + 15 seconds voting
7. **Elimination** - Voted player eliminated, roles revealed
8. **Win Condition Check** - Game ends when team achieves victory
9. **Performance Calculation** - Stars and bricks awarded

## Commands

- `/start` - Register and access main menu
- `/creategame` - Create new game in group chat (group only)

## Database Schema

### Users Collection
- `telegram_id` - Unique Telegram user ID
- `ign` - In-Game Name
- `rank_stars` - Current rank progression
- `bricks` - Currency for Lucky Draw
- `items` - Owned items array
- `games_played` - Total games count
- `games_won` - Won games count

### Games Collection
- `game_id` - Unique game identifier
- `chat_id` - Telegram chat ID
- `creator_id` - Game creator's user ID
- `current_phase` - Current game phase
- `players` - Array of player IDs
- `game_data` - Game state data

### Game Players Collection
- `game_id` - Reference to game
- `user_id` - Reference to user
- `role` - Assigned role
- `role_data` - Role-specific data
- `eliminated` - Elimination status
- `performance_stars` - End-game performance

## Architecture

- **Database Layer** - Appwrite cloud database integration
- **Game Logic** - Modular role system with inheritance
- **Phase Management** - Night/day cycle coordination
- **Voting System** - Democratic elimination mechanics
- **Item System** - Lucky Draw and item effects
- **Handlers** - Telegram bot interaction management

## Testing

The bot includes comprehensive testing for:
- User registration and profile management
- Game creation and lobby mechanics
- All 19 roles and their abilities
- Day/night phase transitions
- Voting and elimination
- Item system and Lucky Draw
- Ranking and performance calculation

## Production Deployment

The bot is designed for production use with:
- Async/await patterns for performance
- Comprehensive error handling
- Logging and monitoring
- Scalable database architecture
- Modular code structure

## Copyright

Bot created and copyrighted by Team UCM.
