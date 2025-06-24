from typing import List

from db import Order
from db.db_utils import db_get_cart_products


def text_for_caption(name, desc, price):
    text = (
        f"<b>{name}</b>\n\n" f"<b>Ingredients:</b> {desc}\n" f"<b>Price:</b> {price} $"
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
            text += f"{count}. {name}\n Quantity: {quantity}\n Cost: ${price}\n\n"

        text += (
            f"Total number of products: {total_products}\n"
            f"Total cost: ${total_price}\n"
        )
        context = (count, text, total_price, cart_id)
        return context
    return None


def format_order_history_text(orders: List[Order]) -> str:
    if not orders:
        return "You don't have any orders yet."

    lines = ["📜 Order history:\n"]
    for order in orders:
        lines.append(
            f"<b>Order №</b>{order.id} | Date: {order.created_at.strftime('%Y-%m-%d %H:%M')}"
        )
        lines.append(f"Total: ${order.total_price} ")
        lines.append("Items:")
        for item in order.items:
            lines.append(
                f"  - {item.product_name} x{item.quantity} at ${item.price}  each"
            )
        lines.append("")  # empty line between orders

    return "\n".join(lines)
