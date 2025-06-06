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
