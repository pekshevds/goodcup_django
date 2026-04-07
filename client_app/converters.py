from client_app.models import Client, Contract, Region
from client_app.schemas import (
    ClientSchemaOutgoing,
    ContractSchemaOutgoing,
    RegionSchemaOutgoing,
    DeliveryAddressSchemaOutgoing,
)


def _prepare_contract_name(contract: Contract) -> str:
    address = contract.address
    organization_name = contract.organization.name if contract.organization else ""
    return f"{address} {organization_name} {contract.name}".lstrip().rstrip()


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
    addresses = [
        DeliveryAddressSchemaOutgoing(id=str(address.id), name=address.name)
        for address in contract.addresses
    ]
    model = ContractSchemaOutgoing(
        id=str(contract.id), name=_prepare_contract_name(contract), addresses=addresses
    )
    return model
