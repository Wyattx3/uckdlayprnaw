import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import MIN_PLAYERS, MAX_PLAYERS, LOBBY_TIMEOUT

logger = logging.getLogger(__name__)

class GameLobbyHandler:
    def __init__(self, db_manager, game_manager):
        self.db_manager = db_manager
        self.game_manager = game_manager
        self.lobby_timers = {}

    async def handle_create_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.type == 'private':
            await update.message.reply_text(
                "❌ Games can only be created in group chats. Add me to a group first!"
            )
            return
        
        chat_id = update.effective_chat.id
        creator_id = update.effective_user.id
        
        user = await self.db_manager.get_user(creator_id)
        if not user:
            await update.message.reply_text(
                "❌ You need to register first! Send me a private message to get started."
            )
            return
        
        existing_game = await self.db_manager.get_active_game_by_chat(chat_id)
        if existing_game:
            await update.message.reply_text(
                "❌ There's already an active game in this chat!"
            )
            return
        
        game_id = await self.game_manager.create_game(chat_id, creator_id)
        if not game_id:
            await update.message.reply_text(
                "❌ Failed to create game. Please try again."
            )
            return
        
        message = "🎭 **A new game of UC Kingdom is starting!** 🎭\n\n"
        message += f"Registered players, click the button below to join within {LOBBY_TIMEOUT} seconds!\n\n"
        message += f"👥 Players needed: {MIN_PLAYERS}-{MAX_PLAYERS}\n"
        message += f"🎮 Creator: {user.ign}"
        
        keyboard = [[InlineKeyboardButton("Join Game 🎯", callback_data=f"join_game_{game_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
        
        self.lobby_timers[game_id] = asyncio.create_task(self.lobby_timeout(game_id, chat_id))

    async def handle_join_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        
        callback_data = update.callback_query.data
        game_id = callback_data.split('_')[2]
        user_id = update.effective_user.id
        
        user = await self.db_manager.get_user(user_id)
        if not user:
            await update.callback_query.answer(
                "❌ Please register with me first! Send me a private message.",
                show_alert=True
            )
            return
        
        game = await self.db_manager.get_game(game_id)
        if not game or game.current_phase != 'lobby':
            await update.callback_query.answer(
                "❌ This game is no longer accepting players.",
                show_alert=True
            )
            return
        
        if user_id in game.players:
            await update.callback_query.answer(
                "❌ You're already in this game!",
                show_alert=True
            )
            return
        
        if len(game.players) >= MAX_PLAYERS:
            await update.callback_query.answer(
                "❌ This game is full!",
                show_alert=True
            )
            return
        
        success = await self.game_manager.join_game(game_id, user_id)
        if not success:
            await update.callback_query.answer(
                "❌ Failed to join game. Please try again.",
                show_alert=True
            )
            return
        
        game = await self.db_manager.get_game(game_id)
        player_names = []
        for player_id in game.players:
            player_user = await self.db_manager.get_user(player_id)
            if player_user:
                player_names.append(player_user.ign)
        
        message = "🎭 **A new game of UC Kingdom is starting!** 🎭\n\n"
        message += f"Registered players, click the button below to join within {LOBBY_TIMEOUT} seconds!\n\n"
        message += f"👥 Players ({len(game.players)}/{MAX_PLAYERS}):\n"
        message += "\n".join([f"• {name}" for name in player_names])
        
        keyboard = [[InlineKeyboardButton("Join Game 🎯", callback_data=f"join_game_{game_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            message, reply_markup=reply_markup, parse_mode='Markdown'
        )
        
        await update.callback_query.answer(f"✅ {user.ign} joined the game!")
        
        if len(game.players) >= MIN_PLAYERS:
            if game_id in self.lobby_timers:
                self.lobby_timers[game_id].cancel()
                del self.lobby_timers[game_id]
            
            await asyncio.sleep(2)
            await self.start_game_if_ready(game_id)

    async def lobby_timeout(self, game_id: str, chat_id: int):
        try:
            await asyncio.sleep(LOBBY_TIMEOUT)
            
            game = await self.db_manager.get_game(game_id)
            if not game or game.current_phase != 'lobby':
                return
            
            if len(game.players) >= MIN_PLAYERS:
                await self.start_game_if_ready(game_id)
            else:
                await self.game_manager.send_group_message(
                    chat_id,
                    f"❌ Game cancelled due to insufficient players. Need at least {MIN_PLAYERS} players."
                )
                await self.game_manager.cleanup_game()
        
        except asyncio.CancelledError:
            pass
        finally:
            self.lobby_timers.pop(game_id, None)

    async def start_game_if_ready(self, game_id: str):
        game = await self.db_manager.get_game(game_id)
        if not game or game.current_phase != 'lobby':
            return
        
        if len(game.players) < MIN_PLAYERS:
            return
        
        success = await self.game_manager.start_game(game_id)
        if not success:
            await self.game_manager.send_group_message(
                game.chat_id,
                "❌ Failed to start game. Please try creating a new one."
            )
