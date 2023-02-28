from typing import Self

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from database.models.base import Base
from trading_assets.domain import aggregates, entities

PostgresTradingAssetTags = Table(
    "trading_asset_tags",
    Base.metadata,
    Column("trading_asset_id", ForeignKey("trading_assets.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class PostgresTradingAsset(Base):
    __tablename__ = "trading_assets"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(255), nullable=False)
    iso_code = Column(String(255), nullable=False)
    tags = relationship(
        "PostgresTag", secondary=PostgresTradingAssetTags, backref="trading_asset"
    )

    @classmethod
    def from_aggregate(cls, trading_asset: aggregates.TradingAsset) -> Self:
        tags = [PostgresTag.from_entity(tag) for tag in trading_asset.tags]

        return cls(
            id=trading_asset.id,
            full_name=trading_asset.full_name,
            iso_code=trading_asset.iso_code,
            tags=tags,
        )

    def to_aggregate(self) -> aggregates.TradingAsset:
        tags = [tag.to_entity() for tag in self.tags]

        return aggregates.TradingAsset(
            id=self.id,
            full_name=self.full_name,
            iso_code=self.iso_code,
            tags=tags,
        )


class PostgresTag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    trading_assets = relationship(
        "PostgresTradingAsset", secondary=PostgresTradingAssetTags, backref="tag"
    )

    @classmethod
    def from_entity(cls, tag: entities.Tag) -> Self:
        return cls(
            id=tag.id,
            name=tag.name,
        )

    def to_entity(self) -> entities.Tag:
        return entities.Tag(
            id=self.id,
            name=self.name,
        )


class PostgresTradingAssetCommandLog(Base):
    __tablename__ = "trading_assets_commands_logs"

    command_id = Column(String(255), primary_key=True)
    reason = Column(String(255), nullable=True)
    status = Column(String(255), nullable=False)

    @classmethod
    def from_entity(cls, log: entities.TradingAssetCommandLog) -> Self:
        return cls(
            command_id=log.command_id,
            reason=log.reason,
            status=log.status.value,
        )

    def to_entity(self) -> entities.TradingAssetCommandLog:
        return entities.TradingAssetCommandLog(
            command_id=self.command_id,
            reason=self.reason,
            status=entities.CommandStatus(self.status),
        )
