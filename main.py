import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from filters import router as filters_router
from handlers import router as handlers_router
from callback import router as callback_router


TOKEN = settings.token
dp = Dispatcher()

dp.include_routers(
    filters_router,
    handlers_router,
    callback_router,
)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
