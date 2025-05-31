import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.inline_kb import *
from keyboards.reply_kb import *
from db.db_utils import *
from config import settings


TOKEN = settings.token

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Здравствуйте, {html.bold(message.from_user.full_name)}! \n"
        f"Вас приветствует бот по заказу еды."
    )
    await start_register_user(message)


async def start_register_user(message: Message) -> None:
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    user = db_get_user_by_telegram(chat_id)

    if not user:
        if db_register_user(chat_id, full_name):
            await message.answer("Вы успешно зарегистрированы.")
        else:
            await message.answer("Произошла ошибка при регистрации.")
        user = db_get_user_by_telegram(chat_id)  # обновляем после регистрации

    if user.phone:
        await message.answer("Приветствуем в нашем магазине вкусной еды! 🥙")
        # TODO: показать меню
    else:
        await message.answer(
            text="Для связи с Вами нам нужен Ваш контактный номер ☎️",
            reply_markup=share_phone_button(),
        )


@dp.message(F.text)
async def text_handler(message: Message) -> None:
    await message.answer(text="Не понимаю. Пожалуйста выберите один из вариантов")


@dp.message(F.photo)
async def text_handler(message: Message) -> None:
    await message.answer(
        text="Я не вижу картинок. Пожалуйста выберите один из вариантов"
    )


@dp.message(F.contact)
async def contact_handler(message: Message) -> None:
    # Обновление контакта
    chat_id = message.chat.id
    phone = message.contact.phone_number
    db_update_user(chat_id, phone)
    if db_create_user_cart(chat_id):
        await message.answer(text="Регистрация прошла успешно")
        # TODO Показать меню


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
