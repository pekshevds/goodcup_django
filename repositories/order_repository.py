from django.db.models import QuerySet
from order_app.models import StatusOrder, Order


def fetch_new_orders() -> QuerySet[Order]:
    return Order.objects.all()


def fetch_all_statuses() -> QuerySet[StatusOrder]:
    return StatusOrder.objects.all()


def fetch_status_by_ids(ids: list[str]) -> QuerySet[StatusOrder]:
    return StatusOrder.objects.filter(id__in=ids).all()


def fetch_orders_by_ids(ids: list[str]) -> QuerySet[Order]:
    return Order.objects.filter(id__in=ids).all()


def fetch_status_by_id(id: str) -> StatusOrder | None:
    return StatusOrder.objects.filter(id=id).first()


def fetch_order_by_id(id: str) -> Order | None:
    return Order.objects.filter(id=id).first()


def update_orders_stutuses(orders_to_update: list[Order]) -> None:
    Order.objects.bulk_update(orders_to_update, ["status"])


def create_or_update_statuses(
    statuses_to_create: list[StatusOrder], statuses_to_update: list[StatusOrder]
) -> None:
    if statuses_to_create:
        StatusOrder.objects.bulk_create(statuses_to_create)
    if statuses_to_update:
        StatusOrder.objects.bulk_update(statuses_to_update, ["name"])
