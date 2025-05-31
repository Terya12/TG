from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from db.db_utils import (
    db_get_user_by_telegram,
    db_register_user,
    db_update_user,
    db_create_user_cart,
)
from keyboards.reply_kb import share_phone_button

router = Router(name=__name__)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Здравствуйте, <b>{message.from_user.full_name}</b>! \n"
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


@router.message(F.contact)
async def contact_handler(message: Message) -> None:
    # Обновление контакта
    chat_id = message.chat.id
    phone = message.contact.phone_number
    db_update_user(chat_id, phone)
    if db_create_user_cart(chat_id):
        await message.answer(text="Регистрация прошла успешно")
        # TODO Показать меню
