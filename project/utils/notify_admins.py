import logging

from aiogram import Dispatcher

from data.config import ADMINS, MAIN_ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in MAIN_ADMINS:
        if admin != '':
            try:
                await dp.bot.send_message(admin, "Бот Запущен")
            except Exception as err:
                logging.exception(err)
