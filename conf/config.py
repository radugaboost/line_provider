from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BIND_HOST: str
    BIND_PORT: int

    SERVICE_NAME: str = 'line_provider'

    PG_DBNAME: str
    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: int

    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_MAIN_EXCHANGE: str

    LOG_LEVEL: str = 'debug'

    NAME_MAX_LENGTH: int = 128

    @property
    def db_url(self) -> str:
        return f'postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DBNAME}'


settings = Settings()
