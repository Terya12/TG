from aiogram import F, Router
from aiogram.types import Message

router = Router(name=__name__)


@router.message(F.text)
async def text_handler(message: Message) -> None:
    await message.answer(text="Не понимаю. Пожалуйста выберите один из вариантов")


@router.message(F.photo)
async def photo_handler(message: Message) -> None:
    await message.answer(
        text="Я не вижу картинок. Пожалуйста выберите один из вариантов"
    )
