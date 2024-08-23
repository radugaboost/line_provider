from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from webapp.api.event.router import default_router
from webapp.crud.event import EventRepository
from webapp.db.postgres import get_session
from webapp.schema.event import EventResponse, ListEventResponse


@default_router.get('/event/{event_id}', response_model=EventResponse)
async def get_event_handler(
    event_id: int,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    event = await EventRepository(session).get_event_by_id(event_id)
    if event is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Event not found')

    return ORJSONResponse(content=EventResponse.model_validate(event).model_dump(mode='json'), status_code=HTTP_200_OK)


@default_router.get('/events', response_model=ListEventResponse)
async def get_actual_events_handler(
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    events = await EventRepository(session).get_actual_events()
    if events is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Events not found')

    return ORJSONResponse(
        content=ListEventResponse(count=len(events), items=events).model_dump(mode='json'), status_code=HTTP_200_OK
    )
