from catalog_app.models import PropertyRecord
from catalog_app.schemas import PropertySchemaIncoming
from repositories import property_repository, good_repository


def create_properties(properties_list: list[PropertySchemaIncoming]) -> None:
    goods = {
        str(good.id): good
        for good in good_repository.fetch_goods_by_ids(
            [str(item.good_id) for item in properties_list]
        )
    }
    to_create = []
    for record in properties_list:
        good = goods.get(record.good_id)
        if good:
            item = PropertyRecord()
            item.good = good
            item.name = record.name
            item.value = record.value
            to_create.append(item)
    property_repository.create_properties(to_create)
