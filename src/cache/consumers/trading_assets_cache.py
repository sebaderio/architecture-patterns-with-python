import os
from dataclasses import dataclass

from base import bootstrap
from base.consumer import run_consumer
from cache.services.update_trading_asset import UpdateTradingAssetCacheService


@dataclass
class TradingAssetsCacheConsumer:
    _service: UpdateTradingAssetCacheService

    def __call__(self, event: dict):
        trading_asset_id = int(event["data"]["trading_asset_id"])
        self._service.update(trading_asset_id)


if __name__ == "__main__":
    config_path = os.environ["CONFIG_PATH"]
    container = bootstrap(config_path)
    service = container.get(UpdateTradingAssetCacheService)
    run_consumer(container, TradingAssetsCacheConsumer(service))
