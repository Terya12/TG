from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from db.db_utils import db_get_all_category, db_get_products


def generate_category_menu() -> InlineKeyboardMarkup:
    # Кнопки категорий
    categories = db_get_all_category()
    builder = InlineKeyboardBuilder()
    # TODO Общая сумма корзины

    builder.button(text=f"Ваша корзина (TODO сум)", callback_data="Ваша корзина")
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
            callback_data="add_to_cart",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="👈 Назад",
            callback_data="back_to_products",
        )
    )

    return builder.as_markup()
