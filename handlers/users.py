from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from db.db_utils import (
    db_get_user_by_telegram,
    db_register_user,
    db_update_user,
    db_create_user_cart,
)
from keyboards.reply_kb import share_phone_button, generate_main_menu

router = Router(name=__name__)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Hello, <b>{message.from_user.full_name}</b>! \n"
        f"Welcome to the food ordering bot."
    )
    await start_register_user(message)


async def start_register_user(message: Message) -> None:
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    user = db_get_user_by_telegram(chat_id)

    if not user:
        if db_register_user(chat_id, full_name):
            await message.answer("You have successfully registered.")
        else:
            await message.answer("An error occurred during registration.")
        user = db_get_user_by_telegram(chat_id)  # refresh after registration

    if user.phone:
        await message.answer(
            "Welcome to our delicious food shop! 🥙",
            reply_markup=generate_main_menu(),
        )
    else:
        await message.answer(
            text="We need your contact number to reach you ☎️",
            reply_markup=share_phone_button(),
        )


@router.message(F.contact)
async def contact_handler(message: Message) -> None:
    # Update user's contact
    chat_id = message.chat.id
    phone = message.contact.phone_number
    db_update_user(chat_id, phone)
    if db_create_user_cart(chat_id):
        await message.answer(
            text="Registration completed successfully",
            reply_markup=generate_main_menu(),
        )


async def show_main_menu(message: Message) -> None:
    # Make order, History, Basket, Settings
    await message.answer(text="Choose an option", reply_markup=generate_main_menu())
