from dataclasses import dataclass

from trading_assets.domain.types import TradingAssetId


@dataclass(frozen=True)
class AddTradingAsset:
    id: str  # unique, uuid compliant
    trading_asset_id: TradingAssetId
    full_name: str
    iso_code: str
    tags: list[str]


@dataclass(frozen=True)
class UpdateTradingAsset:
    id: str  # unique, uuid compliant
    trading_asset_id: TradingAssetId
    full_name: str
    iso_code: str
    tags: list[str]
