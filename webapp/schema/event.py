from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from conf.config import settings
from webapp.models.line_provider.event import EventStatusEnum


class EventCreate(BaseModel):
    name: str = Field(..., max_length=settings.NAME_MAX_LENGTH)
    status: EventStatusEnum
    deadline: datetime
    odds: Decimal = Field(..., gt=1)

    @model_validator(mode='after')
    def validate_odds(self) -> "EventCreate":
        if self.odds and len(str(self.odds).rsplit('.')[-1]) != 2:
            raise ValueError('Invalid odds format. Must be 2 decimal places')

        return self

    @model_validator(mode='after')
    def convert_deadline_to_utc(self) -> "EventCreate":
        if self.deadline:
            self.deadline = self.deadline.replace(tzinfo=None)

        return self


class EventUpdate(EventCreate):
    name: str | None = Field(None, max_length=settings.NAME_MAX_LENGTH)
    status: EventStatusEnum | None = None
    deadline: datetime | None = None
    odds: Decimal | None = Field(None, gt=1)


class EventResponse(EventCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ListEventResponse(BaseModel):
    count: int
    items: list[EventResponse]
