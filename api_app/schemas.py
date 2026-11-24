from pydantic import BaseModel, Field

from catalog_app.schemas import (
    GoodSchemaIncoming,
    MarketplaceGoodSchemaIncoming,
    PropertySchemaIncoming,
)
from client_app.schemas import RegionSchemaIncoming
from order_app.schemas import StatusSchemaIncoming
from price_app.schemas import PriceSchema


class DataSchema(BaseModel):
    goods: list[GoodSchemaIncoming] = Field()
    properties: list[PropertySchemaIncoming] = Field()
    regions: list[RegionSchemaIncoming] = Field()
    prices: list[PriceSchema] = Field()
    order_statuses: list[StatusSchemaIncoming] = Field()
    marketplace_data: list[MarketplaceGoodSchemaIncoming] = Field()
