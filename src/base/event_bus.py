from dataclasses import dataclass
from typing import Generic, List, Type, TypeVar

from injector import Injector

Event = TypeVar("Event")


class Listener(Generic[Event]):
    def __call__(self, event: Event) -> None:
        raise NotImplementedError


@dataclass
class EventBus:
    _container: Injector

    def handle(self, event: Event) -> None:
        event_cls: Type[Event] = type(event)
        listeners = self._container.get(List[Listener[event_cls]])
        for listener in listeners:
            listener(event)
