import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

class GamePlayHandler:
    def __init__(self, db_manager, game_manager):
        self.db_manager = db_manager
        self.game_manager = game_manager

    async def handle_night_action_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        
        callback_data = update.callback_query.data
        parts = callback_data.split('_')
        
        if len(parts) < 3:
            return
        
        user_id = update.effective_user.id
        
        if callback_data.startswith('night_target_'):
            target_id = int(parts[2])
            game_id = parts[3]
            
            action_data = {
                'target_id': target_id,
                'action_type': 'target'
            }
            
            phase_manager = self.game_manager.phase_managers.get(game_id)
            if phase_manager:
                success = await phase_manager.handle_night_action(user_id, action_data)
                if not success:
                    await update.callback_query.answer("❌ Invalid action.", show_alert=True)
        
        elif callback_data.startswith('hunter_'):
            action_type = parts[1]
            game_id = parts[2]
            
            if action_type in ['investigate', 'kill']:
                game_players = await self.db_manager.get_game_players(game_id)
                active_players = [p for p in game_players if not p.eliminated and p.user_id != user_id]
                
                if not active_players:
                    await update.callback_query.answer("❌ No valid targets.", show_alert=True)
                    return
                
                message = f"Hunter, choose your target to {action_type}:"
                buttons = []
                
                for player in active_players:
                    player_ign = await self.game_manager.get_player_ign(player.user_id)
                    buttons.append({
                        'text': player_ign,
                        'callback_data': f"hunter_{action_type}_target_{player.user_id}_{game_id}"
                    })
                
                keyboard = []
                for button in buttons:
                    keyboard.append([InlineKeyboardButton(button['text'], callback_data=button['callback_data'])])
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.callback_query.edit_message_text(message, reply_markup=reply_markup)
        
        elif callback_data.startswith('hunter_investigate_target_') or callback_data.startswith('hunter_kill_target_'):
            action_parts = callback_data.split('_')
            action_type = action_parts[1]
            target_id = int(action_parts[3])
            game_id = action_parts[4]
            
            action_data = {
                'action_type': action_type,
                'target_id': target_id
            }
            
            phase_manager = self.game_manager.phase_managers.get(game_id)
            if phase_manager:
                success = await phase_manager.handle_night_action(user_id, action_data)
                if not success:
                    await update.callback_query.answer("❌ Invalid action.", show_alert=True)
        
        elif callback_data.startswith('leopard_') or callback_data.startswith('tiger_'):
            role = parts[0]
            action_type = parts[1]
            game_id = parts[2]
            
            if action_type == 'kill':
                game_players = await self.db_manager.get_game_players(game_id)
                active_players = [p for p in game_players if not p.eliminated and p.user_id != user_id]
                
                if not active_players:
                    await update.callback_query.answer("❌ No valid targets.", show_alert=True)
                    return
                
                message = f"{role.title()}, choose your kill target:"
                buttons = []
                
                for player in active_players:
                    player_ign = await self.game_manager.get_player_ign(player.user_id)
                    buttons.append({
                        'text': player_ign,
                        'callback_data': f"{role}_kill_target_{player.user_id}_{game_id}"
                    })
                
                keyboard = []
                for button in buttons:
                    keyboard.append([InlineKeyboardButton(button['text'], callback_data=button['callback_data'])])
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.callback_query.edit_message_text(message, reply_markup=reply_markup)
            
            elif action_type == 'vulture':
                action_data = {
                    'action_type': 'vulture_command'
                }
                
                phase_manager = self.game_manager.phase_managers.get(game_id)
                if phase_manager:
                    success = await phase_manager.handle_night_action(user_id, action_data)
                    if not success:
                        await update.callback_query.answer("❌ Invalid action.", show_alert=True)
        
        elif callback_data.startswith('leopard_kill_target_') or callback_data.startswith('tiger_kill_target_'):
            action_parts = callback_data.split('_')
            role = action_parts[0]
            target_id = int(action_parts[3])
            game_id = action_parts[4]
            
            action_data = {
                'action_type': 'kill',
                'target_id': target_id
            }
            
            phase_manager = self.game_manager.phase_managers.get(game_id)
            if phase_manager:
                success = await phase_manager.handle_night_action(user_id, action_data)
                if not success:
                    await update.callback_query.answer("❌ Invalid action.", show_alert=True)
        
        elif callback_data.startswith('herbivore_'):
            location = parts[1]
            game_id = parts[2]
            
            action_data = {
                'location': location
            }
            
            phase_manager = self.game_manager.phase_managers.get(game_id)
            if phase_manager:
                success = await phase_manager.handle_night_action(user_id, action_data)
                if not success:
                    await update.callback_query.answer("❌ Invalid action.", show_alert=True)
        
        elif callback_data.startswith('wildboar_'):
            location = parts[1]
            game_id = parts[2]
            
            action_data = {
                'location': location
            }
            
            phase_manager = self.game_manager.phase_managers.get(game_id)
            if phase_manager:
                success = await phase_manager.handle_night_action(user_id, action_data)
                if not success:
                    await update.callback_query.answer("❌ Invalid action.", show_alert=True)

    async def handle_vote_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        
        callback_data = update.callback_query.data
        parts = callback_data.split('_')
        
        if len(parts) < 3:
            return
        
        target_id = int(parts[1])
        game_id = parts[2]
        voter_id = update.effective_user.id
        
        voting_system = self.game_manager.voting_systems.get(game_id)
        if not voting_system:
            await update.callback_query.answer("❌ Voting is not active.", show_alert=True)
            return
        
        success = await voting_system.cast_vote(voter_id, target_id)
        if not success:
            await update.callback_query.answer("❌ Vote failed.", show_alert=True)
