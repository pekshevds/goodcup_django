import decimal
from datetime import datetime
from typing import Optional, Any
from django.db import transaction
from django.db.models import QuerySet, Q
from order_app.models import StatusOrder, Order, OrderItem, CartItem, WishItem
from client_app.models import Client, Contract
from catalog_app.models import Good


def fetch_new_orders() -> QuerySet[Order]:
    return Order.objects.all()


def fetch_orders(
    client: Client, date_from: Optional[datetime], date_to: Optional[datetime]
) -> QuerySet[Order]:
    contracts = [c for c in client.contracts.all()]
    filter_contracts = Q(contract__in=contracts)
    if date_from is None and date_to is None:
        return Order.objects.filter(filter_contracts).all()
    if date_from and date_to:
        filter_date = Q(date__range=(date_from, date_to))
        return Order.objects.filter(filter_contracts & filter_date).all()
    if date_from is not None:
        filter_date = Q(date__gte=date_from)
        return Order.objects.filter(filter_contracts & filter_date).all()
    if date_to is not None:
        filter_date = Q(date__lte=date_to)
        return Order.objects.filter(filter_contracts & filter_date).all()


def fetch_all_statuses() -> QuerySet[StatusOrder]:
    return StatusOrder.active_objects.all()


def fetch_status_by_ids(ids: list[str]) -> QuerySet[StatusOrder]:
    return StatusOrder.objects.filter(id__in=ids).all()


def fetch_orders_by_ids(ids: list[str]) -> QuerySet[Order]:
    return Order.objects.filter(id__in=ids).all()


@transaction.atomic
def create_order(
    order_items: list[dict[str, Any]],
    contract: Contract | None,
    full_name: str = "",
    email: str = "",
    phone: str = "",
    delivery: int = 1,
) -> Order:
    new_order = Order.objects.create()
    new_order.is_active = True
    new_order.contract = contract
    new_order.full_name = full_name
    new_order.email = email
    new_order.phone = phone
    new_order.delivery = delivery
    new_order.status = StatusOrder.objects.get(name="Новый")
    new_order.save()
    for item in order_items:
        new_item = OrderItem.objects.create(order=new_order)
        new_item.good = item.get("good")
        new_item.quantity = item.get("quantity")
        new_item.price = item.get("price")
        new_item.amount = item.get("amount")
        new_item.save()
    return new_order


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


def fetch_cart_items(cart_owner: Client) -> QuerySet[CartItem]:
    return CartItem.objects.filter(client=cart_owner).all()


def clear_cart(cart_owner: Client) -> None:
    return CartItem.objects.filter(client=cart_owner).delete()


def set_item_to_cart(cart_owner: Client, good: Good, quantity: float) -> None:
    item = fetch_cart_items(cart_owner).filter(good=good).first()
    if not item:
        item = CartItem.objects.create()
        item.client = cart_owner
        item.good = good
    item.quantity = decimal.Decimal(float(quantity)) * good.k
    item.save()


def add_item_to_cart(cart_owner: Client, good: Good, quantity: float) -> None:
    item = fetch_cart_items(cart_owner).filter(good=good).first()
    if not item:
        item = CartItem.objects.create()
        item.client = cart_owner
        item.good = good
    item.quantity += decimal.Decimal(float(quantity)) * good.k
    item.save()


def drop_item_from_cart(cart_owner: Client, good: Good) -> None:
    item = fetch_cart_items(cart_owner).filter(good=good).first()
    if item:
        item.delete()


def fetch_wish_items(wish_owner: Client) -> QuerySet[WishItem]:
    return WishItem.objects.filter(client=wish_owner).all()


def clear_wish(wish_owner: Client) -> None:
    return WishItem.objects.filter(client=wish_owner).delete()


def set_item_to_wish(wish_owner: Client, good: Good) -> None:
    item = fetch_wish_items(wish_owner).filter(good=good).first()
    if item:
        return
    item = WishItem.objects.create()
    item.client = wish_owner
    item.good = good
    item.save()


def drop_item_from_wish(wish_owner: Client, good: Good) -> None:
    item = fetch_wish_items(wish_owner).filter(good=good).first()
    if item:
        item.delete()
