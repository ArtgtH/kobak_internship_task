"""
Здесь лежит функционал бота
"""


import asyncio
import logging
import time
from datetime import datetime as dt
import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from user.user_class import User

from bot_parts.config import token
from db.connection_preparedata import check_person_in_staff_db

from bot_parts.buttons import keyboard_1, inline_kb_1


bot = Bot(token=token)
logging.basicConfig(level=logging.INFO)
dp = Dispatcher()


def seconds_till_friday():
    """
    Функция, которая вычисляет количество секунд до следующей пятницы
    return: количество секунд до следующей пятницы
    """
    now = datetime.datetime.now()

    # now = '2024-01-19 15:00:01'
    # now = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')

    hours = now.strftime('%H')
    minutes = now.strftime('%M')
    seconds = now.strftime('%S')
    days = now.weekday()
    time_format = '%H'

    if days == 4 and int(hours) == 15 and int(minutes) == 00 and int(seconds) == 00:
        next_friday = now + datetime.timedelta(days=7)
    else:
        days_to_friday = (4 - days + 7) % 7
        if int(hours) >= 15:
            if days_to_friday == 0:
                days_to_friday += 6
            else:
                days_to_friday -= 1

        delta_time = ((datetime.datetime.strptime('15', time_format) -
                      datetime.timedelta(hours=float(hours), minutes=float(minutes), seconds=float(seconds))).
                      strftime('%H:%M:%S'))

        hours, minutes, seconds = delta_time.split(':')

        next_friday = now + datetime.timedelta(days=days_to_friday, hours=int(hours), minutes=int(minutes),
                                               seconds=int(seconds))

    time_until_friday = (next_friday - now).total_seconds()

    return time_until_friday



@dp.message(Command("start"))
async def send_message(message: types.Message) -> None:
    """
    Реакция на первое сообщение пользователя (команда start)
    Создает объект класса User
    :param message: сообщение от пользователя
    """

    chat_id = message.chat.id
    user_id = message.from_user.id
    user = User(chat_id, user_id)

    await message.answer("Привет я бот, который будет проверять время работы")
    # await aioschedule.every().minute().do(start_procedure, message, user)
    loop = asyncio.get_event_loop()

    loop.create_task(start_procedure(message, user))

    # async def job():
    #     current_date = dt.now()
    #     current_day = current_date.weekday()
    #     current_time = current_date.time()
    #
    #     if current_day == 4 and current_time.hour == 18 and current_time.minute == 0:
    #         await start_procedure(message, user)
    #
    # schedule.every().friday.at("18:00").do(job)


async def start_procedure(message, user_class) -> None:
    """
    Функция, которая отправляет пользователю сообщение с каким-то фиксированным периодом
    :param message: стартовое сообщение
    :param user_class: объект класса User
    """

    while True:
        sleep_in_seconds = seconds_till_friday()
        chat_member = await bot.get_chat_member(chat_id=user_class.get_chat(), user_id=user_class.get_user())
        username = chat_member.user.username

        await asyncio.sleep(sleep_in_seconds)
        if check_person_in_staff_db("@" + username):
            await message.answer(text="Еженедельная проверка часов", reply_markup=keyboard_1)


@dp.message(Command("send_form"))
async def send_web_form(message: types.Message) -> None:
    """
    Функция для отправки ссылки на форму пользователю, обрабатывает команду send_form
    :param message:
    """
    inline_kb1 = inline_kb_1(message.from_user.username)

    await message.reply(text="высылаю форму", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text="переход на веб-форму", reply_markup=inline_kb1)


if __name__ == "__main__":
    dp.run_polling(bot)
