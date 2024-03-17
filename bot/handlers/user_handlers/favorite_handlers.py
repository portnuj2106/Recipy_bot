from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    CallbackContext,
    ConversationHandler
)
from bot.bd.bd import users_db
import env
from bot.API.api_preferences import api_preferences
from bot.keyboards.inline import favorite_recipes_buttons
from bot.constants import NEXT_RECIPE
from bot.API.api_get import recipy_api
from bot.API.api_show import api_show
recipe_index = 0
recipes_infos = ''


async def get_favorite_recipes(update: Update, context: CallbackContext):
    global recipes_infos
    recipes_ids = users_db.get_user_recipes_string(update.effective_user.id)
    recipes_infos = await api_preferences.get_recipes_info(update, context, recipes_ids)
    return recipes_infos


async def show_favorite_recipes(update: Update, context: CallbackContext):
    global recipes_infos, recipe_index
    recipes_infos = await get_favorite_recipes(update, context)
    if recipes_infos:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=recipes_infos[recipe_index]['title'])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=recipes_infos[recipe_index]['image'],
                                       reply_markup=favorite_recipes_buttons(update.effective_chat.id, recipe_index, len(recipes_infos)))
        return NEXT_RECIPE
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No recipes")
        return ConversationHandler.END






async def next_recipe(update: Update, context: CallbackContext):
    global recipes_infos, recipe_index
    query = update.callback_query
    if query.data == 'next':
        pass
    elif query.data == 'description':
        await recipy_api.search_for_description(update, context, recipe_index, recipes_infos)
    elif query.data == 'deleteFav':
        users_db.delete_user_recipe(update.effective_user.id, recipes_infos[recipe_index]['id'])
        check_for_recipes = await get_favorite_recipes(update, context)
        if check_for_recipes:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Recipe removed from favorites")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="No more recipes")
            return ConversationHandler.END
    return NEXT_RECIPE




