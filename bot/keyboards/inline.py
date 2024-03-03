from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def create_recipy_buttons() -> InlineKeyboardMarkup:
    first_row = [InlineKeyboardButton(text="Show another recipe", callback_data="another"),
                 InlineKeyboardButton(text="More about this one", callback_data="more")]
    second_row = [InlineKeyboardButton(text="Enter new ingredients", callback_data="new")]
    keyboard = [first_row, second_row]
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