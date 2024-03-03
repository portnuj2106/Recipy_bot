import requests
import json
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
import env
from ..constants import CLICK, SEARCH
from bot.global_vars import GlobalVars
from bot.global_vars import global_vars, preferences
from bot.keyboards.inline import create_recipy_buttons, enter_new_ingredients_buttons


class APIPreferences(GlobalVars):
    async def get_recipes_info(self, update: Update, context: CallbackContext):
        recipe_infos = []
        for recipe in global_vars.data:
            res = requests.get(f'https://api.spoonacular.com/recipes/{recipe['id']}/information?apiKey={env.Keys.API_KEY}&includeNutrition=false')
            if res.status_code == 200:
                recipe_data = json.loads(res.text)
                recipe_infos.append(recipe_data)
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error: {res.status_code}")
        if preferences.isVegetarian and not preferences.cookingTime:
            await api_preferences.filter_vegetarian_recipes(update, context, recipe_infos)
        elif preferences.cookingTime and not preferences.isVegetarian:
            await api_preferences.sort_by_cooking_time(update, context, recipe_infos)
        elif preferences.cookingTime and preferences.isVegetarian:
            await api_preferences.show_sorted_vegetarian(update, context, recipe_infos)


    async def filter_vegetarian_recipes(self, update: Update, context: CallbackContext, recipe_infos):
        if recipe_infos:
            vegetarian_recipes = []
            for recipe in recipe_infos:
                if recipe["vegetarian"]:
                    vegetarian_recipes.append(recipe)
            num_vegetarian_recipes = len(vegetarian_recipes)
        if num_vegetarian_recipes > 0:
            if global_vars.call_index == 0:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Found {num_vegetarian_recipes} vegetarian recipes:")
            else:
                pass
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Sorry, no vegetarian recipes were found with given ingredients",
                                           reply_markup=enter_new_ingredients_buttons())
            return ConversationHandler.END
        if preferences.isVegetarian and not preferences.cookingTime:
            await api_preferences.vegetarian_ids(update, context, vegetarian_recipes)
        elif preferences.isVegetarian and preferences.cookingTime:
            return vegetarian_recipes


    async def vegetarian_ids(self, update: Update, context: CallbackContext, vegetarian_recipes):
        seen_ids = {}
        for item in vegetarian_recipes:
            seen_ids[item['id']] = True
        await api_preferences.show_vegetarian_recipe(update, context, seen_ids)

    async def show_vegetarian_recipe(self, update: Update, context: CallbackContext, seen_ids):
        if global_vars.call_index >= len(seen_ids):
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="==============That's all vegetarian recipes available=============",
                                           reply_markup=enter_new_ingredients_buttons())
            return CLICK
        for item in global_vars.data:
            if item["id"] in seen_ids:
                await context.bot.send_message(update.effective_chat.id,
                                               f"{global_vars.data[global_vars.call_index]['title']}")
                await context.bot.send_photo(update.effective_chat.id,
                                             f"{global_vars.data[global_vars.call_index]['image']}",
                                             reply_markup=create_recipy_buttons())
                global_vars.call_index += 1
        return CLICK

    async def sort_by_cooking_time(self, update: Update, context: CallbackContext, recipe_infos):
        sorted_recipe_infos = sorted(recipe_infos, key=lambda x: x["readyInMinutes"])
        data_dict = {}
        if preferences.cookingTime and not preferences.isVegetarian:
            for recipe, data in zip(recipe_infos, global_vars.data):
                data_dict[recipe["id"]] = data
            await api_preferences.show_sorted_by_cookingtime(update, context, sorted_recipe_infos, data_dict)

    async def show_sorted_by_cookingtime(self, update: Update, context: CallbackContext, sorted_recipe_infos, data_dict):
        if global_vars.call_index >= len(sorted_recipe_infos):
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="==============That's all vegetarian recipes available=============",
                                           reply_markup=enter_new_ingredients_buttons())
            return CLICK
        if preferences.cookingTime and not preferences.isVegetarian:
            recipe_id = sorted_recipe_infos[global_vars.call_index]["id"]
            data = data_dict.get(recipe_id)
            await context.bot.send_message(update.effective_chat.id, f"Cooking time: {sorted_recipe_infos[global_vars.call_index]["readyInMinutes"]} minutes")
            await context.bot.send_message(update.effective_chat.id, f"{data['title']}")
            await context.bot.send_photo(update.effective_chat.id, f"{data['image']}",
                                             reply_markup=create_recipy_buttons())
            global_vars.call_index += 1
            return CLICK

    async def show_sorted_vegetarian(self, update: Update, context: CallbackContext, recipe_infos):
        vegetarian_recipes = await api_preferences.filter_vegetarian_recipes(update, context, recipe_infos)
        sorted_vegetarian_infos = sorted(vegetarian_recipes, key=lambda x: x["readyInMinutes"])
        seen_ids = {}
        for item in sorted_vegetarian_infos:
            seen_ids[item['id']] = True
        if global_vars.call_index >= len(seen_ids):
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="==============That's all vegetarian recipes available=============",
                                           reply_markup=enter_new_ingredients_buttons())
            return CLICK
        for item in global_vars.data:
            if item["id"] in seen_ids:
                await context.bot.send_message(update.effective_chat.id,
                                               f"Cooking time: {sorted_vegetarian_infos[global_vars.call_index]['readyInMinutes']} minutes")
                await context.bot.send_message(update.effective_chat.id,
                                               f"{global_vars.data[global_vars.call_index]['title']}")
                await context.bot.send_photo(update.effective_chat.id,
                                             f"{global_vars.data[global_vars.call_index]['image']}",
                                             reply_markup=create_recipy_buttons())
                global_vars.call_index += 1
        return CLICK


api_preferences = APIPreferences()