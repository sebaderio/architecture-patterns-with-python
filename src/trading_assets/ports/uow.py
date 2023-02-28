import abc
from dataclasses import dataclass

from injector import inject

from trading_assets.ports import repositories


@inject
@dataclass
class TradingAssetsContext:
    command_log: repositories.TradingAssetCommandLogRepository
    trading_assets: repositories.TradingAssetRepository


class TradingAssetsUnitOfWork(abc.ABC):
    @abc.abstractmethod
    def __enter__(self) -> TradingAssetsContext:
        ...

    @abc.abstractmethod
    def _commit(self) -> None:
        ...

    @abc.abstractmethod
    def _rollback(self) -> None:
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self._rollback()
        else:
            self._commit()
