import asyncio
import time

from aiogram import executor

from data.data_base import db_session
from loader import dp
import middlewares
import handlers
from middlewares.send_messages import send_messages
from data.data_base.users import User
from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    await on_startup_notify(dispatcher)


def repeat(coro, lp):
    asyncio.ensure_future(coro(), loop=lp)
    loop.call_later(5, repeat, coro, lp)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_later(2, repeat, send_messages, loop)
    db_session.global_init("data/data_base.db")

    session = db_session.create_session()

    executor.start_polling(dp, skip_updates=True, loop=loop, on_startup=on_startup)
