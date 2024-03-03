from telegram import Update
from telegram.ext import (
    CallbackContext,
    ConversationHandler
)
from bot.keyboards.reply import create_admin_panel_buttons
import env


async def admin_panel_handler(update: Update, context: CallbackContext):
    if update.message.from_user.id == int(env.Keys.ADMIN_ID):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the admin panel",
                                       reply_markup=create_admin_panel_buttons())
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are no admin boy")