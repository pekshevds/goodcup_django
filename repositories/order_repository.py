from order_app.models import StatusOrder, Order


def fetch_new_orders() -> list[Order]:
    return Order.objects.all()


def fetch_all_statuses() -> list[StatusOrder]:
    return StatusOrder.objects.all()


def fetch_status_by_ids(ids: list[str]) -> list[StatusOrder]:
    return StatusOrder.objects.filter(id__in=ids).all()


def create_or_update_statuses(
    statuses_to_create: list[StatusOrder], statuses_to_update: list[StatusOrder]
) -> None:
    if statuses_to_create:
        StatusOrder.objects.bulk_create(statuses_to_create)
    if statuses_to_update:
        StatusOrder.objects.bulk_update(statuses_to_update, ["name", "code"])
