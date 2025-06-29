from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from db.db_utils import (
    db_get_product_by_id,
    db_get_user_cart,
    db_update_to_cart,
)
from keyboards.inline_kb import (
    show_product_by_category,
    generate_category_menu,
    add_to_cart,
    send_order_page,
)
from keyboards.reply_kb import share_phone_button
from utils.caption import text_for_caption

router = Router(name=__name__)


@router.callback_query(F.data.startswith("category_"))
async def show_product_button(call: CallbackQuery):
    # Display all products from the selected category
    category_id = int(call.data.split("_")[1])
    await call.message.edit_text(
        text="Choose a product",
        reply_markup=show_product_by_category(
            category_id,
        ),
    )


@router.callback_query(F.data.startswith("back_to_categories"))
# Return to category selection
async def back_to_categories(call: CallbackQuery):
    await call.message.edit_text(
        text="Choose a product",
        reply_markup=generate_category_menu(call.message.chat.id),
    )


@router.callback_query(F.data.startswith("product_"))
async def show_detail_product(call: CallbackQuery):
    # Display product details
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
            text="We need your contact information",
            reply_markup=share_phone_button(),
        )


@router.callback_query(F.data.startswith("back_to_products"))
async def back_to_products(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        text="Choose a product",
        reply_markup=generate_category_menu(call.message.chat.id),
    )


@router.callback_query(F.data.startswith("orders_page:"))
async def paginate_orders(callback: CallbackQuery):
    _, page_str = callback.data.split(":")
    page = int(page_str)
    await send_order_page(callback, callback.from_user.id, page)
