import abc

from trading_assets.domain import entities


class TradingAssetCommandLogAlreadyExists(Exception):
    def __init__(self, command_id: str) -> None:
        self._command_id = command_id

    def __str__(self) -> str:
        return f"Trading asset command log with id {self._command_id} already exists."


class TradingAssetCommandLogRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, log: entities.TradingAssetCommandLog):
        ...

    @abc.abstractmethod
    def get(self, command_id: str) -> entities.TradingAssetCommandLog:
        ...
