from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from injector import Injector

Command = TypeVar("Command")


class Handler(Generic[Command]):
    def __call__(self, command: Command) -> None:
        raise NotImplementedError


@dataclass
class CommandBus:
    _container: Injector

    def handle(self, command: Command) -> None:
        command_cls: Type[Command] = type(command)
        handler = self._container.get(Handler[command_cls])
        handler(command)
