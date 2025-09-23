from order_app.schemas import (
    StatusSchemaIncoming,
    OrderSchemaOutgoing,
    OrderListSchemaOutgoing,
    OrderItemSchemaOutgoing,
    OrderStatusListUpdateSchemaIncoming,
)
from order_app.models import StatusOrder, Order
from repositories import order_repository


def update_order_statuses(data: OrderStatusListUpdateSchemaIncoming) -> None:
    """
    Обновляет статусы заказов клиентов"""
    statuses = order_repository.fetch_status_by_ids(
        [item.status_id for item in data.statuses]
    )
    statuses_dict = {str(status.id): status for status in statuses}
    orders = order_repository.fetch_orders_by_ids(
        [item.order_id for item in data.statuses]
    )
    orders_dict = {str(order.id): order for order in orders}
    orders_to_update = []
    for item in data.statuses:
        order = orders_dict.get(item.order_id)
        if not order:
            raise Order.DoesNotExist(f"order with id={item.order_id} does not exist")
        status = statuses_dict.get(item.status_id)
        if not status:
            raise StatusOrder.DoesNotExist(
                f"status with id={item.status_id} does not exist"
            )
        order.status = status
        orders_to_update.append(order)
    order_repository.update_orders_stutuses(orders_to_update)


def fetch_new_orders() -> OrderListSchemaOutgoing:
    orders = []
    for order in order_repository.fetch_new_orders():
        order_schema = OrderSchemaOutgoing.model_validate(order.as_dict())
        order_schema.items = [
            OrderItemSchemaOutgoing.model_validate(item.as_dict())
            for item in order.items.all()
        ]
        orders.append(order_schema)
    return OrderListSchemaOutgoing(orders=orders)


def fetch_all_regions() -> list[StatusOrder]:
    return order_repository.fetch_all_statuses()


def create_or_update_statuses(statuses_list: list[StatusSchemaIncoming]) -> None:
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
