from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
)
import re
from bot.keyboards.inline import create_prefs_buttons, yes_or_no_buttons
from bot.constants import *
from bot.global_vars import preferences
from bot.bd.bd import users_db

user_name = ''


async def start_registration(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    if users_db.user_exists(user_id):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are already registered.")
        return ConversationHandler.END
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Your name:")
        return NAME



async def save_nickname(update: Update, context: CallbackContext) -> int:
    if len(update.message.text.strip()) > 20:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Name is too long, try again:")
        return NAME
    else:
        global user_name
        user_name = update.message.text
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Your email:")
        return EMAIL


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


async def save_email(update: Update, context: CallbackContext) -> int:
    if is_valid_email(update.message.text):
        global user_name
        user_email = update.message.text
        user_id = update.message.from_user.id
        users_db.add_user(user_id, user_name, user_email)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"You have been registered as: {user_name}")
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"You may proceed to entering ingredients or setting preferences")
        return ConversationHandler.END
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid email, try again:")
        return EMAIL



# async def save_user_to_db(update: Update, context: CallbackContext) -> int:
#     print("Entering the save func")
#     global user_name, user_email
#     user_id = update.message.from_user.id
#     users_db.add_user(user_id, user_name, user_email)
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{users_db.get_all_users()}")
#     return ConversationHandler.END




