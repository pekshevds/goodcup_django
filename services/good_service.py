from django.core.paginator import Paginator
from catalog_app.models import Good
from client_app.models import Region
from catalog_app.schemas import (
    CategorySchemaOutgoing,
    CategoryListSchemaOutgoing,
    GoodSchemaIncoming,
    GoodSchemaOutgoing,
    GoodListSchemaOutgoing,
)
from catalog_app import converters
from repositories import good_repository
from repositories import price_repository

PER_PAGE: int = 25


def __fetch_goods(
    all_goods: list[Good], region: Region | None = None
) -> GoodListSchemaOutgoing:
    if not region:
        return GoodListSchemaOutgoing(
            goods=[converters.good_to_outgoing_schema(good) for good in all_goods]
        )
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
            slug=good.slug,
            code=good.code,
            okei=good.okei,
            description=good.description,
            is_active=good.is_active,
            properties=converters.properties_to_outgoing_schema(good.properties.all()),
            preview_image=converters.image_to_outgoing_schema(good.preview_image),
            images=converters.images_to_outgoing_schema(good.images.all()),
            price=price,
            balance=balance,
        )
        goods.append(good_schema)
    return GoodListSchemaOutgoing(goods=goods, count=len(goods))


def search_goods(
    search: str, region: Region | None = None, page_number: int = 0
) -> GoodListSchemaOutgoing:
    queryset = __fetch_goods(good_repository.search_goods(search), region)
    if page_number == 0:
        return queryset
    paginator = Paginator(queryset.goods, PER_PAGE)
    return paginator.get_page(page_number)


def fetch_all_categories() -> CategoryListSchemaOutgoing:
    categories = good_repository.fetch_all_categories()
    return CategoryListSchemaOutgoing(
        categories=[converters.category_to_outgoing_schema(cat) for cat in categories],
        count=len(categories),
    )


def fetch_all_goods(
    region: Region | None = None, page_number: int = 0
) -> GoodListSchemaOutgoing:
    queryset = __fetch_goods(good_repository.fetch_all_goods(), region)
    if page_number == 0:
        return queryset
    paginator = Paginator(queryset.goods, PER_PAGE)
    return paginator.get_page(page_number)


def fetch_category_by_slug(slug: str) -> CategorySchemaOutgoing:
    category = good_repository.fetch_category_by_slug(slug)
    return converters.category_to_outgoing_schema(category)


def fetch_good_by_category(
    category_slug: str, region: Region | None = None, page_number: int = 0
) -> GoodListSchemaOutgoing:
    category = good_repository.fetch_category_by_slug(category_slug)
    queryset = __fetch_goods(good_repository.fetch_goods_by_category(category), region)
    if page_number == 0:
        return queryset
    paginator = Paginator(queryset.goods, PER_PAGE)
    return paginator.get_page(page_number)


def fetch_good_by_slug(slug: str, region: Region | None = None) -> GoodSchemaOutgoing:
    good = good_repository.fetch_good_by_slug(slug)
    if not region:
        return converters.good_to_outgoing_schema(good)
    record = price_repository.fetch_price([good], [region]).first()
    price = record.price if record else good.price
    balance = record.balance if record else good.balance
    return GoodSchemaOutgoing(
        id=str(good.id),
        name=good.name,
        art=good.art,
        slug=good.slug,
        code=good.code,
        okei=good.okei,
        description=good.description,
        is_active=good.is_active,
        properties=converters.properties_to_outgoing_schema(good.properties.all()),
        preview_image=converters.image_to_outgoing_schema(good.preview_image),
        images=converters.images_to_outgoing_schema(good.images.all()),
        price=price,
        balance=balance,
    )


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
