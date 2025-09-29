from django.db import transaction
from django.db.models import Q
from price_app.models import PriceItem
from catalog_app.models import Good
from client_app.models import Region


def fetch_all_price() -> list[PriceItem]:
    return PriceItem.objects.all()


def fetch_price(goods: list[Good], regions: list[Region]) -> list[PriceItem]:
    good_filter = Q(good__in=goods)
    region_filter = Q(region__in=regions)
    return PriceItem.objects.filter(good_filter & region_filter)


def clear_price() -> None:
    PriceItem.objects.all().delete()


def clear_price_by_goods(goods: list[Good]) -> None:
    PriceItem.objects.filter(good__in=goods).delete()


def clear_price_by_regions(regions: list[Region]) -> None:
    PriceItem.objects.filter(region__in=regions).delete()


def create_or_update_price(
    price_to_create: list[PriceItem], price_to_update: list[PriceItem]
) -> None:
    if price_to_create:
        PriceItem.objects.bulk_create(price_to_create)
    if price_to_update:
        PriceItem.objects.bulk_update(price_to_update, ["price", "balance"])


@transaction.atomic
def create_price(price_to_create: list[PriceItem]) -> None:
    clear_price_by_goods([item.good for item in price_to_create])
    if price_to_create:
        PriceItem.objects.bulk_create(price_to_create)
