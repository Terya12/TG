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
    # Здесь можно проверить payload, например:
    if not pre_checkout_q.invoice_payload.startswith("order_"):
        await pre_checkout_q.answer(ok=False, error_message="Некорректный заказ.")
        return

    await pre_checkout_q.answer(ok=True)


@router.callback_query(F.data == "order_pay")
async def show_detail_payment(call: CallbackQuery):
    count, text, total_price, cart_id = basket_text(
        call.message.chat.id,
        "Итоговый список для оплаты",
    )
    text += "\n Доставка по городу 100грн"
    await call.message.delete()
    await call.message.answer_invoice(
        title="Оплата заказа",
        description=text,
        payload=f"order_{cart_id}_{call.from_user.id}",
        provider_token=settings.payment,
        currency=Currency.UAH,
        prices=[
            LabeledPrice(label="Товаров на сумму", amount=int(total_price * 100)),
            LabeledPrice(label="Стоимость доставки", amount=int(100 * 100)),
        ],
        start_parameter="time-to-pay",
    )


@router.message(F.successful_payment)
async def process_successful_payment(message: Message, bot: Bot):
    payment: SuccessfulPayment = message.successful_payment
    payload = payment.invoice_payload

    try:
        # Разбор payload — ожидаем "order_<basket_id>_<user_id>"
        parts = payload.split("_")
        if len(parts) != 3 or parts[0] != "order":
            raise ValueError("Неверный формат payload")

        cart_id = int(parts[1])
        user_id = int(parts[2])

        user = db_get_user_by_tg_id(user_id)
        if not user:
            raise ValueError(f"Пользователь с ID {user_id} не найден")

        # Получаем корзину и считаем итоговую сумму
        count, text, total_price, cart_id = basket_text(
            message.chat.id,
            "",
        )

        # Сохраняем заказ и получаем order_id
        order_id = db_save_order(user.id, total_price, cart_id)

        await bot.send_message(
            chat_id=settings.work_group,
            text=(
                f"✅ Получен новый заказ!\n"
                f"Пользователь: {user.name}\n"
                f"Телефон: {user.phone}\n"
                f"Заказ № {order_id}"
                f"{text}"
            ),
        )

        db_clear_basket(cart_id)

        await message.answer("Спасибо за оплату! Ваш заказ подтверждён ✅")

    except Exception as e:
        print(f"[Ошибка оплаты] {e}")
        await message.answer(
            "Произошла ошибка при обработке платежа. Мы уже разбираемся."
        )
