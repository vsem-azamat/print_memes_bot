from aiogram import Router

from .memes import router as memes_router

router = Router()

router.include_router(memes_router)
