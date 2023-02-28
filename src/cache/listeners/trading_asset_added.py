from dataclasses import dataclass

from base.event_bus import Listener
from base.ports.event_publisher import EventPublisher
from trading_assets.events import TradingAssetAdded


@dataclass
class CacheTradingAssetAddedListener(Listener[TradingAssetAdded]):
    CHANNEL_NAME = "trading_assets_cache"
    _event_publisher: EventPublisher

    def __call__(self, event: TradingAssetAdded) -> None:
        self._event_publisher.publish(self.CHANNEL_NAME, event)
