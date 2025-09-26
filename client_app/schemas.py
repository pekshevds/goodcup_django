from pydantic import BaseModel, Field


class RegionSchema(BaseModel):
    id: str = Field()
    name: str = Field(max_length=150)
    code: str = Field(max_length=11, default="")
    is_active: bool = Field(default=False)


class ClientSchemaIncoming(BaseModel):
    name: str = Field()


class ClientSchemaOutgoing(BaseModel):
    name: str = Field()


class ContractSchemaOutgoing(BaseModel):
    name: str = Field()


class PinSchema(BaseModel):
    pin: str = Field()


class ClientCredentialSchema(BaseModel):
    name: str = Field()
    pin: str = Field()


class TokenSchema(BaseModel):
    token: str = Field()
