from typing import List

from injector import Binder, Module, multiprovider, provider

from base.command_bus import Handler
from base.event_bus import Listener
from base.ports.event_publisher import EventPublisher
from trading_assets.adapters.repositories import (
    PostgresTradingAssetCommandLogRepository,
    PostgresTradingAssetRepository,
)
from trading_assets.adapters.uow import PostgresTradingAssetsUnitOfWork
from trading_assets.command_handlers.add_trading_asset import AddTradingAssetHandler
from trading_assets.command_handlers.update_trading_asset import (
    UpdateTradingAssetHandler,
)
from trading_assets.commands import AddTradingAsset, UpdateTradingAsset
from trading_assets.events import (
    AddTradingAssetFailed,
    TradingAssetAdded,
    TradingAssetUpdated,
    UpdateTradingAssetFailed,
)
from trading_assets.listeners.add_trading_asset_failed import (
    LogAddTradingAssetFailedListener,
)
from trading_assets.listeners.trading_asset_added import LogTradingAssetAddedListener
from trading_assets.listeners.trading_asset_updated import (
    LogTradingAssetUpdatedListener,
)
from trading_assets.listeners.update_trading_asset_failed import (
    LogUpdateTradingAssetFailedListener,
)
from trading_assets.ports.repositories import (
    TradingAssetCommandLogRepository,
    TradingAssetRepository,
)
from trading_assets.ports.uow import TradingAssetsUnitOfWork


class TradingAssetsModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(
            TradingAssetCommandLogRepository,
            to=PostgresTradingAssetCommandLogRepository,
        )
        binder.bind(TradingAssetRepository, to=PostgresTradingAssetRepository)
        binder.bind(TradingAssetsUnitOfWork, to=PostgresTradingAssetsUnitOfWork)

    @provider
    def add_trading_asset_handler(
        self, uow: TradingAssetsUnitOfWork
    ) -> Handler[AddTradingAsset]:
        return AddTradingAssetHandler(uow)

    @provider
    def update_trading_asset_handler(
        self, uow: TradingAssetsUnitOfWork
    ) -> Handler[UpdateTradingAsset]:
        return UpdateTradingAssetHandler(uow)

    @multiprovider
    def log_trading_asset_added_listener(
        self, event_publisher: EventPublisher
    ) -> List[Listener[TradingAssetAdded]]:
        return [LogTradingAssetAddedListener(event_publisher)]

    @multiprovider
    def log_add_trading_asset_failed_listener(
        self, event_publisher: EventPublisher
    ) -> List[Listener[AddTradingAssetFailed]]:
        return [LogAddTradingAssetFailedListener(event_publisher)]

    @multiprovider
    def log_trading_asset_updated_listener(
        self, event_publisher: EventPublisher
    ) -> List[Listener[TradingAssetUpdated]]:
        return [LogTradingAssetUpdatedListener(event_publisher)]

    @multiprovider
    def log_update_trading_asset_failed_listener(
        self, event_publisher: EventPublisher
    ) -> List[Listener[UpdateTradingAssetFailed]]:
        return [LogUpdateTradingAssetFailedListener(event_publisher)]
