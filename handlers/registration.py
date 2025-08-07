import logging
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.models import User

logger = logging.getLogger(__name__)

class RegistrationHandler:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        user = await self.db_manager.get_user(user_id)
        
        if user:
            await self.show_main_menu(update, context, user)
        else:
            await self.show_registration(update, context)

    async def show_registration(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = "🎭 **Welcome to UC Kingdom!** 🎭\n\n"
        message += "A mysterious transformation awaits you in this village of animal spirits. "
        message += "Will you survive the night or fall to the predators?\n\n"
        message += "To begin your journey, you must register with an In-Game Name (IGN)."
        
        keyboard = [[InlineKeyboardButton("Register 📝", callback_data="register")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user: User):
        message = f"🎭 **Welcome back, {user.ign}!** 🎭\n\n"
        message += "What would you like to do today?"
        
        keyboard = [
            [InlineKeyboardButton("My Info 📊", callback_data="my_info")],
            [InlineKeyboardButton("Lucky Draw 🎁", callback_data="lucky_draw")],
            [InlineKeyboardButton("Add to Group ➕", callback_data="add_to_group")],
            [InlineKeyboardButton("Join UC Era 🌌", callback_data="join_uc_era")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.message:
            await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await update.callback_query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def handle_register_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        
        message = "Please enter your desired In-Game Name (IGN):\n\n"
        message += "📝 Your IGN will be displayed to other players during games.\n"
        message += "📝 You can change it once every 72 hours.\n"
        message += "📝 Choose wisely!"
        
        await update.callback_query.edit_message_text(message, parse_mode='Markdown')
        context.user_data['awaiting_ign'] = True

    async def handle_ign_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.user_data.get('awaiting_ign'):
            return
        
        user_id = update.effective_user.id
        ign = update.message.text.strip()
        
        if len(ign) < 2 or len(ign) > 20:
            await update.message.reply_text(
                "❌ IGN must be between 2 and 20 characters. Please try again."
            )
            return
        
        user = User(telegram_id=user_id, ign=ign)
        success = await self.db_manager.create_user(user)
        
        if success:
            context.user_data['awaiting_ign'] = False
            message = f"✅ Registration successful!\n\nWelcome to UC Kingdom, **{ign}**! 🎉"
            await update.message.reply_text(message, parse_mode='Markdown')
            
            await self.show_main_menu(update, context, user)
        else:
            await update.message.reply_text(
                "❌ Registration failed. Please try again later."
            )

    async def handle_my_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        
        user_id = update.effective_user.id
        user = await self.db_manager.get_user(user_id)
        
        if not user:
            await update.callback_query.edit_message_text("❌ User not found. Please register first.")
            return
        
        rank_info = user.get_rank_info()
        rank = rank_info['rank']
        current_stars = rank_info['current_stars']
        
        star_display = rank['emoji'] * current_stars
        if current_stars == 0:
            star_display = "-"
        
        message = f"👤 **Name:** {user.ign}\n"
        message += f"🎖️ **Rank:** {rank['name']} ({star_display})\n"
        message += f"🧱 **Bricks:** {user.bricks:,}\n"
        message += f"🎲 **Cubes:** Unavailable\n"
        message += f"⚔️ **Games Played:** {user.games_played}\n"
        message += f"📈 **Win Rate:** {user.get_win_rate():.1f}%\n"
        message += f"🗓️ **Joined:** {user.joined_date}\n"
        
        keyboard = [
            [InlineKeyboardButton("Change IGN ✏️", callback_data="change_ign")],
            [InlineKeyboardButton("Back 🔙", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def handle_change_ign(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        
        user_id = update.effective_user.id
        user = await self.db_manager.get_user(user_id)
        
        if not user:
            await update.callback_query.edit_message_text("❌ User not found.")
            return
        
        if user.last_ign_change:
            last_change = datetime.fromisoformat(user.last_ign_change)
            cooldown_end = last_change + timedelta(hours=72)
            
            if datetime.now() < cooldown_end:
                remaining = cooldown_end - datetime.now()
                hours_left = int(remaining.total_seconds() / 3600)
                
                message = f"❌ You can change your IGN again in {hours_left} hours.\n\n"
                message += f"Last change: {user.last_ign_change[:10]}"
                
                keyboard = [[InlineKeyboardButton("Back 🔙", callback_data="my_info")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.callback_query.edit_message_text(message, reply_markup=reply_markup)
                return
        
        message = "Please enter your new In-Game Name (IGN):\n\n"
        message += f"📝 Current IGN: **{user.ign}**\n"
        message += "📝 You can change it once every 72 hours."
        
        keyboard = [[InlineKeyboardButton("Cancel 🔙", callback_data="my_info")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['awaiting_ign_change'] = True

    async def handle_ign_change_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.user_data.get('awaiting_ign_change'):
            return
        
        user_id = update.effective_user.id
        new_ign = update.message.text.strip()
        
        if len(new_ign) < 2 or len(new_ign) > 20:
            await update.message.reply_text(
                "❌ IGN must be between 2 and 20 characters. Please try again."
            )
            return
        
        user = await self.db_manager.get_user(user_id)
        if not user:
            await update.message.reply_text("❌ User not found.")
            return
        
        old_ign = user.ign
        user.ign = new_ign
        user.last_ign_change = datetime.now().isoformat()
        
        success = await self.db_manager.update_user(user)
        
        if success:
            context.user_data['awaiting_ign_change'] = False
            message = f"✅ IGN changed successfully!\n\n"
            message += f"Old IGN: **{old_ign}**\n"
            message += f"New IGN: **{new_ign}**"
            await update.message.reply_text(message, parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ Failed to change IGN. Please try again later.")

    async def handle_add_to_group(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        
        message = "🤖 **Add UC Kingdom Bot to Your Group** 🤖\n\n"
        message += "To start playing UC Kingdom in your group chat:\n\n"
        message += "1️⃣ Click the link below\n"
        message += "2️⃣ Select your group chat\n"
        message += "3️⃣ Make the bot an admin (optional but recommended)\n"
        message += "4️⃣ Use /creategame to start a new game!\n\n"
        message += "🔗 https://t.me/uckingdombot?startgroup=true"
        
        keyboard = [[InlineKeyboardButton("Back 🔙", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def handle_join_uc_era(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        
        message = "🌌 **Join UC Era** 🌌\n\n"
        message += "Coming Soon! UC Kingdom is proud to be part of the future UC Era ecosystem.\n\n"
        message += "Stay tuned for more exciting games and features! 🚀"
        
        keyboard = [[InlineKeyboardButton("Back 🔙", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def handle_main_menu_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        
        user_id = update.effective_user.id
        user = await self.db_manager.get_user(user_id)
        
        if user:
            await self.show_main_menu(update, context, user)
        else:
            await self.show_registration(update, context)
