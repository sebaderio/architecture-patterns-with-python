from pydantic import BaseModel

from trading_assets.domain import entities
from trading_assets.domain.types import TradingAssetId


class TradingAsset(BaseModel):
    id: TradingAssetId | None
    full_name: str
    iso_code: str
    tags: list[entities.Tag]

    def add_tag(self, tag: entities.Tag):
        if not any(x for x in self.tags if x.name == tag.name):
            self.tags.append(tag)

    def remove_tag(self, tag: entities.Tag):
        self.tags = [x for x in self.tags if x.name != tag.name]

    def __eq__(self, other) -> bool:
        if isinstance(other, TradingAsset):
            return (self.full_name, self.iso_code) == (other.full_name, other.iso_code)
        raise NotImplementedError

    def __hash__(self):
        return hash((self.full_name, self.iso_code))
