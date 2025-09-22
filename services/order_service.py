from order_app.schemas import (
    StatusSchema,
    OrderSchema,
    OrderListSchema,
    OrderItemSchema,
)
from order_app.models import StatusOrder
from repositories import order_repository


def fetch_new_orders() -> OrderListSchema:
    orders = []
    for order in order_repository.fetch_new_orders():
        order_schema = OrderSchema.model_validate(order.as_dict())
        order_schema.items = [
            OrderItemSchema.model_validate(item.as_dict()) for item in order.items.all()
        ]
        orders.append(order_schema)
    return OrderListSchema(orders=orders)


def fetch_all_regions() -> list[StatusOrder]:
    return order_repository.fetch_all_statuses()


def create_or_update_statuses(statuses_list: list[StatusSchema]) -> None:
    ids = [
        str(_.id)
        for _ in order_repository.fetch_status_by_ids(
            [str(item.id) for item in statuses_list]
        )
    ]
    to_create = []
    to_update = []
    for _ in statuses_list:
        item = StatusOrder(**_.model_dump())
        if item.id in ids:
            to_update.append(item)
        else:
            to_create.append(item)
    order_repository.create_or_update_statuses(to_create, to_update)
