from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from ..constants import CLICK, PREF_GREET
from bot.global_vars import GlobalVars
from bot.global_vars import global_vars, preferences
from ..keyboards.inline import create_recipy_buttons, enter_new_ingredients_buttons
from bot.API.api_preferences import api_preferences

class ShowRecipeAPI(GlobalVars):
    async def show_recipe(self, update: Update, context: CallbackContext):
        if update.message and update.message.text == "Set preferences":
            return ConversationHandler.END
        if global_vars.call_index >= len(global_vars.data):
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text="That's all new recipes available\n============================",
                                           reply_markup=enter_new_ingredients_buttons())
            return CLICK
        else:
            if not preferences.isVegetarian and not preferences.cookingTime:
                await context.bot.send_message(update.effective_chat.id, f"{global_vars.data[global_vars.call_index]['title']}")
                await context.bot.send_photo(update.effective_chat.id, f"{global_vars.data[global_vars.call_index]['image']}",
                                             reply_markup=create_recipy_buttons())
                global_vars.call_index += 1
            else:
                await api_preferences.get_recipes_info(update, context)
            return CLICK

    async def show_missed_ingredients(self, update: Update, context: CallbackContext, call_ind) -> None:
        ingredients = ""
        for index, missedIngredient in enumerate(global_vars.data[call_ind]["missedIngredients"]):
            ingredients += missedIngredient["name"].title()
            if index < len(global_vars.data[call_ind]["missedIngredients"]) - 1:
                ingredients += ",  "
        await context.bot.send_message(update.effective_chat.id,
                                       f"You miss {global_vars.data[call_ind]["missedIngredientCount"]} ingredients:  {ingredients}")


api_show = ShowRecipeAPI()