
from telegram.ext import (ConversationHandler, MessageHandler,
                          CommandHandler, filters, CallbackQueryHandler)
from bot.handlers.user_handlers.recipy_handlers import start, on_recipy_click, start_search
from bot.handlers.user_handlers.prefs_handlers import set_prefs, set_prefs_start, is_vegetarian, cooking_time, is_healthier
from bot.handlers.admin_handlers.admin_handlers import admin_panel_handler
from bot.handlers.user_handlers.registration_handlers import start_registration, save_nickname, save_email
from bot.handlers.user_handlers.favorite_handlers import next_recipe, show_favorite_recipes
from bot.handlers.admin_handlers.admin_handlers import view_users, delete_user
from bot.API.api_get import recipy_api
from bot.constants import *


async def register_handlers(application):
    registration_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & (filters.Regex(r'^Register me$')), start_registration)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_nickname)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_email)],
        },
        fallbacks=[],
    )

    recipy_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & (filters.Regex(r'^Enter ingredients$')), start_search)],
        states={
            SEARCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, recipy_api.search_for_recipes)],
            CLICK: [CallbackQueryHandler(on_recipy_click)]
        },
        fallbacks=[MessageHandler(filters.TEXT & (filters.Regex(r'^Set preferences$')), set_prefs)],
    )

    prefs_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & (filters.Regex(r'^Set preferences$')), set_prefs)],
        states={
            PREF_GREET: [MessageHandler(filters.TEXT & (filters.Regex(r'^Set preferences$')), set_prefs)],
            PREF_START: [CallbackQueryHandler(set_prefs_start)],
            VEGETARIAN: [CallbackQueryHandler(is_vegetarian)],
            COOKING: [CallbackQueryHandler(cooking_time)],
            HEALTHY: [CallbackQueryHandler(is_healthier)],
        },
        fallbacks=[],
    )

    fav_recipes_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & (filters.Regex(r'^Favorite recipes$')), show_favorite_recipes)],
        states={
            NEXT_RECIPE: [CallbackQueryHandler(next_recipe)]
        },
        fallbacks=[]
    )

    # Conversation handlers
    application.add_handler(registration_handler)
    application.add_handler(recipy_handler)
    application.add_handler(prefs_handler)
    application.add_handler(fav_recipes_handler)
    # Admin handlers
    application.add_handler(MessageHandler(filters.TEXT & (filters.Regex(r'^Admin panel$')), admin_panel_handler))
    application.add_handler(MessageHandler(filters.TEXT & (filters.Regex(r'^View registered users$')), view_users))
    application.add_handler(CallbackQueryHandler(delete_user))


    application.add_handler(CommandHandler(["start"], start))

