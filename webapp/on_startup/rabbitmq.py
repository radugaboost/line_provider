from aio_pika import ExchangeType, connect_robust

from conf.config import settings
from webapp.rabbitmq import base


async def start_rabbit() -> None:
    connection = await connect_robust(f'amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@rabbitmq/')
    base.channel = await connection.channel(publisher_confirms=False)
    base.exchange_lines = await base.channel.declare_exchange(settings.RABBITMQ_MAIN_EXCHANGE, ExchangeType.FANOUT)
