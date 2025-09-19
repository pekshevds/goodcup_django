from pydantic import BaseModel, Field


class PriceSchema(BaseModel):
    region_id: str = Field()
    good_id: str = Field()
    price: float = Field(default=0)
    balance: float = Field(default=0)


class PriceListSchema(BaseModel):
    prices: list[PriceSchema] = Field()
