from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from bot.bd.bd import users_db


def create_recipy_buttons() -> InlineKeyboardMarkup:
    first_row = [InlineKeyboardButton(text="Show another recipe", callback_data="another"),
                 InlineKeyboardButton(text="More about this one", callback_data="more")]
    second_row = [InlineKeyboardButton(text="Enter new ingredients", callback_data="new")]
    keyboard = [first_row, second_row]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def auth_create_recipy_buttons() -> InlineKeyboardMarkup:
    first_row = [InlineKeyboardButton(text="Show another recipe", callback_data="another"),
                 InlineKeyboardButton(text="More about this one", callback_data="more")]
    second_row = [InlineKeyboardButton(text="Enter new ingredients", callback_data="new")]
    third_row = [InlineKeyboardButton(text="Add to favorites", callback_data="favorite")]
    keyboard = [first_row, second_row, third_row]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def enter_new_ingredients_buttons() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(text="Enter new ingredients", callback_data="new")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def create_prefs_buttons() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="Are you a vegetarian?", callback_data="isVegetarian")],
        [InlineKeyboardButton(text="Short cooking time is important to you?", callback_data="cookingTime")],
        [InlineKeyboardButton(text="Do you prefer healthier meals?", callback_data="isHealthy")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def yes_or_no_buttons() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="Yes", callback_data="yes"),
         InlineKeyboardButton(text="No", callback_data="no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


# def edit_user_buttons() -> InlineKeyboardMarkup:
#     for user in users_db.get_all_users():
#         keyboard = [[InlineKeyboardButton("Delete", callback_data=f"delete_{user['user_id']}")]]
#         reply_markup = InlineKeyboardMarkup(keyboard)
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     return reply_markup