from pydantic import BaseModel, Field
from catalog_app.schemas import GoodSchema, PropertySchemaIncoming
from client_app.schemas import RegionSchema
from price_app.schemas import PriceSchema
from order_app.schemas import StatusSchemaIncoming


class DataSchema(BaseModel):
    goods: list[GoodSchema] = Field()
    properties: list[PropertySchemaIncoming] = Field()
    regions: list[RegionSchema] = Field()
    prices: list[PriceSchema] = Field()
    order_statuses: list[StatusSchemaIncoming] = Field()
