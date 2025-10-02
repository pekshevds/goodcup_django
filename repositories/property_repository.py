from django.db import transaction
from django.db.models import QuerySet
from catalog_app.models import PropertyRecord, Good


def fetch_all_properties() -> QuerySet[PropertyRecord]:
    return PropertyRecord.objects.all()


def fetch_properties_by_goods(goods: list[Good]) -> QuerySet[Good]:
    return PropertyRecord.objects.filter(good__in=goods).all()


def fetch_goods_properties(good: Good) -> QuerySet[Good]:
    return PropertyRecord.objects.filter(good=good).all()


@transaction.atomic
def create_properties(to_create: list[PropertyRecord]) -> None:
    if to_create:
        PropertyRecord.objects.filter(
            good__in=[record.good for record in to_create]
        ).delete()
        PropertyRecord.objects.bulk_create(to_create)
