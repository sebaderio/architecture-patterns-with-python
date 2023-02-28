from dataclasses import dataclass

from base.command_bus import Handler
from trading_assets.commands import UpdateTradingAsset
from trading_assets.domain.aggregates import TradingAsset
from trading_assets.domain.entities import Tag
from trading_assets.events import TradingAssetUpdated, UpdateTradingAssetFailed
from trading_assets.ports.repositories import TradingAssetNotFound
from trading_assets.ports.uow import TradingAssetsUnitOfWork


@dataclass
class UpdateTradingAssetHandler(Handler[UpdateTradingAsset]):
    _uow: TradingAssetsUnitOfWork

    def __call__(self, command: UpdateTradingAsset) -> None:
        trading_asset = TradingAsset(
            id=command.trading_asset_id,
            full_name=command.full_name,
            iso_code=command.iso_code,
            tags=[Tag(name=tag) for tag in command.tags],
        )
        with self._uow as context:
            try:
                context.trading_assets.update(trading_asset)
            except TradingAssetNotFound:
                event = UpdateTradingAssetFailed(
                    command_id=command.id,
                    trading_asset_id=command.trading_asset_id,
                    reason="Trading asset not found.",
                )
            else:
                event = TradingAssetUpdated(
                    command_id=command.id, trading_asset_id=command.trading_asset_id
                )
            context.events.append(event)
