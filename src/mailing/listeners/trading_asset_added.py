from dataclasses import dataclass

from base.event_bus import Listener
from base.ports.event_publisher import EventPublisher
from trading_assets.events import TradingAssetAdded


@dataclass
class NotifyCustomerCareTradingAssetAddedListener(Listener[TradingAssetAdded]):
    CHANNEL_NAME = "customer_care_notifications"
    _event_publisher: EventPublisher

    def __call__(self, event: TradingAssetAdded) -> None:
        self._event_publisher.publish(self.CHANNEL_NAME, event)
