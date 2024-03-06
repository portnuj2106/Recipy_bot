from telegram import ReplyKeyboardMarkup


def create_reply_buttons() -> ReplyKeyboardMarkup:
    reply_markup = ReplyKeyboardMarkup([['Set preferences', 'Enter ingredients'], ['Register me']], resize_keyboard=True,
                                       one_time_keyboard=False)
    return reply_markup


def auth_create_reply_buttons() -> ReplyKeyboardMarkup:
    reply_markup = ReplyKeyboardMarkup([['Set preferences', 'Enter ingredients'], ['Register me', 'Favorite recipes']], resize_keyboard=True,
                                       one_time_keyboard=False)
    return reply_markup


def create_admin_buttons() -> ReplyKeyboardMarkup:
    reply_markup = ReplyKeyboardMarkup([['Set preferences', 'Enter ingredients'], ['Admin panel', 'Register me']],
                                       resize_keyboard=True, one_time_keyboard=False)
    return reply_markup


def create_admin_panel_buttons() -> ReplyKeyboardMarkup:
    reply_markup = ReplyKeyboardMarkup([['View registered users', 'Favorite recipes'], ['Faggs']],
                                       resize_keyboard=True, one_time_keyboard=False)
    return reply_markup