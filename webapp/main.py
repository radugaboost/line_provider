from contextlib import asynccontextmanager
from logging import getLogger
from typing import AsyncIterator

from fastapi import FastAPI

from webapp.api.event.router import default_router
from webapp.on_startup.rabbitmq import start_rabbit

logger = getLogger(__name__)


def setup_routers(app: FastAPI) -> None:
    app.include_router(default_router)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await start_rabbit()
    logger.info('START APP')
    yield
    logger.info('END APP')


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)

    setup_routers(app)

    return app
