from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class UserRepHistory(Base):
    __tablename__ = "user_rep_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
