import abc

from trading_assets.domain import aggregates
from trading_assets.domain.types import TradingAssetId


class TradingAssetAlreadyExists(Exception):
    def __init__(self, trading_asset_id: TradingAssetId) -> None:
        self._trading_asset_id = trading_asset_id

    def __str__(self) -> str:
        return f"Trading asset with id {self._trading_asset_id} already exists."


class TradingAssetNotFound(Exception):
    def __init__(self, trading_asset_id: TradingAssetId) -> None:
        self._trading_asset_id = trading_asset_id

    def __str__(self) -> str:
        return f"Trading asset with id {self._trading_asset_id} does not exist."


class TradingAssetRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, trading_asset: aggregates.TradingAsset):
        ...

    @abc.abstractmethod
    def get(self, trading_asset_id: TradingAssetId) -> aggregates.TradingAsset:
        ...

    @abc.abstractmethod
    def update(self, trading_asset: aggregates.TradingAsset):
        ...
