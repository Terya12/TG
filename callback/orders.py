from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from db.db_utils import db_get_all_category
from keyboards.inline_kb import show_product_by_category, generate_category_menu

router = Router(name=__name__)


@router.callback_query(F.data.startswith("category_"))
async def show_product_button(call: CallbackQuery):
    # Показ всех продуктов выбраной категории
    category_id = int(call.data.split("_")[1])
    # message_id = call.message.message_id
    await call.message.edit_text(
        text="Выберите продукт", reply_markup=show_product_by_category(category_id)
    )


@router.callback_query(F.data.startswith("back_to_categories"))
async def back_to_categories(call: CallbackQuery):
    await call.message.edit_text(
        text="Выберите продукт",
        reply_markup=generate_category_menu(),
    )
