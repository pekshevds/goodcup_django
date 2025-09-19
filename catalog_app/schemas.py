from pydantic import BaseModel, Field


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


class GoodListSchema(BaseModel):
    goods: list[GoodSchema] = Field()
