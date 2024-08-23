from aio_pika.abc import AbstractChannel, AbstractExchange

channel: AbstractChannel
exchange_lines: AbstractExchange


def get_exchange_lines() -> AbstractExchange:
    global exchange_lines

    return exchange_lines


def get_channel() -> AbstractChannel:
    global channel

    return channel
