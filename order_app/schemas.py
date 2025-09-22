from pydantic import BaseModel, Field


class StatusSchema(BaseModel):
    id: str = Field()
    name: str = Field(max_length=150)
    is_active: bool = Field(default=False)
