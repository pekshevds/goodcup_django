from datetime import datetime
from typing import Any, Optional
from order_app.schemas import (
    StatusSchemaIncoming,
    OrderListSchemaOutgoing,
    OrderSchemaOutgoing,
    OrderStatusListUpdateSchemaIncoming,
    NewOrderIncoming,
    CartItemSchemaOutgoing,
    CartItemListSchemaOutgoing,
    AddCartItemSchemaIncoming,
    WishItemSchemaOutgoing,
    WishItemListSchemaOutgoing,
)

from order_app.models import StatusOrder, Order
from client_app.models import Client, Region
from repositories import (
    order_repository,
    price_repository,
    good_repository,
    client_repository,
)
from catalog_app import converters
from catalog_app.models import Good
from order_app.converters import order_to_outgoing_schema, order_item_to_outgoing_schema


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


def create_order(incoming_data: NewOrderIncoming) -> OrderSchemaOutgoing:
    data = []
    goods = good_repository.fetch_goods_by_slugs(
        slugs=[item.good_slug for item in incoming_data.items]
    )
    for item in incoming_data.items:
        result = [good for good in goods if good.slug == item.good_slug]
        if result:
            data.append(
                {
                    "good": result[0],
                    "quantity": item.quantity,
                    "price": item.price,
                    "amount": item.amount,
                }
            )
    contract = client_repository.fetch_contract_by_name(incoming_data.contract_name)
    order = order_repository.create_order(data, contract)
    return order_to_outgoing_schema(order)


def fetch_new_orders() -> OrderListSchemaOutgoing:
    orders = []
    for order in order_repository.fetch_new_orders():
        order_schema = order_to_outgoing_schema(order)
        order_schema.items = [
            order_item_to_outgoing_schema(item) for item in order.items.all()
        ]
        orders.append(order_schema)
    return OrderListSchemaOutgoing(orders=orders)


def fetch_orders(
    client: Client, date_from: Optional[datetime], date_to: Optional[datetime]
) -> OrderListSchemaOutgoing:
    orders = []
    for order in order_repository.fetch_orders(client, date_from, date_to):
        order_schema = order_to_outgoing_schema(order)
        order_schema.items = [
            order_item_to_outgoing_schema(item) for item in order.items.all()
        ]
        orders.append(order_schema)
    return OrderListSchemaOutgoing(orders=orders)


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


def _fetch_region_prices(goods: list[Good], region: Region) -> dict[str, Any]:
    return {
        f"{str(item.good.id)}": item
        for item in price_repository.fetch_price(goods, [region])
    }


def fetch_cart_items(client: Client) -> CartItemListSchemaOutgoing:
    cart_items = order_repository.fetch_cart_items(client)
    goods = [cart_item.good for cart_item in cart_items]
    region_prices = _fetch_region_prices(goods, client.region)
    items = []
    for cart_item in cart_items:
        good = cart_item.good
        record = region_prices.get(str(good.id))
        price = (record.price if record else good.price) * good.k
        quantity = cart_item.quantity / good.k
        cart_item_schema = CartItemSchemaOutgoing(
            good=converters.good_to_outgoing_schema(good),
            quantity=quantity,
            price=price,
            amount=price * quantity,
        )
        items.append(cart_item_schema)
    return CartItemListSchemaOutgoing(items=items)


def clear_cart(client: Client) -> None:
    order_repository.clear_cart(client)


def set_item_to_cart(data: AddCartItemSchemaIncoming, client: Client) -> None:
    good = good_repository.fetch_good_by_slug(data.good_slug)
    if good:
        order_repository.set_item_to_cart(client, good, data.quantity)


def add_item_to_cart(data: AddCartItemSchemaIncoming, client: Client) -> None:
    good = good_repository.fetch_good_by_slug(data.good_slug)
    if good:
        order_repository.add_item_to_cart(client, good, data.quantity)


def drop_item_from_cart(data: AddCartItemSchemaIncoming, client: Client) -> None:
    good = good_repository.fetch_good_by_slug(data.good_slug)
    if good:
        order_repository.drop_item_from_cart(client, good)


def fetch_wish_items(client: Client) -> WishItemListSchemaOutgoing:
    cart_items = order_repository.fetch_wish_items(client)
    goods = [cart_item.good for cart_item in cart_items]
    region_prices = _fetch_region_prices(goods, client.region)
    items = []
    for cart_item in cart_items:
        good = cart_item.good
        record = region_prices.get(str(good.id))
        price = (record.price if record else good.price) * good.k
        cart_item_schema = WishItemSchemaOutgoing(
            good=converters.good_to_outgoing_schema(good),
            quantity=0,
            price=price,
            amount=0,
        )
        items.append(cart_item_schema)
    return WishItemListSchemaOutgoing(items=items)


def clear_wish(client: Client) -> None:
    order_repository.clear_wish(client)


def set_item_to_wish(data: AddCartItemSchemaIncoming, client: Client) -> None:
    good = good_repository.fetch_good_by_slug(data.good_slug)
    if good:
        order_repository.set_item_to_wish(client, good)


def drop_item_from_wish(data: AddCartItemSchemaIncoming, client: Client) -> None:
    good = good_repository.fetch_good_by_slug(data.good_slug)
    if good:
        order_repository.drop_item_from_wish(client, good)
