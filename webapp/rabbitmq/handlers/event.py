from aio_pika import Message
from orjson import dumps

from conf.config import settings
from webapp.rabbitmq.base import get_exchange_lines
from webapp.schema.event import EventResponse
from webapp.schema.rabbitmq.message import BaseMessage


async def publish_event(body: EventResponse) -> None:
    exchange_lines = get_exchange_lines()

    message = BaseMessage(
        author=settings.SERVICE_NAME,
        message=body.model_dump(),
    ).model_dump(mode='json')

    await exchange_lines.publish(Message(dumps(message), content_type='text/plain'), '')
