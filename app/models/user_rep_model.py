from sqlalchemy import BigInteger, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class UserReps(Base):
    __tablename__ = "user_reps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True, index=True)
    reputation: Mapped[float] = mapped_column(Float, nullable=False, default=10.0)
