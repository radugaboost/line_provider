from fastapi import BackgroundTasks, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from webapp.api.event.router import default_router
from webapp.crud.event import EventRepository
from webapp.db.postgres import get_session
from webapp.rabbitmq.handlers.event import publish_event
from webapp.schema.event import EventCreate, EventResponse


@default_router.post('/event', status_code=HTTP_201_CREATED, response_model=EventResponse)
async def create_event_handler(
    body: EventCreate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    created_event = await EventRepository(session).create_event(body)
    if created_event is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST)

    response_model = EventResponse.model_validate(created_event)

    background_tasks.add_task(publish_event, response_model)

    return ORJSONResponse(content=response_model.model_dump(mode='json'), status_code=HTTP_201_CREATED)
