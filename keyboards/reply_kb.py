from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup


def share_phone_button() -> ReplyKeyboardMarkup:
    # Button for sending contact
    builder = ReplyKeyboardBuilder()
    builder.button(
        text="Share contact 📲",
        request_contact=True,
    )

    return builder.as_markup(resize_keyboard=True)


def generate_main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="✅ Place an order")
    builder.button(text="📖 Order history")
    builder.button(text="🛒 Basket")
    builder.adjust(1, 2)

    return builder.as_markup(resize_keyboard=True)


def back_to_main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Return to main menu")

    return builder.as_markup(resize_keyboard=True)
