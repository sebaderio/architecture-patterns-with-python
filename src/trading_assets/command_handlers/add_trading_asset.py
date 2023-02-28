from dataclasses import dataclass

from base.command_bus import Handler
from trading_assets.commands import AddTradingAsset
from trading_assets.domain.aggregates import TradingAsset
from trading_assets.domain.entities import Tag
from trading_assets.events import AddTradingAssetFailed, TradingAssetAdded
from trading_assets.ports.repositories import TradingAssetAlreadyExists
from trading_assets.ports.uow import TradingAssetsUnitOfWork


@dataclass
class AddTradingAssetHandler(Handler[AddTradingAsset]):
    _uow: TradingAssetsUnitOfWork

    def __call__(self, command: AddTradingAsset) -> None:
        trading_asset = TradingAsset(
            id=command.trading_asset_id,
            full_name=command.full_name,
            iso_code=command.iso_code,
            tags=[Tag(name=tag) for tag in command.tags],
        )
        with self._uow as context:
            try:
                context.trading_assets.add(trading_asset)
            except TradingAssetAlreadyExists:
                event = AddTradingAssetFailed(
                    command_id=command.id,
                    trading_asset_id=command.trading_asset_id,
                    reason="Trading asset already exists.",
                )
            else:
                event = TradingAssetAdded(
                    command_id=command.id, trading_asset_id=command.trading_asset_id
                )
            context.events.append(event)
