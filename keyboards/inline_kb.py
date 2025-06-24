from aiogram.types import CallbackQuery
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
    db_get_orders_with_items_by_telegram,
    db_get_orders_count_by_telegram,
)
from utils.caption import format_order_history_text


def generate_category_menu(chat_id: int) -> InlineKeyboardMarkup:
    # Category buttons
    categories = db_get_all_category()
    builder = InlineKeyboardBuilder()
    total_price = db_get_total_price(chat_id)
    text = f"🛒 Your cart total: ${total_price if total_price else 0} "

    builder.button(text=text, callback_data="your_basket")
    for category in categories:
        builder.button(
            text=category.category_name, callback_data=f"category_{category.id}"
        )
    builder.adjust(1, 2)

    return builder.as_markup()


def show_product_by_category(category_id: int) -> InlineKeyboardMarkup:
    # Product buttons
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
            text="👈 Back",
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
            text="🛒 Add to cart",
            callback_data="put_into_cart",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="👈 Back",
            callback_data="back_to_products",
        )
    )

    return builder.as_markup()


def generate_basket_button(chat_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    cart_product = db_get_product_for_delete(chat_id)
    builder.row(
        InlineKeyboardButton(
            text="🚀 Proceed to payment",
            callback_data="order_pay",
        ),
    )

    for product_id, product_name, quantity in cart_product:
        builder.row(
            InlineKeyboardButton(
                text="➖",
                callback_data=f"decrease_{product_id}",
            ),
            InlineKeyboardButton(
                text=f"{product_name}",
                callback_data="noop",
            ),
            InlineKeyboardButton(
                text="➕",
                callback_data=f"increase_{product_id}",
            ),
        )
    builder.row(
        InlineKeyboardButton(
            text="👈 Back to shopping",
            callback_data="back_to_products",
        ),
    )
    return builder.as_markup()


ORDERS_PER_PAGE = 3


async def send_order_page(message_or_callback, tg_id: int, page: int):
    offset = (page - 1) * ORDERS_PER_PAGE
    orders = db_get_orders_with_items_by_telegram(tg_id, ORDERS_PER_PAGE, offset)
    total_orders = db_get_orders_count_by_telegram(tg_id)
    total_pages = (total_orders + ORDERS_PER_PAGE - 1) // ORDERS_PER_PAGE

    if not orders:
        await message_or_callback.answer("You don't have any orders yet.")
        return

    text = format_order_history_text(orders)

    buttons = []
    if page > 1:
        buttons.append(
            InlineKeyboardButton(text="⬅️ Back", callback_data=f"orders_page:{page - 1}")
        )
    if page < total_pages:
        buttons.append(
            InlineKeyboardButton(text="Next ➡️", callback_data=f"orders_page:{page + 1}")
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons] if buttons else [])

    if isinstance(message_or_callback, CallbackQuery):
        await message_or_callback.message.edit_text(text=text, reply_markup=keyboard)
        await message_or_callback.answer()
    else:
        await message_or_callback.answer(text=text, reply_markup=keyboard)
