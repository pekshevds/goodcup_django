from pydantic import BaseModel, Field


class DocSchemaOutgoing(BaseModel):
    name: str = Field(max_length=150)
    file_name: str = Field(max_length=150)
    path: str = Field(max_length=2048, default="")


class DocListSchemaOutgoing(BaseModel):
    docs: list[DocSchemaOutgoing] = Field()
    count: int = Field(default=0)
