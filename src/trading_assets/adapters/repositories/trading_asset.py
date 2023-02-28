from injector import inject
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import trading_assets as models
from trading_assets.domain import aggregates, entities
from trading_assets.domain.types import TradingAssetId
from trading_assets.ports import repositories


@inject
class PostgresTradingAssetRepository(repositories.TradingAssetRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, trading_asset: aggregates.TradingAsset):
        if trading_asset.id is not None:
            try:
                self.get(trading_asset.id)
            except repositories.TradingAssetNotFound:
                pass
            else:
                raise repositories.TradingAssetAlreadyExists(trading_asset.id)

        trading_asset.tags = self._update_tags(trading_asset.tags)
        trading_asset = models.PostgresTradingAsset.from_aggregate(trading_asset)

        self._session.merge(trading_asset)

    def get(self, trading_asset_id: TradingAssetId) -> aggregates.TradingAsset:
        stmt = select(models.PostgresTradingAsset).where(
            models.PostgresTradingAsset.id == trading_asset_id
        )

        trading_asset: models.PostgresTradingAsset | None = self._session.execute(
            stmt
        ).scalar_one_or_none()

        if trading_asset is None:
            raise repositories.TradingAssetNotFound(trading_asset_id)

        return trading_asset.to_aggregate()

    def update(self, trading_asset: aggregates.TradingAsset):
        self.get(trading_asset.id)
        trading_asset.tags = self._update_tags(trading_asset.tags)
        trading_asset = models.PostgresTradingAsset.from_aggregate(trading_asset)

        self._session.merge(trading_asset)

    def _update_tags(self, tags: list[entities.Tag]) -> list[entities.Tag]:
        if tags:
            stmt = select(models.PostgresTag).where(
                models.PostgresTag.name.in_([tag.name for tag in tags])
            )
            tag_models = self._session.execute(stmt).scalars()
            existing_tags = [tag.to_entity() for tag in tag_models]
            existing_tags_names = [tag.name for tag in existing_tags]
            missing_tags = [tag for tag in tags if tag.name not in existing_tags_names]

            if missing_tags:
                return existing_tags + self._add_tags(missing_tags)
            return existing_tags
        return tags

    def _add_tags(self, tags: list[entities.Tag]) -> list[entities.Tag]:
        tags = [models.PostgresTag.from_entity(tag) for tag in tags]

        self._session.add_all(tags)
        self._session.flush()

        return [tag.to_entity() for tag in tags]
