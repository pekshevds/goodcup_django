from datetime import datetime
from pydantic import BaseModel, Field
from client_app.schemas import ClientSchema
from catalog_app.schemas import GoodSchema


class StatusSchema(BaseModel):
    id: str = Field()
    name: str = Field(max_length=150)
    is_active: bool = Field(default=False)


class OrderItemSchema(BaseModel):
    id: str = Field()
    good: GoodSchema = Field()
    quantity: float = Field()
    price: float = Field()
    amount: float = Field()


class OrderSchema(BaseModel):
    id: str = Field()
    number: int = Field()
    date: datetime = Field()
    comment: str = Field()
    client: ClientSchema = Field()
    status: StatusSchema = Field()
    items: list[OrderItemSchema] = Field(default=[])


class OrderListSchema(BaseModel):
    orders: list[OrderSchema] = Field()
