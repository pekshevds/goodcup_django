from price_app.models import PriceItem
from price_app.schemas import PriceSchema
from repositories import price_repository, good_repository, region_repository
from catalog_app.models import Good
from client_app.models import Region


def _fetch_goods_from_prices(prices: list[PriceSchema]) -> dict[str, Good]:
    return {
        str(good.id): good
        for good in good_repository.fetch_goods_by_ids(
            [record.good_id for record in prices]
        )
    }


def _fetch_regions_from_prices(prices: list[PriceSchema]) -> dict[str, Region]:
    return {
        str(region.id): region
        for region in region_repository.fetch_regions_by_ids(
            [price.region_id for price in prices]
        )
    }


def fetch_all_price() -> list[PriceItem]:
    return price_repository.fetch_all_price()


def fetch_region_price(goods: list[Good], region: Region) -> list[PriceItem]:
    return price_repository.fetch_price(goods, [region])


def create_or_update_price(prices: list[PriceSchema]) -> None:
    goods = _fetch_goods_from_prices(prices)
    regions = _fetch_regions_from_prices(prices)
    to_create = []
    for record in prices:
        region = regions.get(record.region_id)
        if not region:
            raise Region.DoesNotExist(
                f"region with id={record.region_id} does not exist"
            )
        good = goods.get(record.good_id)
        if not good:
            raise Good.DoesNotExist(f"good with id={record.good_id} does not exist")
        item = PriceItem()
        item.region = region
        item.good = good
        item.price = record.price
        item.balance = record.balance
        to_create.append(item)
    price_repository.create_price(to_create)
