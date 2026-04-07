import logging

from telebot.async_telebot import ExceptionHandler


logger = logging.getLogger(__name__)


class BotExceptionHandler(ExceptionHandler):
    async def handle(self, exception):
        logger.error(
            "Unhandled bot exception",
            exc_info=(type(exception), exception, exception.__traceback__),
        )
        return True
