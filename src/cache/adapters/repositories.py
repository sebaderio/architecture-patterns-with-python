from typing import Optional

from injector import inject
from pydantic.error_wrappers import ValidationError
from redis import Redis

from cache.ports import repositories
from trading_assets.domain import aggregates
from trading_assets.domain.types import TradingAssetId


@inject
class RedisTradingAssetCache(repositories.TradingAssetCache):
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    def get(self, trading_asset_id: TradingAssetId) -> aggregates.TradingAsset | None:
        key = f"{aggregates.TradingAsset.__name__}_{trading_asset_id}"
        raw_data: Optional[bytes] = self._redis.get(key)
        if not raw_data:
            return None
        try:
            return aggregates.TradingAsset.parse_raw(raw_data)
        except ValidationError:
            return None

    def set(self, trading_asset: aggregates.TradingAsset):
        data = trading_asset.json()
        self._redis.set(f"{type(trading_asset).__name__}_{trading_asset.id}", data)
