import requests
import json
from telegram import Update
from telegram.ext import CallbackContext
import env

from ..constants import CLICK, SEARCH
from bot.global_vars import GlobalVars
from bot.global_vars import global_vars
from .api_show import api_show


class GetRecipeAPI(GlobalVars):
    async def search_for_recipes(self, update: Update, context: CallbackContext) -> int:
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

    async def search_for_description(self, update: Update, context: CallbackContext, index=global_vars.call_index,
                                     recipe_infos=global_vars.data) -> int:
        if index < 0 or index >= len(recipe_infos):
            index = max(0, min(index, len(recipe_infos) - 1))

        recipe_id = recipe_infos[index]["id"]
        res = requests.get(
            f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions?apiKey={env.Keys.API_KEY}")
        if res.status_code == 200:
            recipe_summary = json.loads(res.text)
            for item in recipe_summary:
                for step in item["steps"]:
                    await context.bot.send_message(update.effective_chat.id, f"Step №{step['number']}: {step['step']}")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error: {res.status_code}")


recipy_api = GetRecipeAPI()