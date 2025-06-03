from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile


from db.db_utils import (
    db_get_all_category,
    db_get_product_by_id,
    db_get_user_cart,
    db_update_to_cart,
    db_get_product_by_name,
)
from keyboards.inline_kb import (
    show_product_by_category,
    generate_category_menu,
    add_to_cart,
)
from keyboards.reply_kb import share_phone_button
from utils.caption import text_for_caption

router = Router(name=__name__)


@router.callback_query(F.data.startswith("category_"))
async def show_product_button(call: CallbackQuery):
    # Показ всех продуктов выбраной категории
    category_id = int(call.data.split("_")[1])
    # message_id = call.message.message_id
    await call.message.edit_text(
        text="Выберите продукт",
        reply_markup=show_product_by_category(
            category_id,
        ),
    )


@router.callback_query(F.data.startswith("back_to_categories"))
# Возврат к выбору категории
async def back_to_categories(call: CallbackQuery):
    await call.message.edit_text(
        text="Выберите продукт",
        reply_markup=generate_category_menu(),
    )


@router.callback_query(F.data.startswith("product_"))
async def show_detail_product(call: CallbackQuery):
    # Показ продукта
    chat_id = call.message.chat.id
    product_id = int(call.data.split("_")[1])
    product = db_get_product_by_id(product_id)
    await call.message.delete()
    if user_cart := db_get_user_cart(chat_id):
        db_update_to_cart(
            price=product.price,
            cart_id=user_cart.id,
        )
        text = text_for_caption(
            name=product.product_name,
            desc=product.description,
            price=product.price,
        )
        await call.message.answer_photo(
            photo=FSInputFile(path=product.image),
            caption=text,
            reply_markup=add_to_cart(),
        )
    else:
        await call.message.answer(
            text="Нам нужен ваш контакт для связи",
            reply_markup=share_phone_button(),
        )


@router.callback_query(F.data.startswith("back_to_products"))
async def back_to_products(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        text="Выберите продукт",
        reply_markup=generate_category_menu(),
    )


@router.callback_query(F.data.startswith("action"))
async def constructor_change(call: CallbackQuery):
    # Получение названия продукта из caption
    product_name = call.message.caption.split("\n")[0]

    # Получение данных из БД
    user_cart = db_get_user_cart(call.message.chat.id)
    product = db_get_product_by_name(product_name)

    if not product or not user_cart:
        await call.answer("Ошибка: товар не найден", show_alert=True)
        return

    action = call.data  # "action+" или "action-"
    quantity = user_cart.total_product

    if action == "action+":
        quantity += 1
        message_text = "✅ Продукт добавлен"
    elif action == "action-":
        if quantity <= 1:
            await call.answer("Меньше одного нельзя", show_alert=True)
            return
        quantity -= 1
        message_text = "🗑️ Продукт удалён"
    else:
        await call.answer("Неизвестное действие", show_alert=True)
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
