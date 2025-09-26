from datetime import datetime
from pydantic import BaseModel, Field
from client_app.schemas import ContractSchemaOutgoing
from catalog_app.schemas import GoodSchemaOutgoing


class StatusSchemaIncoming(BaseModel):
    id: str = Field()
    name: str = Field(max_length=150)


class StatusSchemaOutgoing(BaseModel):
    id: str = Field()


class OrderItemSchemaOutgoing(BaseModel):
    id: str = Field()
    good: GoodSchemaOutgoing = Field()
    quantity: float = Field()
    price: float = Field()
    amount: float = Field()


class OrderSchemaOutgoing(BaseModel):
    id: str = Field()
    number: int = Field()
    date: datetime = Field()
    comment: str = Field()
    contract: ContractSchemaOutgoing = Field()
    status: StatusSchemaOutgoing = Field()
    items: list[OrderItemSchemaOutgoing] = Field(default=[])


class OrderListSchemaOutgoing(BaseModel):
    orders: list[OrderSchemaOutgoing] = Field()


class OrderStatusUpdateSchemaIncoming(BaseModel):
    order_id: str = Field()
    status_id: str = Field()


class OrderStatusListUpdateSchemaIncoming(BaseModel):
    statuses: list[OrderStatusUpdateSchemaIncoming] = Field()
