from app.services import ReputationService


class GetHistoryHandler:
    def __init__(self, bot) -> None:
        service = ReputationService()

        @bot.message_handler(
            commands=["h", "history"],
            chat_types=["group", "supergroup"],
        )
        async def get_user_history(message):
            if not message.reply_to_message:
                return

            actor_id = message.from_user.id
            target_id = message.reply_to_message.from_user.id
            if actor_id == target_id:
                return

            history = await service.get_reduce_rep_history(target_id)
            if not history:
                await bot.reply_to(message, "❌ This user has not rep history!")
                return

            lines = [
                f"Reason: <b>{record.reason}</b>\nDate: <b>{record.date}</b>"
                for record in history
            ]
            payload = "\n\n".join(lines)
            await bot.reply_to(message, "🗃 Reducing rep history of user:\n\n" + payload)
