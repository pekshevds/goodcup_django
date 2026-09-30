from pydantic import BaseModel, Field


class PropertySchemaIncoming(BaseModel):
    good_id: str = Field()
    sort_ordering: int = Field(default=0)
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
    parent_slug: str = Field(max_length=300, default="")
    pic_name: str = Field(max_length=150, default="")
    seo_text: str = Field(default="")
    preview_image: ImageSchemaOutgoing | None = Field(default=None)
    childs: list["CategorySchemaOutgoing"] | None = Field(default=None)


class CompilationSchemaOutgoing(BaseModel):
    id: str = Field()
    name: str = Field(max_length=150)
    slug: str = Field(max_length=300, default="")


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
    balance: float = Field(default=0)
    k: int = Field(default=1)
    is_active: bool = Field(default=False)


class GoodSchemaBaseOutgoing(BaseModel):
    id: str = Field()
    name: str = Field(max_length=150)
    short_name: str = Field(max_length=50, default="")
    art: str = Field(max_length=50, default="")
    slug: str = Field(max_length=300, default="")
    code: str = Field(max_length=11, default="")
    okei: str = Field(max_length=50, default="")
    price: float = Field(default=0)
    description: str = Field(max_length=2048, default="")
    add_description: str = Field(default="")
    balance: float = Field(default=0)
    k: int = Field(default=1)
    is_active: bool = Field(default=False)
    new: bool = Field(default=False)
    hit: bool = Field(default=False)
    promo: bool = Field(default=False)
    offer: str = Field(max_length=300, default="")
    seo_title: str = Field(default="")
    seo_description: str = Field(default="")
    seo_keywords: str = Field(default="")
    registry_link: str = Field(max_length=2048, default="")


class GoodSchemaOutgoing(GoodSchemaBaseOutgoing):
    id: str = Field()
    preview_image: ImageSchemaOutgoing | None = Field(default=None)
    properties: list[PropertySchemaOutgoing] | None = Field(default=None)
    images: list[ImageSchemaOutgoing] | None = Field(default=None)
    related_goods: list[GoodSchemaBaseOutgoing] | None = Field(default=None)


class GoodListSchemaIncoming(BaseModel):
    goods: list[GoodSchemaIncoming] = Field()


class GoodListSchemaOutgoing(BaseModel):
    goods: list[GoodSchemaOutgoing] = Field()
    count: int = Field(default=0)


class CategoryListSchemaOutgoing(BaseModel):
    categories: list[CategorySchemaOutgoing] = Field()
    count: int = Field(default=0)


class CompilationListSchemaOutgoing(BaseModel):
    compilations: list[CompilationSchemaOutgoing] = Field()
    count: int = Field(default=0)
