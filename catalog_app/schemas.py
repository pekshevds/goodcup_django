from pydantic import BaseModel, Field


class PropertySchemaIncoming(BaseModel):
    good_id: str = Field()
    name: str = Field(max_length=150)
    value: str = Field(max_length=150, default="")


class PropertySchemaOutgoing(BaseModel):
    name: str = Field(max_length=150, default="")
    value: str = Field(max_length=150, default="")


class ImageSchemaOutgoing(BaseModel):
    path: str = Field(max_length=2048, default="")


class CategorySchemaOutgoing(BaseModel):
    id: str = Field()
    name: str = Field(max_length=150)
    slug: str = Field(max_length=300, default="")
    preview_image: ImageSchemaOutgoing | None = Field(default=None)
    childs: list["CategorySchemaOutgoing"] | None = Field(default=None)


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


class GoodSchemaOutgoing(BaseModel):
    id: str = Field()
    name: str = Field(max_length=150)
    art: str = Field(max_length=50, default="")
    slug: str = Field(max_length=300, default="")
    code: str = Field(max_length=11, default="")
    okei: str = Field(max_length=50, default="")
    price: float = Field(default=0)
    description: str = Field(max_length=2048, default="")
    balance: int = Field(default=0)
    is_active: bool = Field(default=False)
    preview_image: ImageSchemaOutgoing | None = Field(default=None)
    properties: list[PropertySchemaOutgoing] | None = Field(default=None)
    images: list[ImageSchemaOutgoing] | None = Field(default=None)


class GoodListSchemaIncoming(BaseModel):
    goods: list[GoodSchemaIncoming] = Field()


class GoodListSchemaOutgoing(BaseModel):
    goods: list[GoodSchemaOutgoing] = Field()
    count: int = Field(default=0)


class CategoryListSchemaOutgoing(BaseModel):
    categories: list[CategorySchemaOutgoing] = Field()
    count: int = Field(default=0)
