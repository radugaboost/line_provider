from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from conf.config import settings
from webapp.models.line_provider.base import BaseModel


class EventStatusEnum(Enum):
    WAITING: str = 'waiting'
    W1: str = 'W1'
    W2: str = 'W2'


class Event(BaseModel):
    __tablename__ = 'event'

    name: Mapped[str] = mapped_column(String(settings.NAME_MAX_LENGTH), nullable=False)
    status: Mapped[EventStatusEnum] = mapped_column(
        ENUM(EventStatusEnum, inherit_schema=True), default=EventStatusEnum.WAITING
    )
    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    odds: Mapped[Decimal] = mapped_column(Numeric(100, 2), nullable=False)
