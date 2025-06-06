from aiogram import Router, F
from aiogram.types import Message


from keyboards.inline_kb import generate_category_menu, generate_basket_button
from keyboards.reply_kb import back_to_main_menu, generate_main_menu
from utils.caption import basket_text

router = Router(name=__name__)


@router.message(F.text == "✅ Сделать заказ")
async def make_order(message: Message) -> None:
    # Реакция на кнопку сделать заказ
    chat_id = message.chat.id

    await message.answer(
        text="Давайте начнем",
        reply_markup=back_to_main_menu(),
    )
    await message.answer(
        text="Выберите категорию",
        reply_markup=generate_category_menu(chat_id),
    )


@router.message(F.text == "Вернуться в главное меню")
async def back_to_menu(message: Message) -> None:
    await message.answer(text="Главное меню", reply_markup=generate_main_menu())


@router.message(F.text == "🛒 Корзина")
async def basket_show(message: Message) -> None:
    chat_id = message.chat.id
    context = basket_text(chat_id, "Ваша корзина")
    if context:
        count, text, *_ = context
        await message.answer(
            text=text,
            reply_markup=generate_basket_button(chat_id),
        )
    else:
        await message.answer(
            text="Ваша корзина пуста",
            reply_markup=generate_category_menu(chat_id),
        )
