from decimal import Decimal

from sqlalchemy import BigInteger, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class UserReps(Base):
    __tablename__ = "user_reps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True, index=True)
    reputation: Mapped[Decimal] = mapped_column(
        Numeric(4, 1),
        nullable=False,
        default=Decimal("10.0"),
    )
