from dataclasses import dataclass

from base.event_bus import Listener
from base.ports.event_publisher import EventPublisher
from trading_assets.events import TradingAssetUpdated


@dataclass
class LogTradingAssetUpdatedListener(Listener[TradingAssetUpdated]):
    CHANNEL_NAME = "trading_assets_commands_log"
    _event_publisher: EventPublisher

    def __call__(self, event: TradingAssetUpdated) -> None:
        self._event_publisher.publish(self.CHANNEL_NAME, event)
