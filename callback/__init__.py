from aiogram import Router
from .orders import router as callback_order_router

router = Router(name=__name__)

router.include_routers(callback_order_router)
