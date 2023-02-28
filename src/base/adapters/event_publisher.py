import json
from dataclasses import asdict, dataclass

from injector import inject
from redis import Redis

from base.event_bus import Event
from base.ports.event_publisher import Channel, EventPublisher


@inject
@dataclass
class RedisEventPublisher(EventPublisher):
    _publisher: Redis

    def publish(self, channel: Channel, event: Event) -> None:
        data = {"name": type(event).__name__, "data": asdict(event)}
        self._publisher.publish(channel, json.dumps(data))
