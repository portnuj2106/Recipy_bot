from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    CallbackContext,
    ConversationHandler
)
from bot.keyboards.reply import create_admin_panel_buttons
from bot.bd.bd import users_db
import env



async def admin_panel_handler(update: Update, context: CallbackContext):
    if update.message.from_user.id == int(env.Keys.ADMIN_ID):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the admin panel",
                                       reply_markup=create_admin_panel_buttons())
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are no admin boy")


async def view_users(update: Update, context: CallbackContext):
    users = users_db.get_all_users()
    if users:
        for user in users:
            user_id = user[0]
            user_name = user[1]
            user_email = user[2]
            keyboard = [[InlineKeyboardButton("Delete", callback_data=f"delete_{user_id}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            message_text = f"User ID: {user_id}\nName: {user_name}\nEmail: {user_email}"
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message_text,
                reply_markup=reply_markup
            )
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No registered users")


async def delete_user(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data.startswith("delete_"):
        try:
            user_id = int(query.data.split("_")[1])  # Extract user ID from callback data
            users_db.delete_user(user_id)  # Delete user with the specified user ID
            await query.answer("User deleted successfully.")
            await view_users(update, context)
        except (IndexError, ValueError):
            await query.answer("Invalid user ID.")
