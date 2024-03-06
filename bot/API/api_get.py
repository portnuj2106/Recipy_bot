import requests
import json
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
import env
from ..constants import CLICK, SEARCH, PREF_START
from bot.global_vars import GlobalVars
from bot.global_vars import global_vars
from .api_show import api_show
from bot.bd.bd import users_db

class GetRecipeAPI(GlobalVars):
    async def search_for_recipes(self, update: Update, context: CallbackContext) -> int:
        if update.message.text == "Set preferences":
            await context.bot.send_message(chat_id=update.effective_chat.id, text="If you want to set preferences press the button bellow")
            return ConversationHandler.END
        ingredients = str(update.message.text.lower().strip())
        res = requests.get(
            f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=3&apiKey={env.Keys.API_KEY}")
        if res.status_code == 200:
            global_vars.data = json.loads(res.text)
            if not global_vars.data:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Try again:")
                return SEARCH
            await api_show.show_recipe(update, context)
            return CLICK
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error: {res.status_code}")
        return SEARCH

    async def search_for_description(self, update: Update, context: CallbackContext, call_index=global_vars.call_index) -> int:
        if global_vars.call_index < 0 or global_vars.call_index >= len(global_vars.data):
            recipe_id = global_vars.data[global_vars.call_index - 1]["id"]
        else:
            recipe_id = global_vars.data[global_vars.call_index]["id"]
        res = requests.get(f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions?apiKey={env.Keys.API_KEY}")
        if res.status_code == 200:
            recipe_summary = json.loads(res.text)
            for item in recipe_summary:
                for step in item["steps"]:
                    await context.bot.send_message(update.effective_chat.id, f"Step №{step['number']}: {step['step']}")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error: {res.status_code}")



recipy_api = GetRecipeAPI()