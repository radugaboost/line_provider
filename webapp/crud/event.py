from datetime import datetime
from logging import getLogger
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from webapp.crud.base import Repository
from webapp.models.line_provider.event import Event
from webapp.schema.event import EventCreate, EventUpdate

logger = getLogger('event_repository')


class EventRepository(Repository):
    async def get_event_by_id(self, event_id: int) -> Event | None:
        return await self.session.get(Event, event_id)

    async def get_actual_events(self) -> Sequence[Event] | None:
        query = select(Event).where(Event.deadline > datetime.utcnow())

        result = (await self.session.scalars(query)).all()
        if not result:
            return None

        return result

    async def create_event(self, event_data: EventCreate) -> Event | None:
        event = Event(**event_data.model_dump())
        self.session.add(event)

        try:
            await self.session.commit()
        except IntegrityError as err:
            await self.session.rollback()
            logger.error(str(err))
            return None

        return event

    async def update_event(self, event: Event, event_data: EventUpdate) -> Event | None:
        for key, value in event_data.model_dump(exclude_unset=True).items():
            setattr(event, key, value)

        try:
            await self.session.commit()
        except IntegrityError as err:
            await self.session.rollback()
            logger.error(str(err))
            return None

        await self.session.refresh(event)
        return event
