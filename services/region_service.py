from client_app.models import Region
from client_app.schemas import RegionSchemaIncoming, RegionSchemaOutgoing
from repositories import region_repository


def fetch_all_regions() -> list[RegionSchemaOutgoing]:
    return [
        RegionSchemaOutgoing.model_validate(region)
        for region in region_repository.fetch_all_regions()
    ]


def create_or_update_regions(regions_list: list[RegionSchemaIncoming]) -> None:
    ids = [
        str(_.id)
        for _ in region_repository.fetch_regions_by_ids(
            [str(item.id) for item in regions_list]
        )
    ]
    to_create = []
    to_update = []
    for _ in regions_list:
        item = Region(**_.model_dump())
        if item.id in ids:
            to_update.append(item)
        else:
            to_create.append(item)
    region_repository.create_or_update_regions(to_create, to_update)
