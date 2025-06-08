from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from db.db_utils import (
    db_get_all_category,
    db_get_products,
    db_get_total_price,
    db_get_product_for_delete,
)


def generate_category_menu(chat_id: int) -> InlineKeyboardMarkup:
    # Кнопки категорий
    categories = db_get_all_category()
    builder = InlineKeyboardBuilder()
    total_price = db_get_total_price(chat_id)
    text = f"🛒 Ваша корзина на сумму {total_price if total_price else 0} грн."

    builder.button(text=text, callback_data="your_basket")
    for category in categories:
        builder.button(
            text=category.category_name, callback_data=f"category_{category.id}"
        )
    builder.adjust(1, 2)

    return builder.as_markup()


def show_product_by_category(category_id: int) -> InlineKeyboardMarkup:
    # Кнопки продуктов
    products = db_get_products(category_id)
    builder = InlineKeyboardBuilder()
    for product in products:
        builder.button(
            text=product.product_name,
            callback_data=f"product_{product.id}",
        )
    builder.adjust(2)
    builder.row(
        InlineKeyboardButton(
            text="👈 Вернуться назад",
            callback_data="back_to_categories",
        )
    )
    return builder.as_markup()


def add_to_cart(quantity=1) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="➖", callback_data="action-")
    builder.button(text=str(quantity), callback_data="quantity")
    builder.button(text="➕", callback_data="action+")
    builder.row(
        InlineKeyboardButton(
            text="🛒 Добавить в корзину",
            callback_data="put_into_cart",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="👈 Назад",
            callback_data="back_to_products",
        )
    )

    return builder.as_markup()


def generate_basket_button(chat_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    cart_product = db_get_product_for_delete(chat_id)
    builder.button(text="🚀 Оформить заказ", callback_data="order_pay")
    for finally_cart_id, product_name in cart_product:
        builder.button(
            text=f"❌Удалить: {product_name}",
            callback_data=f"delete_{finally_cart_id}",
        )
    builder.button(text="👈 Назад к покупкам", callback_data="back_to_products")
    builder.adjust(1)
    return builder.as_markup()
