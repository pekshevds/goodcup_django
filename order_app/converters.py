from order_app.models import Order, OrderItem
from order_app.schemas import (
    OrderSchemaOutgoing,
    OrderItemSchemaOutgoing,
    StatusSchemaOutgoing,
)
from catalog_app.converters import good_to_outgoing_schema
from client_app.converters import contract_to_outgoing_schema


def order_item_to_outgoing_schema(order_item: OrderItem) -> OrderItemSchemaOutgoing:
    model = OrderItemSchemaOutgoing(
        id=str(order_item.id),
        good=good_to_outgoing_schema(order_item.good),
        quantity=order_item.quantity,
        price=order_item.price,
        amount=order_item.amount,
    )
    return model


def order_to_outgoing_schema(order: Order) -> OrderSchemaOutgoing:
    model = OrderSchemaOutgoing(
        id=str(order.id),
        number=order.number,
        date=order.date,
        comment=order.comment,
        contract=None
        if order.contract is None
        else contract_to_outgoing_schema(order.contract),
        status=StatusSchemaOutgoing(id=str(order.status.id), name=order.status.name),
        items=[
            order_item_to_outgoing_schema(order_item)
            for order_item in order.items.all()
        ],
    )
    return model
