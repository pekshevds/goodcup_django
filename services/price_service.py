from price_app.models import PriceItem
from price_app.schemas import PriceSchema
from repositories import price_repository, good_repository, region_repository
from catalog_app.models import Good
from client_app.models import Region


def fetch_all_price() -> list[PriceItem]:
    return price_repository.fetch_all_price()


def create_or_update_price(price: list[PriceSchema]) -> None:
    goods = {
        str(good.id): good
        for good in good_repository.fetch_goods_by_ids([_.good_id for _ in price])
    }
    regons = {
        str(region.id): region
        for region in region_repository.fetch_regions_by_ids(
            [_.region_id for _ in price]
        )
    }
    to_create = []
    for _ in price:
        item = PriceItem(**_.model_dump())
        good = goods.get(_.good_id)
        if not good:
            raise Good.DoesNotExist(f"good with id={_.good_id} does not exist")
        item.good = good
        region = regons.get(_.region_id)
        if not region:
            raise Region.DoesNotExist(f"region with id={_.region_id} does not exist")
        item.region = region
        item.price = _.price
        item.balance = _.balance
        to_create.append(item)
    price_repository.create_price(to_create)
