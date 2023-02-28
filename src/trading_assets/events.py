from dataclasses import dataclass

from trading_assets.domain.types import TradingAssetId


@dataclass(frozen=True)
class TradingAsset:
    command_id: str
    trading_asset_id: TradingAssetId


@dataclass(frozen=True)
class TradingAssetFailed:
    command_id: str
    trading_asset_id: TradingAssetId
    reason: str


# dataclass decorator is needed only when the child class
# has more attributes than the parent dataclass.
class TradingAssetAdded(TradingAsset):
    ...


class AddTradingAssetFailed(TradingAssetFailed):
    ...


class TradingAssetUpdated(TradingAsset):
    ...


class UpdateTradingAssetFailed(TradingAssetFailed):
    ...
