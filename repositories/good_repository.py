from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.db.models import Q
from catalog_app.models import Good

PER_PAGE: int = 25


def fetch_all_goods(page_number: int = 0) -> QuerySet[Good]:
    queryset = Good.objects.all()
    if page_number == 0:
        return queryset
    paginator = Paginator(queryset, PER_PAGE)
    return paginator.get_page(page_number)


def search_goods(search: str, page_number: int = 0) -> QuerySet[Good]:
    queryset = Good.objects.filter(Q(name__icontains=search) | Q(art__icontains=search))
    if page_number == 0:
        return queryset
    paginator = Paginator(queryset, PER_PAGE)
    return paginator.get_page(page_number)


def fetch_good_by_slug(slug: str) -> Good:
    return Good.objects.filter(slug=slug).first()


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
