from aiogram import Router

from .users import router as user_router
from .users import start_register_user
from .orders import router as orders_router

router = Router(name=__name__)

router.include_routers(
    user_router,
    orders_router,
)
