from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup


def share_phone_button() -> ReplyKeyboardMarkup:
    # Кнопка для отправки контакта
    builder = ReplyKeyboardBuilder()
    builder.button(text="Поделиться контактом 📲", request_contact=True)

    return builder.as_markup(resize_keyboard=True)
