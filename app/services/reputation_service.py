from dataclasses import dataclass
from decimal import Decimal
import logging

from app.repos import RepController


logger = logging.getLogger(__name__)


@dataclass(slots=True)
class CommandResult:
    action: str | None
    reputation: Decimal | None = None


class ReputationService:
    rep_up = {"+rep", "+реп", "+r", "+р"}
    rep_down = {"-rep", "-реп", "-r", "-р"}
    info = {"!rep", "!реп", "!r", "!р", "!info"}

    def __init__(self, repo: RepController | None = None):
        self.repo = repo or RepController()

    @staticmethod
    def split_command(message_text: str) -> tuple[str, str]:
        normalized = (message_text or "").strip()
        if not normalized:
            return "", "-"

        chunks = normalized.split(maxsplit=1)
        command = chunks[0].lower()
        reason = chunks[1].strip() if len(chunks) > 1 else "-"
        return command, reason or "-"

    async def ensure_user(self, user_id: int) -> None:
        await self.repo.ensure_user(user_id)

    async def get_user(self, user_id: int):
        return await self.repo.get_user(user_id)

    async def process_reply_command(
        self,
        actor_id: int,
        target_id: int,
        message_text: str,
        min_rep_for_reduce: Decimal = Decimal("15.0"),
    ) -> CommandResult:
        await self.ensure_user(actor_id)
        await self.ensure_user(target_id)

        command, reason = self.split_command(message_text)

        if command in self.rep_up:
            reputation = await self.repo.increase_rep(target_id)
            logger.debug("Reputation increased user_id=%s new_rep=%s", target_id, reputation)
            return CommandResult(action="increase", reputation=reputation)

        if command in self.rep_down:
            actor_rep = await self.repo.get_rep(actor_id)
            if actor_rep is not None and actor_rep >= min_rep_for_reduce:
                reputation = await self.repo.reduce_rep(target_id, reason=reason)
                logger.debug(
                    "Reputation reduced user_id=%s actor_id=%s reason=%s new_rep=%s",
                    target_id,
                    actor_id,
                    reason,
                    reputation,
                )
                return CommandResult(action="reduce", reputation=reputation)
            return CommandResult(action=None)

        if command in self.info:
            reputation = await self.repo.get_rep(target_id)
            return CommandResult(action="info", reputation=reputation)

        return CommandResult(action=None)

    async def process_self_info_command(self, actor_id: int, message_text: str) -> CommandResult:
        await self.ensure_user(actor_id)
        command, _ = self.split_command(message_text)

        if command not in self.info:
            return CommandResult(action=None)

        reputation = await self.repo.get_rep(actor_id)
        return CommandResult(action="self_info", reputation=reputation)

    async def get_reduce_rep_history(self, user_id: int):
        return await self.repo.get_reduce_rep_history(user_id)
