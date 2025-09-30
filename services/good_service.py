from catalog_app.models import Good
from client_app.models import Region
from catalog_app.schemas import (
    GoodSchemaIncoming,
    GoodSchemaOutgoing,
    GoodListSchemaOutgoing,
)
from catalog_app import converters
from repositories import good_repository
from repositories import price_repository


def fetch_all_goods(region: Region | None = None) -> GoodListSchemaOutgoing:
    all_goods = good_repository.fetch_all_goods()
    if region:
        region_price = {
            f"{str(item.good.id)}": item
            for item in price_repository.fetch_price(all_goods, [region])
        }
        goods = []
        for good in all_goods:
            record = region_price.get(str(good.id))

            price = record.price if record else good.price
            balance = record.balance if record else good.balance
            good_schema = GoodSchemaOutgoing(
                id=str(good.id),
                name=good.name,
                art=good.art,
                code=good.code,
                okei=good.okei,
                description=good.description,
                is_active=good.is_active,
                properties=converters.properties_to_outgoing_schema(
                    good.properties.all()
                ),
                preview_image=converters.image_to_outgoing_schema(good.preview_image),
                images=converters.images_to_outgoing_schema(good.images.all()),
                price=price,
                balance=balance,
            )
            goods.append(good_schema)
    else:
        goods = [converters.good_to_outgoing_schema(good) for good in all_goods]
    return GoodListSchemaOutgoing(goods=goods)


def create_or_update_goods(goods_list: list[GoodSchemaIncoming]) -> None:
    ids = [
        str(_.id)
        for _ in good_repository.fetch_goods_by_ids(
            [str(item.id) for item in goods_list]
        )
    ]
    to_create = []
    to_update = []
    for _ in goods_list:
        item = Good(**_.model_dump())
        if item.id in ids:
            to_update.append(item)
        else:
            to_create.append(item)
    good_repository.create_or_update_goods(to_create, to_update)
