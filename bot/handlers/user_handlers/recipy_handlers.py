import env

from telegram import Update
from telegram.ext import (
    CallbackContext,
)

from bot.API.api_get import recipy_api
from bot.API.api_show import api_show
from bot.constants import *
from bot.global_vars import global_vars
from bot.keyboards.reply import create_reply_buttons, create_admin_buttons, auth_create_reply_buttons
from bot.bd.bd import users_db


async def start(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id == int(env.Keys.ADMIN_ID):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"What's up, welcome to my recipe bot!",
                                       reply_markup=create_admin_buttons())
    elif users_db.is_authorized(update.effective_user.id):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"What's up, welcome to my recipe bot!",
                                       reply_markup=auth_create_reply_buttons())
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="What's up, welcome to my recipe bot!",
                                       reply_markup=create_reply_buttons())


async def help(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Please enter new ingredients.{update.message.from_user.id}")


async def start_search(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Great! Please enter the ingredients you have.")
    return SEARCH


async def on_recipy_click(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    if query.data == "another":
        await api_show.show_recipe(update, context)
    elif query.data == "new":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please, enter new ingredients.")
        global_vars.call_index = 0
        global_vars.data = ""
        return SEARCH
    elif query.data == "more":
        await recipy_api.search_for_description(update, context, global_vars.call_index, global_vars.data)
        if global_vars.call_index < 0 or global_vars.call_index >= len(global_vars.data):
            await api_show.show_missed_ingredients(update, context, global_vars.call_index - 1, global_vars.data)
        else:
            await api_show.show_missed_ingredients(update, context, global_vars.call_index, global_vars.data)
    elif query.data == "favorite":
        if global_vars.call_index < 0 or global_vars.call_index >= len(global_vars.data):
            users_db.add_user_recipe(update.effective_user.id, global_vars.data[global_vars.call_index - 1]["id"])
        else:
            users_db.add_user_recipe(update.effective_user.id, global_vars.data[global_vars.call_index]["id"])






