from dataclasses import dataclass

from cache.ports.repositories import TradingAssetCache
from trading_assets.domain.types import TradingAssetId
from trading_assets.ports.repositories import TradingAssetNotFound
from trading_assets.ports.uow import TradingAssetsUnitOfWork


@dataclass
class UpdateTradingAssetCacheService:
    _cache: TradingAssetCache
    _uow: TradingAssetsUnitOfWork

    def update(self, trading_asset_id: TradingAssetId):
        with self._uow as context:
            try:
                trading_asset = context.trading_assets.get(trading_asset_id)
            except TradingAssetNotFound:
                return

        self._cache.set(trading_asset)
