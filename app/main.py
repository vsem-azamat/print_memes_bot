import asyncio
from aiogram import types
from aiogram import Bot, Dispatcher

from config import settings
from app.handlers import router


async def set_default_commands(bot: Bot):
    await bot.set_my_commands([
        types.BotCommand("meme",  "Сделать мем"),
        types.BotCommand("helpmeme", "Инструкция")
    ])

async def on_startup(bot: Bot) -> None:
    await bot.delete_webhook()


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()
    await bot.session.close()


# Run bot
async def main() -> None:
    bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)
    await set_default_commands(bot)


if __name__ == "__main__":
    asyncio.run(main())
