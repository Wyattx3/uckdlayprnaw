import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from game.items import ItemSystem
from config import LUCKY_DRAW_COST

logger = logging.getLogger(__name__)

class ItemHandler:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.item_system = ItemSystem()

    async def handle_lucky_draw(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        
        user_id = update.effective_user.id
        user = await self.db_manager.get_user(user_id)
        
        if not user:
            await update.callback_query.edit_message_text("❌ User not found. Please register first.")
            return
        
        message = f"🎁 **Lucky Draw** 🎁\n\n"
        message += f"💰 Your Bricks: {user.bricks:,}\n"
        message += f"💎 Cost per draw: {LUCKY_DRAW_COST:,} Bricks\n\n"
        message += "Test your luck and win amazing items! 🍀"
        
        keyboard = []
        if user.bricks >= LUCKY_DRAW_COST:
            keyboard.append([InlineKeyboardButton("Draw Now! 🎲", callback_data="perform_draw")])
        else:
            keyboard.append([InlineKeyboardButton("❌ Insufficient Bricks", callback_data="insufficient_bricks")])
        
        keyboard.append([InlineKeyboardButton("View Inventory 📦", callback_data="view_inventory")])
        keyboard.append([InlineKeyboardButton("Back 🔙", callback_data="main_menu")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def handle_perform_draw(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        
        user_id = update.effective_user.id
        user = await self.db_manager.get_user(user_id)
        
        if not user or user.bricks < LUCKY_DRAW_COST:
            await update.callback_query.answer("❌ Insufficient bricks!", show_alert=True)
            return
        
        await update.callback_query.edit_message_text("🎲 Drawing... ✨", parse_mode='Markdown')
        
        import asyncio
        await asyncio.sleep(3)
        
        draw_result = self.item_system.perform_lucky_draw()
        
        user.bricks -= LUCKY_DRAW_COST
        
        if draw_result['type'] == 'item':
            user.items.append(draw_result['item_key'])
            result_message = f"🎉 **Congratulations!** 🎉\n\n"
            result_message += f"You won: {draw_result['display']}\n\n"
            result_message += f"💰 Bricks spent: {LUCKY_DRAW_COST:,}\n"
            result_message += f"💰 Remaining bricks: {user.bricks:,}"
        else:
            user.bricks += draw_result['amount']
            result_message = f"🎉 **Lucky!** 🎉\n\n"
            result_message += f"You won: {draw_result['display']}\n\n"
            result_message += f"💰 Net change: +{draw_result['amount'] - LUCKY_DRAW_COST:,} Bricks\n"
            result_message += f"💰 Total bricks: {user.bricks:,}"
        
        await self.db_manager.update_user(user)
        
        keyboard = [
            [InlineKeyboardButton("Draw Again! 🎲", callback_data="lucky_draw")],
            [InlineKeyboardButton("Back to Menu 🔙", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(result_message, reply_markup=reply_markup, parse_mode='Markdown')

    async def handle_view_inventory(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        
        user_id = update.effective_user.id
        user = await self.db_manager.get_user(user_id)
        
        if not user:
            await update.callback_query.edit_message_text("❌ User not found.")
            return
        
        message = f"📦 **{user.ign}'s Inventory** 📦\n\n"
        
        if not user.items:
            message += "Your inventory is empty. Try the Lucky Draw! 🎁"
        else:
            item_counts = {}
            for item_key in user.items:
                item_counts[item_key] = item_counts.get(item_key, 0) + 1
            
            for item_key, count in item_counts.items():
                item_info = self.item_system.get_item_info(item_key)
                if item_info:
                    count_text = f" x{count}" if count > 1 else ""
                    message += f"{item_info['emoji']} {item_info['name']}{count_text}\n"
                    message += f"   _{item_info['description']}_\n\n"
        
        keyboard = [
            [InlineKeyboardButton("Lucky Draw 🎁", callback_data="lucky_draw")],
            [InlineKeyboardButton("Back 🔙", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def handle_insufficient_bricks(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer("You need more bricks to draw! Play games to earn bricks.", show_alert=True)
