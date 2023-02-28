from smtplib import SMTP
from typing import List

from injector import Binder, Module, multiprovider, provider

from base.config import Settings
from base.event_bus import Listener
from base.ports.event_publisher import EventPublisher
from mailing.adapters.notifications import SMTPEmailNotification
from mailing.listeners.trading_asset_added import (
    NotifyCustomerCareTradingAssetAddedListener,
)
from mailing.ports.notifications import EmailNotification
from trading_assets.events import TradingAssetAdded


class MailingModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(EmailNotification, to=SMTPEmailNotification)

    @provider
    def smtp_server(self, settings: Settings) -> SMTP:
        return SMTP(**settings["mailing"])

    @multiprovider
    def notify_customer_care_trading_asset_added_listener(
        self, event_publisher: EventPublisher
    ) -> List[Listener[TradingAssetAdded]]:
        return [NotifyCustomerCareTradingAssetAddedListener(event_publisher)]
