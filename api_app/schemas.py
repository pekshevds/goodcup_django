from pydantic import BaseModel, Field
from catalog_app.schemas import GoodSchemaIncoming, PropertySchemaIncoming
from client_app.schemas import RegionSchemaIncoming
from price_app.schemas import PriceSchema
from order_app.schemas import StatusSchemaIncoming


class DataSchema(BaseModel):
    goods: list[GoodSchemaIncoming] = Field()
    properties: list[PropertySchemaIncoming] = Field()
    regions: list[RegionSchemaIncoming] = Field()
    prices: list[PriceSchema] = Field()
    order_statuses: list[StatusSchemaIncoming] = Field()
