from aiogram import Router, F, Bot
from aiogram.enums import Currency
from aiogram.types import CallbackQuery, LabeledPrice
from aiogram.types import Message, SuccessfulPayment, PreCheckoutQuery

from config import settings
from db.db_utils import (
    db_get_user_by_tg_id,
    db_clear_basket,
    db_save_order,
)
from utils.caption import basket_text

router = Router()


@router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_q: PreCheckoutQuery, bot: Bot):
    # Here you can validate the payload
    if not pre_checkout_q.invoice_payload.startswith("order_"):
        await pre_checkout_q.answer(ok=False, error_message="Invalid order.")
        return

    await pre_checkout_q.answer(ok=True)


@router.callback_query(F.data == "order_pay")
async def show_detail_payment(call: CallbackQuery):
    count, text, total_price, cart_id = basket_text(
        call.message.chat.id,
        "Final order summary for payment",
    )
    delivery_cost = 5  # например 50 грн
    text += f"\nDelivery within the city: ${delivery_cost}"

    await call.message.delete()

    # Отправляем полный текст отдельным сообщением (чтобы переносы сохранились)
    await call.message.answer(text)

    # Отправляем инвойс с кратким описанием (без переносов)
    await call.message.answer_invoice(
        title="Order payment",
        description="Please confirm your order and pay.",
        payload=f"order_{cart_id}_{call.from_user.id}",
        provider_token=settings.payment,
        currency="UAH",
        prices=[
            LabeledPrice(label="Total for products", amount=int(total_price * 100)),
            LabeledPrice(label="Delivery cost", amount=int(delivery_cost * 100)),
        ],
        start_parameter="time-to-pay",
    )


@router.message(F.successful_payment)
async def process_successful_payment(message: Message, bot: Bot):
    payment: SuccessfulPayment = message.successful_payment
    payload = payment.invoice_payload

    try:
        # Parse payload — expected format: "order_<basket_id>_<user_id>"
        parts = payload.split("_")
        if len(parts) != 3 or parts[0] != "order":
            raise ValueError("Invalid payload format")

        cart_id = int(parts[1])
        user_id = int(parts[2])

        user = db_get_user_by_tg_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        # Get cart and calculate total
        count, text, total_price, cart_id = basket_text(
            message.chat.id,
            "",
        )

        # Save the order and get the order ID
        order_id = db_save_order(user.id, total_price, cart_id)

        await bot.send_message(
            chat_id=settings.work_group,
            text=(
                f"✅ New order received!\n"
                f"User: {user.name}\n"
                f"Phone: {user.phone}\n"
                f"Order № {order_id}"
                f"{text}"
            ),
        )

        db_clear_basket(cart_id)

        await message.answer(
            "Thank you for your payment! Your order has been confirmed ✅"
        )

    except Exception as e:
        print(f"[Payment error] {e}")
        await message.answer(
            "An error occurred while processing the payment. We’re already looking into it."
        )
