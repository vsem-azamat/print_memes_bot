import asyncio
from aiogram import types
from aiogram import Bot, Dispatcher

from config import settings
from app.handlers import router


async def set_default_commands(bot: Bot):
    await bot.set_my_commands([
        types.BotCommand("старт",  "Старт"),
        types.BotCommand("хелп", "Инструкция")
    ])

async def on_startup(bot: Bot) -> None:
    await bot.delete_webhook()


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()
    await bot.session.close()


# Run bot
async def main() -> None:
    bot = Bot(token=settings.bot_token.get_secret_value(), parse_mode="HTML")
    dp = Dispatcher()

    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)
    await set_default_commands(bot)


if __name__ == "__main__":
    asyncio.run(main())