from injector import inject
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import trading_assets as models
from trading_assets.domain import entities
from trading_assets.ports import repositories


@inject
class PostgresTradingAssetCommandLogRepository(
    repositories.TradingAssetCommandLogRepository
):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, log: entities.TradingAssetCommandLog):
        existing_log = self.get(log.command_id)
        if existing_log.status != entities.CommandStatus.NEW:
            raise repositories.TradingAssetCommandLogAlreadyExists(log.command_id)

        log = models.PostgresTradingAssetCommandLog.from_entity(log)

        self._session.add(log)

    def get(self, command_id: str) -> entities.TradingAssetCommandLog:
        stmt = select(models.PostgresTradingAssetCommandLog).where(
            models.PostgresTradingAssetCommandLog.command_id == command_id
        )

        log: models.PostgresTradingAssetCommandLog | None = self._session.execute(
            stmt
        ).scalar_one_or_none()

        if log is None:
            return entities.TradingAssetCommandLog.get_new(command_id)

        return log.to_entity()
