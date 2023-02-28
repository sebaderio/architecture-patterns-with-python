import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import trading_assets as models
from database.models.base import metadata
from trading_assets.adapters import repositories as postgres_repositories
from trading_assets.ports import repositories


@pytest.fixture
def in_memory_sqlite_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def sqlite_session_factory(in_memory_sqlite_db):
    yield sessionmaker(bind=in_memory_sqlite_db)


@pytest.fixture
def sqlite_session(sqlite_session_factory):
    return sqlite_session_factory()


@pytest.fixture
def trading_asset_repository(
    sqlite_session,
) -> postgres_repositories.PostgresTradingAssetRepository:
    return postgres_repositories.PostgresTradingAssetRepository(sqlite_session)


@pytest.fixture
def trading_assets_query(sqlite_session):
    return sqlite_session.query(models.PostgresTradingAsset)


@pytest.fixture
def tags_query(sqlite_session):
    return sqlite_session.query(models.PostgresTag)


def test_add_trading_asset(
    trading_asset, trading_assets_query, trading_asset_repository
):
    assert len(trading_assets_query.all()) == 0

    trading_asset_repository.add(trading_asset)

    [trading_asset_in_db] = trading_assets_query.all()
    trading_asset_in_db = trading_asset_in_db.to_aggregate()

    assert trading_asset_in_db == trading_asset
    assert set(trading_asset_in_db.tags) == set(trading_asset.tags)


def test_add_trading_asset_add_tag_if_does_not_exist(
    tags_query, trading_asset, trading_asset_repository
):
    assert len(tags_query.all()) == 0

    trading_asset_repository.add(trading_asset)

    [tag_in_db] = tags_query.all()

    assert [tag_in_db.to_entity()] == trading_asset.tags


def test_add_trading_asset_do_not_add_tag_if_already_exists(
    sqlite_session, tags_query, trading_asset, trading_asset_repository
):
    tag = list(trading_asset.tags)[0]
    sqlite_session.add(models.PostgresTag.from_entity(tag))
    assert len(tags_query.all()) == 1

    trading_asset_repository.add(trading_asset)

    [tag_in_db] = tags_query.all()

    assert [tag_in_db.to_entity()] == trading_asset.tags


def test_add_trading_asset_raises_already_exists(
    trading_asset, trading_assets_query, trading_asset_repository
):
    trading_asset_repository.add(trading_asset)
    assert len(trading_assets_query.all()) == 1

    with pytest.raises(repositories.TradingAssetAlreadyExists):
        trading_asset_repository.add(trading_asset)


def test_get_trading_asset(trading_asset, trading_asset_repository):
    trading_asset_repository.add(trading_asset)

    trading_asset_from_db = trading_asset_repository.get(trading_asset.id)

    assert trading_asset_from_db == trading_asset


def test_get_trading_asset_raises_not_found(trading_asset, trading_asset_repository):
    with pytest.raises(repositories.TradingAssetNotFound):
        trading_asset_repository.get(trading_asset.id)


def test_update_trading_asset_attribute(
    trading_asset, trading_assets_query, trading_asset_repository
):
    trading_asset_repository.add(trading_asset)

    trading_asset.full_name = "Yuan"
    trading_asset_repository.update(trading_asset)

    [trading_asset_in_db] = trading_assets_query.all()

    assert trading_asset_in_db.to_aggregate() == trading_asset


def test_update_trading_asset_raises_not_found(trading_asset, trading_asset_repository):
    with pytest.raises(repositories.TradingAssetNotFound):
        trading_asset_repository.update(trading_asset)


def test_update_trading_asset_add_tag(
    tag_fiat, trading_asset, trading_assets_query, trading_asset_repository
):
    trading_asset_repository.add(trading_asset)

    trading_asset.add_tag(tag_fiat)
    trading_asset_repository.update(trading_asset)

    [trading_asset_in_db] = trading_assets_query.all()

    assert trading_asset_in_db.to_aggregate() == trading_asset


def test_update_trading_asset_remove_tag(
    tag_fiat, tags_query, trading_asset, trading_assets_query, trading_asset_repository
):
    trading_asset.add_tag(tag_fiat)
    trading_asset_repository.add(trading_asset)

    assert len(tags_query.all()) == 2

    trading_asset.remove_tag(tag_fiat)
    trading_asset_repository.update(trading_asset)

    [trading_asset_in_db] = trading_assets_query.all()
    trading_asset_in_db = trading_asset_in_db.to_aggregate()

    assert trading_asset_in_db == trading_asset
    assert len(trading_asset_in_db.tags) == 1
    assert set(trading_asset_in_db.tags) == set(trading_asset.tags)
    assert len(tags_query.all()) == 2
