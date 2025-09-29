from pydantic import BaseModel, Field


class PropertySchemaIncoming(BaseModel):
    good_id: str = Field()
    name: str = Field(max_length=150)
    value: str = Field(max_length=150, default="")


class GoodSchema(BaseModel):
    id: str = Field()
    name: str = Field(max_length=150)
    art: str = Field(max_length=50, default="")
    code: str = Field(max_length=11, default="")
    okei: str = Field(max_length=50, default="")
    price: float = Field(default=0)
    description: str = Field(max_length=2048, default="")
    balance: int = Field(default=0)
    is_active: bool = Field(default=False)
    # properties: list[PropertySchemaIncoming] | None = Field()


class GoodSchemaIncoming(BaseModel):
    id: str = Field()
    name: str = Field(max_length=150)
    art: str = Field(max_length=50, default="")
    code: str = Field(max_length=11, default="")
    okei: str = Field(max_length=50, default="")
    price: float = Field(default=0)
    description: str = Field(max_length=2048, default="")
    balance: int = Field(default=0)
    is_active: bool = Field(default=False)
    # properties: list[PropertySchemaIncoming] | None = Field()


class GoodSchemaOutgoing(BaseModel):
    id: str = Field()


class GoodListSchema(BaseModel):
    goods: list[GoodSchema] = Field()
