from django.db.models import Q, QuerySet
from catalog_app.models import Good, Category


def fetch_all_goods() -> QuerySet[Good]:
    queryset = Good.objects.all()
    return queryset


def search_goods(search: str) -> QuerySet[Good]:
    queryset = Good.objects.filter(Q(name__icontains=search) | Q(art__icontains=search))
    return queryset


def fetch_all_categories() -> QuerySet[Category]:
    queryset = Category.objects.all()
    return queryset


def fetch_category_by_slug(slug: str) -> Category:
    return Category.objects.filter(slug=slug).first()


def fetch_categories_by_ids(ids: list[str]) -> QuerySet[Category]:
    return Category.objects.filter(id__in=ids).all()


def fetch_good_by_slug(slug: str) -> Good | None:
    return Good.objects.filter(slug=slug).first()


def fetch_goods_by_category(category: Category) -> QuerySet[Good]:
    queryset = Good.objects.filter(category=category).all()
    return queryset


def fetch_goods_by_ids(ids: list[str]) -> QuerySet[Good]:
    return Good.objects.filter(id__in=ids).all()


def create_or_update_goods(
    goods_to_create: list[Good], goods_to_update: list[Good]
) -> None:
    if goods_to_create:
        Good.objects.bulk_create(goods_to_create)
    if goods_to_update:
        Good.objects.bulk_update(
            goods_to_update, ["name", "art", "code", "okei", "price", "description"]
        )
