from aiogram import Router
from .orders import router as callback_order_router
from .basket import router as basket_router

router = Router(name=__name__)

router.include_routers(
    callback_order_router,
    basket_router,
)
