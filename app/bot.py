from telebot.async_telebot import AsyncTeleBot

from app.core import settings
from app.db import init_database
from app.handlers import GetHistoryHandler, JoinedUserHandler, MessageHandler


class TelegramBot:
    def __init__(self) -> None:
        if not settings.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment")

        self.bot = AsyncTeleBot(settings.bot_token)
        self.bot.parse_mode = "html"

        GetHistoryHandler(self.bot)
        MessageHandler(self.bot)
        JoinedUserHandler(self.bot)

    async def start(self):
        await init_database()
        await self.bot.infinity_polling(skip_pending=True)
