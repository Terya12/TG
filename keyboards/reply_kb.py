from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup


def share_phone_button() -> ReplyKeyboardMarkup:
    # кнопка для отправки контакта
    builder = ReplyKeyboardBuilder()
    builder.button(
        text="поделиться контактом 📲",
        request_contact=True,
    )

    return builder.as_markup(resize_keyboard=True)


def generate_main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="✅ Сделать заказ")
    builder.button(text="📖 История заказов")
    builder.button(text="🛒 Корзина")
    builder.adjust(1, 2)

    return builder.as_markup(resize_keyboard=True)


def back_to_main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Вернуться в главное меню")

    return builder.as_markup(resize_keyboard=True)
