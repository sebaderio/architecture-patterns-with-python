import abc
from typing import NewType

from base.event_bus import Event

Channel = NewType("Channel", str)


class EventPublisher(abc.ABC):
    @abc.abstractmethod
    def publish(self, channel: Channel, event: Event) -> None:
        ...
