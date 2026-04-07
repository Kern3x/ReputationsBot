import asyncio

from app.bot import TelegramBot
from app.db import dispose_database


async def main():
    bot = TelegramBot()
    try:
        await bot.start()
    finally:
        await dispose_database()


if __name__ == "__main__":
    asyncio.run(main())
