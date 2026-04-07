from app.core import settings
from app.services import ReputationService


class JoinedUserHandler:
    def __init__(self, bot) -> None:
        service = ReputationService()

        @bot.message_handler(content_types=["new_chat_members"])
        async def new_chat_member(message):
            for new in message.new_chat_members:
                user_id = new.id
                user = await service.get_user(user_id)

                if user is not None:
                    if user.reputation <= -10:
                        first_name = new.first_name or "-"
                        last_name = new.last_name or "-"
                        username = "@" + new.username if new.username else "-"
                        is_bot = new.is_bot

                        await bot.reply_to(
                            message,
                            settings.attention_text.format(
                                user.reputation,
                                first_name,
                                last_name,
                                username,
                                is_bot,
                                user_id,
                            ),
                        )
                    continue

                await service.ensure_user(user_id)
