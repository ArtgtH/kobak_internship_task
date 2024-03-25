"""
Здесь лежат кнопки для Бота
"""


import aiogram
from aiogram import types
from aiogram.types import WebAppInfo


def inline_kb_1(username):
    params = {
        "username": username,
    }

    url = "***********" + "?" + "&".join(f'{key}={value}' for key, value in params.items())

    buttons_1 = [[
        types.InlineKeyboardButton(text="Вызвать web-форму", web_app=WebAppInfo(url=url))
    ]]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons_1, row_width=1)

buttons_2 = [[
    types.InlineKeyboardButton(text="/send_keyboard")
]]
inline_kb2 = types.InlineKeyboardMarkup(inline_keyboard=buttons_2)

buttons_3 = [[
    types.KeyboardButton(text="/send_form")
]]
keyboard_1 = types.ReplyKeyboardMarkup(keyboard=buttons_3)