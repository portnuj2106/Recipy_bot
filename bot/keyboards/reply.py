from telegram import ReplyKeyboardMarkup


def create_reply_buttons() -> ReplyKeyboardMarkup:
    reply_markup = ReplyKeyboardMarkup([['Set preferences'], ['Enter ingredients']], resize_keyboard=True,
                                       one_time_keyboard=False)
    return reply_markup


def create_admin_buttons() -> ReplyKeyboardMarkup:
    reply_markup = ReplyKeyboardMarkup([['Set preferences', 'Enter ingredients'], ['Admin panel']],
                                       resize_keyboard=True, one_time_keyboard=False)
    return reply_markup


def create_admin_panel_buttons() -> ReplyKeyboardMarkup:
    reply_markup = ReplyKeyboardMarkup([['Shit', 'Fuck'], ['Faggs']],
                                       resize_keyboard=True, one_time_keyboard=False)
    return reply_markup