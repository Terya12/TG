from typing import List

from db import Order
from db.db_utils import db_get_cart_products


def text_for_caption(name, desc, price):
    text = (
        f"<b>{name}</b>\n\n"
        f"<b>Ингридиенты:</b> {desc}\n"
        f"<b>Цена:</b> {price} грн."
    )
    return text


def basket_text(chat_id, user_text):
    products = db_get_cart_products(chat_id)
    if products:
        text = f"{user_text}\n\n"
        total_products = total_price = count = 0
        for name, quantity, price, cart_id in products:
            count += 1
            total_products += quantity
            total_price += price
            text += f"{count}. {name}\n Количество: {quantity}\n Стоимость: {price}\n\n"

        text += (
            f"Общее кол-во продуктов: {total_products}\n"
            f"Общая стоимость: {total_price}\n"
        )
        context = (count, text, total_price, cart_id)
        return context
    return None


def format_order_history_text(orders: List[Order]) -> str:
    if not orders:
        return "У вас пока нет заказов."

    lines = ["📜 История заказов:\n"]
    for order in orders:
        lines.append(
            f"<b>Заказ №</b>{order.id} | Дата: {order.created_at.strftime('%Y-%m-%d %H:%M')}"
        )
        lines.append(f"Итого: {order.total_price} грн.")
        lines.append("Товары:")
        for item in order.items:
            lines.append(
                f"  - {item.product_name} x{item.quantity} по {item.price} грн."
            )
        lines.append("")  # пустая строка между заказами

    return "\n".join(lines)
