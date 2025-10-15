from client_app.models import Client, Contract, Region
from client_app.schemas import (
    ClientSchemaOutgoing,
    ContractSchemaOutgoing,
    RegionSchemaOutgoing,
)


def region_to_outgoing_schema(region: Region) -> RegionSchemaOutgoing:
    model = RegionSchemaOutgoing(
        id=str(region.id),
        name=region.name,
        code=region.code,
        comment=region.comment,
        is_active=region.is_active,
    )
    return model


def client_to_outgoing_schema(client: Client) -> ClientSchemaOutgoing:
    model = ClientSchemaOutgoing(name=client.name)
    return model


def contract_to_outgoing_schema(contract: Contract) -> ContractSchemaOutgoing:
    model = ContractSchemaOutgoing(name=contract.name)
    return model
