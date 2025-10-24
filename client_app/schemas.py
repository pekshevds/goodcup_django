from pydantic import BaseModel, Field


class RegionSchemaIncoming(BaseModel):
    id: str = Field()
    name: str = Field(max_length=150)
    code: str = Field(max_length=11, default="")
    comment: str = Field(default="")
    is_active: bool = Field(default=False)


class RegionSchemaOutgoing(BaseModel):
    id: str = Field()
    name: str = Field(max_length=150)
    code: str = Field(max_length=11, default="")
    comment: str = Field(default="")
    is_active: bool = Field(default=False)


class ClientSchemaIncoming(BaseModel):
    name: str = Field()


class ContractSchemaIncoming(BaseModel):
    name: str = Field()


class ClientSchemaOutgoing(BaseModel):
    name: str = Field()


class ContractSchemaOutgoing(BaseModel):
    id: str = Field()
    name: str = Field()


class ContractListSchemaOutgoing(BaseModel):
    items: list[ContractSchemaOutgoing] = Field()


class PinSchema(BaseModel):
    pin: str = Field()


class ClientCredentialSchema(BaseModel):
    name: str = Field()
    pin: str = Field()


class TokenSchema(BaseModel):
    token: str = Field()


class RequestSchemaIncoming(BaseModel):
    name: str = Field()
    phone: str = Field()
    email: str = Field(default="")


class FeedbackSchemaIncoming(BaseModel):
    name: str = Field()
    phone: str = Field()
    email: str = Field(default="")
    message: str = Field()
