import abc

from trading_assets.domain import aggregates
from trading_assets.domain.types import TradingAssetId


class TradingAssetCache(abc.ABC):
    @abc.abstractmethod
    def get(self, tradign_asset_id: TradingAssetId) -> aggregates.TradingAsset | None:
        ...

    @abc.abstractmethod
    def set(self, trading_asset: aggregates.TradingAsset):
        ...
