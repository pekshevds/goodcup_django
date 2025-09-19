from price_app.models import PriceItem
from price_app.schemas import PriceSchema
from repositories import price_repository, good_repository, region_repository


def fetch_all_price() -> list[PriceItem]:
    return price_repository.fetch_all_price()


def create_or_update_price(price: list[PriceSchema]) -> None:
    goods = {
        str(_.id): _
        for _ in good_repository.fetch_goods_by_ids([item.good_id for item in price])
    }
    regons = {
        str(_.id): _
        for _ in region_repository.fetch_regions_by_ids(
            [item.region_id for item in price]
        )
    }
    to_create = []
    for _ in price:
        item = PriceItem(**_.model_dump())
        item.good = goods.get(_.good_id)
        item.region = regons.get(_.region_id)
        item.price = _.price
        item.balance = _.balance
        to_create.append(item)
    price_repository.create_price(to_create)
