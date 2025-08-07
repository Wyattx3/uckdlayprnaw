import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from database.db_manager import DatabaseManager
from game.game_manager import GameManager
from handlers.registration import RegistrationHandler
from handlers.game_lobby import GameLobbyHandler
from handlers.game_play import GamePlayHandler
from handlers.item_handler import ItemHandler
from config import BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class UCKingdomBot:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.game_manager = GameManager(self.db_manager, None)
        self.registration_handler = RegistrationHandler(self.db_manager)
        self.game_lobby_handler = GameLobbyHandler(self.db_manager, self.game_manager)
        self.game_play_handler = GamePlayHandler(self.db_manager, self.game_manager)
        self.item_handler = ItemHandler(self.db_manager)
        
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.game_manager.bot = self.application.bot
        
        self.setup_handlers()

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.registration_handler.handle_start))
        self.application.add_handler(CommandHandler("creategame", self.game_lobby_handler.handle_create_game))
        
        self.application.add_handler(CallbackQueryHandler(
            self.registration_handler.handle_register_callback,
            pattern="^register$"
        ))
        
        self.application.add_handler(CallbackQueryHandler(
            self.registration_handler.handle_my_info,
            pattern="^my_info$"
        ))
        
        self.application.add_handler(CallbackQueryHandler(
            self.registration_handler.handle_change_ign,
            pattern="^change_ign$"
        ))
        
        self.application.add_handler(CallbackQueryHandler(
            self.registration_handler.handle_add_to_group,
            pattern="^add_to_group$"
        ))
        
        self.application.add_handler(CallbackQueryHandler(
            self.registration_handler.handle_join_uc_era,
            pattern="^join_uc_era$"
        ))
        
        self.application.add_handler(CallbackQueryHandler(
            self.registration_handler.handle_main_menu_callback,
            pattern="^main_menu$"
        ))
        
        self.application.add_handler(CallbackQueryHandler(
            self.item_handler.handle_lucky_draw,
            pattern="^lucky_draw$"
        ))
        
        self.application.add_handler(CallbackQueryHandler(
            self.item_handler.handle_perform_draw,
            pattern="^perform_draw$"
        ))
        
        self.application.add_handler(CallbackQueryHandler(
            self.item_handler.handle_view_inventory,
            pattern="^view_inventory$"
        ))
        
        self.application.add_handler(CallbackQueryHandler(
            self.item_handler.handle_insufficient_bricks,
            pattern="^insufficient_bricks$"
        ))
        
        self.application.add_handler(CallbackQueryHandler(
            self.game_lobby_handler.handle_join_game,
            pattern="^join_game_"
        ))
        
        self.application.add_handler(CallbackQueryHandler(
            self.game_play_handler.handle_night_action_callback,
            pattern="^(night_target_|hunter_|leopard_|tiger_|herbivore_|wildboar_)"
        ))
        
        self.application.add_handler(CallbackQueryHandler(
            self.game_play_handler.handle_vote_callback,
            pattern="^vote_"
        ))
        
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.handle_text_message
        ))

    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.user_data.get('awaiting_ign'):
            await self.registration_handler.handle_ign_input(update, context)
        elif context.user_data.get('awaiting_ign_change'):
            await self.registration_handler.handle_ign_change_input(update, context)

    async def initialize(self):
        try:
            await self.db_manager.initialize_collections()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    async def run(self):
        await self.initialize()
        logger.info("Starting UC Kingdom Bot...")
        await self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def stop(self):
        logger.info("Stopping UC Kingdom Bot...")
        await self.application.stop()

async def main():
    bot = UCKingdomBot()
    try:
        await bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        raise
    finally:
        await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
