from typing import Iterable
from django.db import transaction
from django.db.models import Q
from price_app.models import PriceItem
from catalog_app.models import Good
from client_app.models import Region


def fetch_all_price() -> Iterable[PriceItem]:
    return PriceItem.objects.all()


def fetch_price(
    goods: Iterable[Good], regions: Iterable[Region]
) -> Iterable[PriceItem]:
    good_filter = Q(good__in=goods)
    region_filter = Q(region__in=regions)
    return PriceItem.objects.filter(good_filter & region_filter)


def clear_price() -> None:
    PriceItem.objects.all().delete()


def clear_price_by_goods(goods: Iterable[Good]) -> None:
    PriceItem.objects.filter(good__in=goods).delete()


def clear_price_by_regions(regions: Iterable[Region]) -> None:
    PriceItem.objects.filter(region__in=regions).delete()


def create_or_update_price(
    price_to_create: Iterable[PriceItem], price_to_update: Iterable[PriceItem]
) -> None:
    if price_to_create:
        PriceItem.objects.bulk_create(price_to_create)
    if price_to_update:
        PriceItem.objects.bulk_update(price_to_update, ["price", "balance"])


@transaction.atomic
def create_price(price_to_create: Iterable[PriceItem]) -> None:
    clear_price_by_goods([item.good for item in price_to_create])
    if price_to_create:
        PriceItem.objects.bulk_create(price_to_create)
