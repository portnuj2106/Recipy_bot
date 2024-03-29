from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from ..constants import CLICK
from bot.global_vars import GlobalVars
from bot.global_vars import global_vars, preferences
from ..keyboards.inline import create_recipy_buttons, enter_new_ingredients_buttons, auth_create_recipy_buttons
from bot.API.api_preferences import api_preferences
from bot.bd.bd import users_db


class ShowRecipeAPI(GlobalVars):
    async def show_recipe(self, update: Update, context: CallbackContext):
        if global_vars.call_index >= len(global_vars.data):
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text="That's all new recipes available\n============================",
                                           reply_markup=enter_new_ingredients_buttons())
            return CLICK
        else:
            if not preferences.isVegetarian and not preferences.cookingTime:
                await context.bot.send_message(update.effective_chat.id, f"{global_vars.data[global_vars.call_index]['title']}")
                if users_db.is_authorized(update.effective_user.id):
                    await context.bot.send_photo(update.effective_chat.id, f"{global_vars.data[global_vars.call_index]['image']}",
                                                 reply_markup=auth_create_recipy_buttons())
                else:
                    await context.bot.send_photo(update.effective_chat.id,
                                                 f"{global_vars.data[global_vars.call_index]['image']}",
                                                 reply_markup=create_recipy_buttons())
                global_vars.call_index += 1
            else:
                recipe_ids = []
                for recipe in global_vars.data:
                    recipe_ids.append(recipe["id"])
                await api_preferences.check_preferences(update, context, recipe_ids)
            return CLICK

    async def show_missed_ingredients(self, update: Update, context: CallbackContext, call_ind, recipe_info) -> None:
        ingredients = ""
        for index, missedIngredient in enumerate(recipe_info[call_ind]["missedIngredients"]):
            ingredients += missedIngredient["name"].title()
            if index < len(recipe_info[call_ind]["missedIngredients"]) - 1:
                ingredients += ",  "
        await context.bot.send_message(update.effective_chat.id,
                                       f"You miss {recipe_info[call_ind]["missedIngredientCount"]} ingredients:  {ingredients}")


api_show = ShowRecipeAPI()