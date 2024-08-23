from fastapi import BackgroundTasks, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from webapp.api.event.router import default_router
from webapp.crud.event import EventRepository
from webapp.db.postgres import get_session
from webapp.rabbitmq.handlers.event import publish_event
from webapp.schema.event import EventResponse, EventUpdate


@default_router.put('/event/{event_id}', response_model=EventResponse)
async def update_event_handler(
    event_id: int,
    body: EventUpdate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    event_repo = EventRepository(session)

    event = await event_repo.get_event_by_id(event_id)
    if event is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Event not found')

    updated_event = await event_repo.update_event(event, body)
    if updated_event is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST)

    response_model = EventResponse.model_validate(updated_event)

    background_tasks.add_task(publish_event, response_model)

    return ORJSONResponse(content=response_model.model_dump(mode='json'), status_code=HTTP_200_OK)
