from typing import cast

from injector import Binder, Injector, Module, provider, singleton
from redis import Redis
from sqlalchemy import engine_from_config
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from base.adapters.event_publisher import RedisEventPublisher
from base.command_bus import CommandBus
from base.config import Settings, read_config
from base.event_bus import EventBus
from base.ports.event_publisher import EventPublisher


class BaseModule(Module):
    def __init__(self, config_path: str) -> None:
        self.config_path = config_path

    def configure(self, binder: Binder) -> None:
        binder.bind(EventPublisher, to=RedisEventPublisher)

    @singleton
    @provider
    def settings(self) -> Settings:
        return read_config(self.config_path)

    @singleton
    @provider
    def engine(self, settings: Settings) -> Engine:
        return engine_from_config(settings["alembic"])

    @singleton
    @provider
    def session(self, engine: Engine) -> Session:
        return cast(Session, scoped_session(sessionmaker(bind=engine)))

    @singleton
    @provider
    def redis(self, settings: Settings) -> Redis:
        return Redis(**settings["redis"])

    @provider
    def command_bus(self, container: Injector) -> CommandBus:
        return CommandBus(container)

    @provider
    def event_bus(self, container: Injector) -> EventBus:
        return EventBus(container)
