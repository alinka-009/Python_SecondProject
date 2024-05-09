from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from data.config import env
from loader import dp
from middlewares.add_update_user import add_update_User


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ["Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            '/get_id - получение вашего id']

    if str(message.from_user.id) in env.list('ADMINS') or str(message.from_user.id) in env.list('MAIN_ADMINS'):
        text.append('/create_post - создать новый пост')
        text.append('/delete_post - удалить пост')

    await add_update_User(message)
    await message.answer("\n".join(text), reply_markup=types.ReplyKeyboardRemove())
