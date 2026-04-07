import logging

from telebot.async_telebot import AsyncTeleBot

from app.core import BotExceptionHandler, configure_logging, settings
from app.db import init_database
from app.handlers import GetHistoryHandler, JoinedUserHandler, MessageHandler


configure_logging(settings.log_level)
logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self) -> None:
        if not settings.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment")

        self.bot = AsyncTeleBot(
            settings.bot_token,
            exception_handler=BotExceptionHandler(),
        )
        self.bot.parse_mode = "html"

        GetHistoryHandler(self.bot)
        MessageHandler(self.bot)
        JoinedUserHandler(self.bot)
        logger.info("Bot handlers are registered")

    async def start(self):
        logger.info("Checking database connection")
        await init_database()
        logger.info("Bot polling started")
        await self.bot.infinity_polling(skip_pending=True)
