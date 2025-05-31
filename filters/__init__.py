from aiogram import Router
from .filters import router as filters_router

router = Router(name=__name__)

router.include_routers(filters_router)
