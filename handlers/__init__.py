from aiogram import Router

from .users import router as user_router
from .users import start_register_user

router = Router(name=__name__)

router.include_router(user_router)
