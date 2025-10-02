from django.db.models import QuerySet
from client_app.models import Region


def fetch_all_regions() -> QuerySet[Region]:
    return Region.objects.all()


def fetch_regions_by_ids(ids: list[str]) -> QuerySet[Region]:
    return Region.objects.filter(id__in=ids).all()


def create_or_update_regions(
    regions_to_create: list[Region], regions_to_update: list[Region]
) -> None:
    if regions_to_create:
        Region.objects.bulk_create(regions_to_create)
    if regions_to_update:
        Region.objects.bulk_update(regions_to_update, ["name", "code"])
