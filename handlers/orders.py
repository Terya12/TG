from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.inline_kb import generate_category_menu
from keyboards.reply_kb import back_to_main_menu, generate_main_menu

router = Router(name=__name__)


@router.message(F.text == "✅ Сделать заказ")
async def make_order(message: Message) -> None:
    # Реакция на кнопку сделать заказ
    chat_id = message.chat.id
    # TODO Получить id корзины пользователя
    await message.answer(
        text="Давайте начнем",
        reply_markup=back_to_main_menu(),
    )
    await message.answer(
        text="Выберите категорию",
        reply_markup=generate_category_menu(),
    )


@router.message(F.text == "Вернуться в главное меню")
async def back_to_menu(message: Message) -> None:
    await message.answer(text="Главное меню", reply_markup=generate_main_menu())
