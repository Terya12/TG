from aiogram import F, Router
from aiogram.types import Message

router = Router(name=__name__)


@router.message(F.photo)
async def photo_handler(message: Message) -> None:
    await message.answer(text="I can't see images. Please choose one of the options.")


@router.message(F.sticker)
async def sticker_handler(message: Message) -> None:
    await message.reply(text="Nice sticker")


@router.message(F.text)
async def text_handler(message: Message) -> None:
    await message.answer(text="Select one of the options")
