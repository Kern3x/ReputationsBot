from sqlalchemy import select

from app.db import SessionFactory
from app.models import UserRepHistory, UserReps


class RepController:
    def __init__(self, session_factory=SessionFactory):
        self._session_factory = session_factory

    async def _get_user(self, session, user_id: int, lock_for_update: bool = False):
        query = select(UserReps).where(UserReps.user_id == user_id)
        if lock_for_update:
            query = query.with_for_update()

        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def add_new_user(self, user_id: int):
        async with self._session_factory() as session:
            user = await self._get_user(session, user_id)
            if user is not None:
                return user

            user = UserReps(user_id=user_id, reputation=10.0)
            session.add(user)
            await session.commit()
            return user

    async def ensure_user(self, user_id: int):
        return await self.add_new_user(user_id)

    async def get_user(self, user_id: int):
        async with self._session_factory() as session:
            return await self._get_user(session, user_id)

    async def get_rep(self, user_id: int):
        user = await self.get_user(user_id)
        if user is None:
            return None
        return user.reputation

    async def increase_rep(self, user_id: int, step: float = 0.1):
        async with self._session_factory() as session:
            user = await self._get_user(session, user_id, lock_for_update=True)
            if user is None:
                user = UserReps(user_id=user_id, reputation=10.0)
                session.add(user)

            user.reputation = round(float(user.reputation) + step, 1)
            await session.commit()
            return user.reputation

    async def reduce_rep(self, user_id: int, reason: str = "-", step: float = 0.1):
        async with self._session_factory() as session:
            user = await self._get_user(session, user_id, lock_for_update=True)
            if user is None:
                user = UserReps(user_id=user_id, reputation=10.0)
                session.add(user)

            user.reputation = round(float(user.reputation) - step, 1)
            session.add(UserRepHistory(user_id=user_id, reason=reason or "-"))
            await session.commit()
            return user.reputation

    async def get_reduce_rep_history(self, user_id: int):
        async with self._session_factory() as session:
            result = await session.execute(
                select(UserRepHistory)
                .where(UserRepHistory.user_id == user_id)
                .order_by(UserRepHistory.date.desc(), UserRepHistory.id.desc())
            )
            return list(result.scalars().all())
