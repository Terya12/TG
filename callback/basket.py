from itertools import product

from aiogram import Router, F
from aiogram.types import CallbackQuery

from db.db_utils import (
    db_get_user_cart,
    db_get_product_by_name,
    db_update_to_cart,
    db_insert_or_upd_finally_cart,
)
from handlers.users import show_main_menu
from keyboards.inline_kb import add_to_cart, generate_category_menu
from utils.caption import text_for_caption, basket_text

router = Router(name=__name__)


@router.callback_query(F.data.startswith("action"))
async def constructor_change(call: CallbackQuery):
    # Получение названия продукта из caption
    product_name = call.message.caption.split("\n")[0]

    # Получение данных из БД
    user_cart = db_get_user_cart(call.message.chat.id)
    product = db_get_product_by_name(product_name)

    if not product or not user_cart:
        await call.answer("Ошибка: товар не найден", show_alert=False)
        return

    action = call.data  # "action+" или "action-"
    quantity = user_cart.total_product

    if action == "action+":
        quantity += 1
        message_text = "✅ Продукт добавлен"
    elif action == "action-":
        if quantity <= 1:
            await call.answer("Меньше одного нельзя", show_alert=False)
            return
        quantity -= 1
        message_text = "🗑️ Продукт удалён"
    else:
        await call.answer("Неизвестное действие", show_alert=False)
        return

    # Обновление корзины
    total_price = product.price * quantity
    db_update_to_cart(
        price=total_price,
        quantity=quantity,
        cart_id=user_cart.id,
    )

    # Обновление сообщения
    new_text = text_for_caption(
        name=product.product_name,
        desc=product.description,
        price=total_price,
    )
    await call.message.edit_caption(
        caption=new_text,
        reply_markup=add_to_cart(user_cart.total_product),
    )

    # Уведомление пользователя
    await call.answer(
        message_text,
        show_alert=False,
    )


@router.callback_query(F.data == "quantity")
async def quantity(call: CallbackQuery):
    user_cart = db_get_user_cart(call.message.chat.id)
    quantity = user_cart.total_product
    await call.answer(f"{quantity}", show_alert=False)


@router.callback_query(F.data == "put_into_cart")
async def put_into_cart(call: CallbackQuery):
    # Добавление товаров в корзину
    product_name = call.message.caption.split("\n")[0]
    cart = db_get_user_cart(call.message.chat.id)

    await call.message.delete()

    if db_insert_or_upd_finally_cart(
        cart_id=cart.id,
        product_name=product_name,
        total_products=cart.total_product,
        total_price=cart.total_price,
    ):
        await call.message.answer(
            "✅ Продукт добавлен в корзину",
            reply_markup=generate_category_menu(call.message.chat.id),
        )
    else:
        await call.message.answer(
            "📝 Количество успешно обновлено",
            reply_markup=generate_category_menu(call.message.chat.id),
        )


@router.callback_query(F.data == "your_basket")
async def show_basket(call: CallbackQuery):
    """Показ корзины"""
    chat_id = call.message.chat.id
    context = basket_text(chat_id, "Ваша корзина")
    if context:
        count, text, *_ = context
        await call.message.answer(text=text)
    else:
        await call.message.answer(text="Ваша корзина пуста")
