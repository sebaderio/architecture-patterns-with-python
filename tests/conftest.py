import pytest

from trading_assets.domain import aggregates, entities


@pytest.fixture
def tag_fiat():
    return entities.Tag(id=1, name="fiat")


@pytest.fixture
def tag_growing():
    return entities.Tag(id=2, name="growing")


@pytest.fixture
def trading_asset(tag_growing) -> aggregates.TradingAsset:
    return aggregates.TradingAsset(
        id=1, full_name="Renminbi", iso_code="CNY", tags=[tag_growing]
    )
