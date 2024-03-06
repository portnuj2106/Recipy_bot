from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    CallbackContext,
    ConversationHandler
)
from bot.keyboards.reply import create_admin_panel_buttons
from bot.bd.bd import users_db
import env
from bot.API.api_preferences import api_preferences


async def get_favorite_recipes(update: Update, context: CallbackContext):
    recipes_ids = users_db.get_user_recipes_string(update.effective_user.id)
    recipes_infos = await api_preferences.get_recipes_info(update, context, recipes_ids)


