import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from starlette.middleware.sessions import SessionMiddleware


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
import uvicorn

from admin.admin_auth import AdminAuth
from config import settings
from filters import router as filters_router
from handlers import router as handlers_router
from callback import router as callback_router
from db.models import engine
from admin.admin_views import (
    UserAdmin,
    CartAdmin,
    FinallyCartAdmin,
    CategoryAdmin,
    ProductAdmin,
    OrderAdmin,
    OrderItemAdmin,
)


# === Bot Setup ===
TOKEN = settings.token
dp = Dispatcher()

dp.include_routers(
    filters_router,
    handlers_router,
    callback_router,
)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


# === FastAPI + SQLAdmin Setup ===
fastapi_app = FastAPI()
fastapi_app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
fastapi_app.mount("/media", StaticFiles(directory="media"), name="media")

admin_auth = AdminAuth()


admin = Admin(fastapi_app, engine, authentication_backend=admin_auth)
admin.add_view(UserAdmin)
admin.add_view(CartAdmin)
admin.add_view(FinallyCartAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(ProductAdmin)
admin.add_view(OrderAdmin)
admin.add_view(OrderItemAdmin)


async def start_bot():
    await dp.start_polling(bot)


async def start_fastapi():
    config = uvicorn.Config(
        app=fastapi_app, host="0.0.0.0", port=8000, log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await asyncio.gather(start_bot(), start_fastapi())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
