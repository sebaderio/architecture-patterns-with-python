from typing import List

from injector import Binder, Module, multiprovider, provider

from base.event_bus import Listener
from base.ports.event_publisher import EventPublisher
from cache.adapters.repositories import RedisTradingAssetCache
from cache.listeners.trading_asset_added import CacheTradingAssetAddedListener
from cache.listeners.trading_asset_updated import CacheTradingAssetUpdatedListener
from cache.ports.repositories import TradingAssetCache
from cache.services.update_trading_asset import UpdateTradingAssetCacheService
from trading_assets.events import TradingAssetAdded, TradingAssetUpdated
from trading_assets.ports.uow import TradingAssetsUnitOfWork


class CacheModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(TradingAssetCache, to=RedisTradingAssetCache)

    @provider
    def update_trading_asset_cache_service(
        self, cache: TradingAssetCache, uow: TradingAssetsUnitOfWork
    ) -> UpdateTradingAssetCacheService:
        return UpdateTradingAssetCacheService(cache, uow)

    @multiprovider
    def cache_trading_asset_added_listener(
        self, event_publisher: EventPublisher
    ) -> List[Listener[TradingAssetAdded]]:
        return [CacheTradingAssetAddedListener(event_publisher)]

    @multiprovider
    def cache_trading_asset_updated_listener(
        self, event_publisher: EventPublisher
    ) -> List[Listener[TradingAssetUpdated]]:
        return [CacheTradingAssetUpdatedListener(event_publisher)]
