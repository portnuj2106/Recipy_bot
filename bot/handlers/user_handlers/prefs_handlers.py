from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
)
from bot.keyboards.inline import create_prefs_buttons, yes_or_no_buttons
from bot.constants import *
from bot.global_vars import preferences



async def set_prefs(update: Update, context: CallbackContext) -> int:
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Start", callback_data="start")]])
    await context.bot.send_message(chat_id=update.effective_chat.id, text="We are going to ask you for your preferences",
                                   reply_markup=reply_markup)
    return PREF_START


async def set_prefs_start(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    if query.data == "start":
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Are you a vegetarian?",
                                       reply_markup=yes_or_no_buttons())
        return VEGETARIAN


async def is_vegetarian(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    if query.data == "yes":
        preferences.isVegetarian = True
    else:
        preferences.isVegetarian = False
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Got it")
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="You want to see meals with shorter cooking time first?",
                                   reply_markup=yes_or_no_buttons())
    return COOKING


async def cooking_time(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    if query.data == "yes":
        preferences.cookingTime = True
    else:
        preferences.cookingTime = False
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Got it")
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="You want to see healthier meals first?",
                                   reply_markup=yes_or_no_buttons())
    return HEALTHY


async def is_healthier(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    if query.data == "yes":
        preferences.isHealthy = True
    else:
        preferences.isHealthy = False
    await context.bot.send_message(chat_id=update.effective_chat.id, text="That's all, press the button below to enter ingredients")

    return ConversationHandler.END


# async def go_to_recipes(update: Update, context: CallbackContext) -> int:
#     query = update.callback_query
#     if query.data == "goToRecipes":
#         await context.bot.send_message(chat_id=update.effective_chat.id, text="Enter ingredients")
