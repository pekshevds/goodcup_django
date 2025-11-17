from pydantic import BaseModel, Field


class PageSchemaOutgoing(BaseModel):
    name: str = Field(max_length=150, default="")
    seo_title: str = Field(default="")
    seo_description: str = Field(default="")
    seo_keywords: str = Field(default="")


class PageListSchemaOutgoing(BaseModel):
    pages: list[PageSchemaOutgoing] = Field()
    count: int = Field(default=0)
