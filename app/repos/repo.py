from decimal import Decimal

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert as postgres_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

from app.db import SessionFactory
from app.models import UserRepHistory, UserReps


DEFAULT_REPUTATION = Decimal("10.0")
REPUTATION_STEP = Decimal("0.1")


class RepController:
    def __init__(self, session_factory=SessionFactory):
        self._session_factory = session_factory

    async def _insert_user_if_missing(self, session, user_id: int):
        payload = {"user_id": user_id, "reputation": DEFAULT_REPUTATION}
        dialect = session.get_bind().dialect.name

        if dialect == "postgresql":
            query = postgres_insert(UserReps).values(**payload)
            query = query.on_conflict_do_nothing(index_elements=[UserReps.user_id])
            await session.execute(query)
            return

        if dialect == "sqlite":
            query = sqlite_insert(UserReps).values(**payload)
            query = query.on_conflict_do_nothing(index_elements=[UserReps.user_id])
            await session.execute(query)
            return

        exists = await session.execute(
            select(UserReps.user_id).where(UserReps.user_id == user_id)
        )
        if exists.scalar_one_or_none() is None:
            session.add(UserReps(**payload))

    async def _get_user(self, session, user_id: int):
        result = await session.execute(
            select(UserReps).where(UserReps.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def _update_reputation(self, session, user_id: int, delta: Decimal):
        result = await session.execute(
            update(UserReps)
            .where(UserReps.user_id == user_id)
            .values(reputation=UserReps.reputation + delta)
            .returning(UserReps.reputation)
        )
        return result.scalar_one()

    async def add_new_user(self, user_id: int):
        async with self._session_factory() as session:
            await self._insert_user_if_missing(session, user_id)
            await session.commit()
            return await self._get_user(session, user_id)

    async def ensure_user(self, user_id: int):
        async with self._session_factory() as session:
            await self._insert_user_if_missing(session, user_id)
            await session.commit()

    async def get_user(self, user_id: int):
        async with self._session_factory() as session:
            return await self._get_user(session, user_id)

    async def get_rep(self, user_id: int):
        async with self._session_factory() as session:
            result = await session.execute(
                select(UserReps.reputation).where(UserReps.user_id == user_id)
            )
            return result.scalar_one_or_none()

    async def increase_rep(self, user_id: int, step: Decimal = REPUTATION_STEP):
        async with self._session_factory() as session:
            await self._insert_user_if_missing(session, user_id)
            reputation = await self._update_reputation(session, user_id, step)
            await session.commit()
            return reputation

    async def reduce_rep(
        self,
        user_id: int,
        reason: str = "-",
        step: Decimal = REPUTATION_STEP,
    ):
        async with self._session_factory() as session:
            await self._insert_user_if_missing(session, user_id)
            reputation = await self._update_reputation(session, user_id, -step)
            session.add(UserRepHistory(user_id=user_id, reason=reason or "-"))
            await session.commit()
            return reputation

    async def get_reduce_rep_history(self, user_id: int):
        async with self._session_factory() as session:
            result = await session.execute(
                select(UserRepHistory)
                .where(UserRepHistory.user_id == user_id)
                .order_by(UserRepHistory.date.desc(), UserRepHistory.id.desc())
            )
            return list(result.scalars().all())
