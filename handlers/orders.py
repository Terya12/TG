from aiogram import Router, F
from aiogram.types import Message

from keyboards.inline_kb import (
    generate_category_menu,
    generate_basket_button,
    send_order_page,
)
from keyboards.reply_kb import back_to_main_menu, generate_main_menu
from utils.caption import basket_text

router = Router(name=__name__)


@router.message(F.text == "✅ Place an order")
async def make_order(message: Message) -> None:
    # Response to the "place order" button
    chat_id = message.chat.id

    await message.answer(
        text="Let's get started",
        reply_markup=back_to_main_menu(),
    )
    await message.answer(
        text="Choose a category",
        reply_markup=generate_category_menu(chat_id),
    )


@router.message(F.text == "Return to main menu")
async def back_to_menu(message: Message) -> None:
    await message.answer(text="Main menu", reply_markup=generate_main_menu())


@router.message(F.text == "🛒 Basket")
async def basket_show(message: Message) -> None:
    chat_id = message.chat.id
    context = basket_text(chat_id, "🛒 Your basket")
    if context:
        count, text, *_ = context
        await message.answer(
            text=text,
            reply_markup=generate_basket_button(chat_id),
        )
    else:
        await message.answer(
            text="Your basket is empty",
            reply_markup=generate_category_menu(chat_id),
        )


@router.message(F.text == "📖 Order history")
async def order_history_handler(message: Message) -> None:
    await send_order_page(message, message.from_user.id, page=1)
