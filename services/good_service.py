from django.core.paginator import Paginator
from django.conf import settings
from catalog_app.models import Good
from client_app.models import Region
from catalog_app.schemas import (
    CategorySchemaOutgoing,
    CategoryListSchemaOutgoing,
    GoodSchemaIncoming,
    GoodSchemaOutgoing,
    GoodListSchemaOutgoing,
    CompilationSchemaOutgoing,
    CompilationListSchemaOutgoing,
)
from catalog_app import converters
from repositories import good_repository
from repositories import price_repository


def _fetch_goods(
    all_goods: list[Good], region: Region | None = None
) -> list[GoodSchemaOutgoing]:
    if not region:
        goods = [converters.good_to_outgoing_schema(good) for good in all_goods]
        return goods
    region_price = {
        f"{str(item.good.id)}": item
        for item in price_repository.fetch_price(all_goods, [region])
    }
    goods = []
    for good in all_goods:
        record = region_price.get(str(good.id))
        price = (record.price if record else good.price) * good.k
        balance = (record.balance if record else good.balance) / good.k
        good_schema = converters.good_to_outgoing_schema(good)
        good_schema.price = price
        good_schema.balance = balance
        goods.append(good_schema)
    return goods


def search_goods(
    search: str, region: Region | None = None, page_number: int = 0
) -> GoodListSchemaOutgoing:
    queryset = _fetch_goods(good_repository.search_goods(search), region)
    if page_number == 0:
        return GoodListSchemaOutgoing(goods=queryset, count=len(queryset))
    paginator = Paginator(queryset, settings.ITEMS_PER_PAGE)
    return GoodListSchemaOutgoing(
        goods=paginator.get_page(page_number), count=len(queryset)
    )


def fetch_all_categories() -> CategoryListSchemaOutgoing:
    categories = good_repository.fetch_all_active_categories()
    return CategoryListSchemaOutgoing(
        categories=[converters.category_to_outgoing_schema(cat) for cat in categories],
        count=len(categories),
    )


def fetch_subcategories_by_slug(
    category_slug: str,
) -> CategoryListSchemaOutgoing | None:
    category = good_repository.fetch_category_by_slug(category_slug)
    if not category:
        return None
    categories = good_repository.fetch_active_subcategories(category)
    return CategoryListSchemaOutgoing(
        categories=[converters.category_to_outgoing_schema(cat) for cat in categories],
        count=len(categories),
    )


def fetch_all_goods(
    region: Region | None = None, page_number: int = 0
) -> GoodListSchemaOutgoing:
    queryset = _fetch_goods(good_repository.fetch_all_active_goods(), region)
    if page_number == 0:
        return GoodListSchemaOutgoing(goods=queryset, count=len(queryset))
    paginator = Paginator(queryset, settings.ITEMS_PER_PAGE)
    return GoodListSchemaOutgoing(
        goods=paginator.get_page(page_number), count=len(queryset)
    )


def fetch_category_by_slug(slug: str) -> CategorySchemaOutgoing | None:
    category = good_repository.fetch_category_by_slug(slug)
    if category:
        return converters.category_to_outgoing_schema(category)
    return None


def fetch_goods_by_compilation_slug(
    compilation_slug: str, region: Region | None = None, page_number: int = 0
) -> GoodListSchemaOutgoing | None:
    compilation = good_repository.fetch_compilation_by_slug(compilation_slug)
    if not compilation:
        return None
    queryset = _fetch_goods(
        good_repository.fetch_goods_by_compilation(compilation), region
    )
    if page_number == 0:
        return GoodListSchemaOutgoing(goods=queryset, count=len(queryset))
    paginator = Paginator(queryset, settings.ITEMS_PER_PAGE)
    return GoodListSchemaOutgoing(
        goods=paginator.get_page(page_number), count=len(queryset)
    )


def fetch_goods_by_offer_slug(
    offer_slug: str, region: Region | None = None, page_number: int = 0
) -> GoodListSchemaOutgoing | None:
    offer = good_repository.fetch_offer_by_slug(offer_slug)
    if not offer:
        return None
    queryset = _fetch_goods(good_repository.fetch_goods_by_offer(offer), region)
    if page_number == 0:
        return GoodListSchemaOutgoing(goods=queryset, count=len(queryset))
    paginator = Paginator(queryset, settings.ITEMS_PER_PAGE)
    return GoodListSchemaOutgoing(
        goods=paginator.get_page(page_number), count=len(queryset)
    )


def fetch_goods_by_category_slug(
    category_slug: str, region: Region | None = None, page_number: int = 0
) -> GoodListSchemaOutgoing | None:
    category = good_repository.fetch_category_by_slug(category_slug)
    if not category:
        return None
    categories = [_ for _ in category.childs.all()]
    categories.append(category)
    goods = good_repository.fetch_goods_by_categories(categories)
    queryset = _fetch_goods(goods, region)
    if page_number == 0:
        return GoodListSchemaOutgoing(goods=queryset, count=len(queryset))
    paginator = Paginator(queryset, settings.ITEMS_PER_PAGE)
    return GoodListSchemaOutgoing(
        goods=paginator.get_page(page_number), count=len(queryset)
    )


def fetch_compilations_by_category_slug(
    category_slug: str,
) -> CompilationListSchemaOutgoing | None:
    category = good_repository.fetch_category_by_slug(category_slug)
    if not category:
        return None
    queryset = good_repository.fetch_compilations_by_category(category=category)
    return CompilationListSchemaOutgoing(
        compilations=[
            CompilationSchemaOutgoing(id=str(item.id), name=item.name, slug=item.slug)
            for item in queryset
        ],
        count=len(queryset),
    )


def fetch_universal_compilations() -> CompilationListSchemaOutgoing | None:
    queryset = good_repository.fetch_active_universal_compilations()
    if not queryset:
        return None
    return CompilationListSchemaOutgoing(
        compilations=[
            CompilationSchemaOutgoing(id=str(item.id), name=item.name, slug=item.slug)
            for item in queryset
        ],
        count=len(queryset),
    )


def fetch_good_by_slug(
    slug: str, region: Region | None = None
) -> GoodSchemaOutgoing | None:
    good = good_repository.fetch_good_by_slug(slug)
    if not good:
        return None
    result = converters.good_to_outgoing_schema(good)
    if not region:
        return result

    record = price_repository.fetch_price([good], [region]).first()
    price = (record.price if record else good.price) * good.k
    balance = (record.balance if record else good.balance) * good.k

    result.price = price
    result.balance = balance
    return result


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
