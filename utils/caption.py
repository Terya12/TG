def text_for_caption(name, desc, price):
    text = (
        f"<b>{name}</b>\n\n"
        f"<b>Ингридиенты:</b> {desc}\n"
        f"<b>Цена:</b> {price} грн."
    )
    return text
