from catalog_app.models import Good


def fetch_all_goods() -> list[Good]:
    return Good.objects.all()


def fetch_goods_by_ids(ids: list[str]) -> list[Good]:
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
