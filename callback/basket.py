from aiogram import Router, F
from aiogram.types import CallbackQuery

from db.db_utils import (
    db_get_user_cart,
    db_get_product_by_name,
    db_update_to_cart,
    db_insert_or_upd_finally_cart,
    db_delete_product_by_id,
    db_decrease_product_quantity,
    db_increase_product_quantity,
)
from keyboards.inline_kb import (
    add_to_cart,
    generate_category_menu,
    generate_basket_button,
)
from utils.caption import text_for_caption, basket_text

router = Router(name=__name__)


@router.callback_query(F.data.startswith("action"))
async def constructor_change(call: CallbackQuery):
    # Get product name from caption
    product_name = call.message.caption.split("\n")[0]

    # Fetch data from DB
    user_cart = db_get_user_cart(call.message.chat.id)
    product = db_get_product_by_name(product_name)

    if not product or not user_cart:
        await call.answer("Error: product not found", show_alert=False)
        return

    action = call.data  # "action+" or "action-"
    quantity = user_cart.total_product

    if action == "action+":
        quantity += 1
        message_text = "✅ Product added"
    elif action == "action-":
        if quantity <= 1:
            await call.answer("Cannot be less than one", show_alert=False)
            return
        quantity -= 1
        message_text = "🗑️ Product removed"
    else:
        await call.answer("Unknown action", show_alert=False)
        return

    # Update cart
    total_price = product.price * quantity
    db_update_to_cart(
        price=total_price,
        quantity=quantity,
        cart_id=user_cart.id,
    )

    # Update message
    new_text = text_for_caption(
        name=product.product_name,
        desc=product.description,
        price=total_price,
    )
    await call.message.edit_caption(
        caption=new_text,
        reply_markup=add_to_cart(user_cart.total_product),
    )

    # Notify user
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
    # Add products to cart
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
            "✅ Product added to cart",
            reply_markup=generate_category_menu(call.message.chat.id),
        )
    else:
        await call.message.answer(
            "📝 Quantity successfully updated",
            reply_markup=generate_category_menu(call.message.chat.id),
        )


@router.callback_query(F.data == "your_basket")
async def show_basket(call: CallbackQuery):
    """Display cart"""
    chat_id = call.message.chat.id
    context = basket_text(chat_id, " 🧺 Your cart")
    await call.message.delete()
    if context:
        count, text, *_ = context
        await call.message.answer(
            text=text,
            reply_markup=generate_basket_button(chat_id),
        )
    else:
        await call.message.answer(
            text="Your cart is empty 😔",
            reply_markup=generate_category_menu(chat_id),
        )


@router.callback_query(F.data.startswith("delete_"))
async def delete_cart_product(call: CallbackQuery):
    finally_id = int(call.data.split("_")[1])
    db_delete_product_by_id(finally_id)
    chat_id = call.message.chat.id

    await call.answer("🗑️ Product removed")
    await show_basket(call)


@router.callback_query(lambda c: c.data.startswith("increase_"))
async def increase_quantity(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    chat_id = callback.from_user.id
    db_increase_product_quantity(chat_id, product_id)

    context = basket_text(chat_id, " 🧺 Your cart")
    if context:
        count, text, *_ = context

        if count == 0:
            # If cart is empty, show empty cart message and menu
            await callback.message.edit_text(
                text="Your cart is empty 😔",
                reply_markup=generate_category_menu(chat_id),
            )
        else:
            # Update both text and keyboard
            await callback.answer(text="✅ Product added")
            await callback.message.edit_text(
                text=text,
                reply_markup=generate_basket_button(chat_id),
            )
    else:
        # If context is unexpectedly empty, show empty cart
        await callback.message.edit_text(
            text="Your cart is empty 😔",
            reply_markup=generate_category_menu(chat_id),
        )

    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("decrease_"))
async def decrease_quantity(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    chat_id = callback.from_user.id

    db_decrease_product_quantity(chat_id, product_id)

    context = basket_text(chat_id, " 🧺 Your cart")
    if context:
        count, text, *_ = context

        if count == 0:
            # If cart is empty, show empty cart message and menu
            await callback.message.edit_text(
                text="Your cart is empty 😔",
                reply_markup=generate_category_menu(chat_id),
            )
        else:
            # Update both text and keyboard
            await callback.answer(text="🗑️ Product removed")
            await callback.message.edit_text(
                text=text,
                reply_markup=generate_basket_button(chat_id),
            )
    else:
        # If context is unexpectedly empty, show empty cart
        await callback.message.edit_text(
            text="Your cart is empty 😔",
            reply_markup=generate_category_menu(chat_id),
        )

    await callback.answer()


@router.callback_query(lambda c: c.data == "noop")
async def noop_callback(callback: CallbackQuery):
    await callback.answer()  # just ignore, do nothing
