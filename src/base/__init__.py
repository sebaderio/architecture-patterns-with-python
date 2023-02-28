from injector import Injector

from base.module import BaseModule
from cache.module import CacheModule
from mailing.module import MailingModule
from trading_assets.module import TradingAssetsModule


def bootstrap(config_path: str) -> Injector:
    return Injector(
        modules=[
            BaseModule(config_path),
            CacheModule(),
            MailingModule(),
            TradingAssetsModule(),
        ]
    )
