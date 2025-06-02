from aiogram import F, Router
from aiogram.types import Message

from keyboards.reply_kb import generate_main_menu

router = Router(name=__name__)


@router.message(F.photo)
async def photo_handler(message: Message) -> None:
    await message.answer(
        text="Я не вижу картинок. Пожалуйста выберите один из вариантов"
    )
