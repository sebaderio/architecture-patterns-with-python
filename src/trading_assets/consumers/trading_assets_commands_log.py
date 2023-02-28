import os
from dataclasses import dataclass

from base import bootstrap
from base.consumer import run_consumer
from trading_assets.domain.entities import CommandStatus, TradingAssetCommandLog
from trading_assets.events import (
    AddTradingAssetFailed,
    TradingAssetAdded,
    TradingAssetUpdated,
    UpdateTradingAssetFailed,
)
from trading_assets.ports.repositories import TradingAssetCommandLogAlreadyExists
from trading_assets.ports.uow import TradingAssetsUnitOfWork


@dataclass
class TradingAssetsCommandsLogConsumer:
    _uow: TradingAssetsUnitOfWork

    def __call__(self, event: dict):
        event_name = event["name"]
        event_data = event["data"]
        log = TradingAssetCommandLog(
            command_id=event_data["command_id"],
            reason=event_data.get("reason"),
            status=self._get_status_for_event_name(event_name),
        )
        with self._uow as context:
            try:
                context.command_log.add(log)
            except TradingAssetCommandLogAlreadyExists:
                pass

    @staticmethod
    def _get_status_for_event_name(name: str) -> CommandStatus:
        success_events_names = [
            TradingAssetAdded.__name__,
            TradingAssetUpdated.__name__,
        ]
        failed_events_names = [
            AddTradingAssetFailed.__name__,
            UpdateTradingAssetFailed.__name__,
        ]
        if name in success_events_names:
            return CommandStatus.SUCCESS
        if name in failed_events_names:
            return CommandStatus.FAILED
        raise NotImplementedError


if __name__ == "__main__":
    config_path = os.environ["CONFIG_PATH"]
    container = bootstrap(config_path)
    uow = container.get(TradingAssetsUnitOfWork)
    run_consumer(container, TradingAssetsCommandsLogConsumer(uow))
