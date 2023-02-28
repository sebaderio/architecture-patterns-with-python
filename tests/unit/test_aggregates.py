def test_add_tag(tag_fiat, tag_growing, trading_asset):
    assert trading_asset.tags == [tag_growing]

    trading_asset.add_tag(tag_fiat)

    assert set(trading_asset.tags) == set([tag_fiat, tag_growing])


def test_add_tag_does_not_add_duplicated_tag(tag_growing, trading_asset):
    assert trading_asset.tags == [tag_growing]

    trading_asset.add_tag(tag_growing)

    assert trading_asset.tags == [tag_growing]


def test_remove_tag(tag_growing, trading_asset):
    assert trading_asset.tags == [tag_growing]

    trading_asset.remove_tag(tag_growing)

    assert trading_asset.tags == list()


def test_remove_tag_does_not_remove_tag_when_tag_does_not_exist(
    tag_fiat, tag_growing, trading_asset
):
    assert trading_asset.tags == [tag_growing]

    trading_asset.remove_tag(tag_fiat)

    assert trading_asset.tags == [tag_growing]
