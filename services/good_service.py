from catalog_app.models import Good
from catalog_app.schemas import GoodSchema, GoodListSchema
from repositories import good_repository


def fetch_all_goods() -> GoodListSchema:
    return GoodListSchema(
        goods=[
            GoodSchema.model_validate(good.as_dict())
            for good in good_repository.fetch_all_goods()
        ]
    )


def create_or_update_goods(goods_list: list[GoodSchema]) -> None:
    ids = [
        str(_.id)
        for _ in good_repository.fetch_goods_by_ids(
            [str(item.id) for item in goods_list]
        )
    ]
    to_create = []
    to_update = []
    for _ in goods_list:
        item = Good(**_.model_dump())
        if item.id in ids:
            to_update.append(item)
        else:
            to_create.append(item)
    good_repository.create_or_update_goods(to_create, to_update)
