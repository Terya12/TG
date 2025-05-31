from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from db.db_utils import db_get_all_category


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
