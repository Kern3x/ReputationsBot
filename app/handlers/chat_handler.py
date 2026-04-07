from app.core import settings
from app.services import ReputationService


class MessageHandler:
    def __init__(self, bot) -> None:
        service = ReputationService()

        @bot.message_handler(content_types=["text"], chat_types=["group", "supergroup"])
        async def messages(message):
            actor_id = message.from_user.id
            message_text = message.text or ""
            command, _ = service.split_command(message_text)
            response_text = None

            if message.reply_to_message:
                if command not in service.rep_up | service.rep_down | service.info:
                    return

                target_id = message.reply_to_message.from_user.id
                if actor_id == target_id or settings.bot_id == target_id:
                    return

                first_name = message.reply_to_message.from_user.first_name or "Unknown"

                result = await service.process_reply_command(
                    actor_id=actor_id,
                    target_id=target_id,
                    message_text=message_text,
                )

                if result.action == "increase":
                    response_text = (
                        f"📈 Reputation for <b>{first_name}</b>, has been increased!"
                    )
                elif result.action == "reduce":
                    response_text = (
                        f"📉 Reputation for <b>{first_name}</b>, has been reduced!"
                    )
                elif result.action == "info" and result.reputation is not None:
                    response_text = (
                        f"📊 Reputation of <b>{first_name}</b>: {result.reputation:.1f}🌟"
                    )
            else:
                if command not in service.info:
                    return

                result = await service.process_self_info_command(actor_id, message_text)
                if result.action == "self_info" and result.reputation is not None:
                    response_text = f"📊 Your reputation: {result.reputation:.1f}🌟"

            if response_text:
                await bot.reply_to(message, response_text)
