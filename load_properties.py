import json
from catalog_app.models import Good, Offer
from services import property_service
from catalog_app.schemas import PropertySchemaIncoming


def read_data(file_name: str) -> list[dict[str, str]]:
    with open(file_name, mode="r", encoding="utf-8-sig") as file:
        data = json.load(fp=file)
    return data


def load_properties() -> None:
    for item in read_data("data.json"):
        good = Good.objects.filter(art=item.get("art")).first()
        if not good:
            continue
        offer_name = item.get("offer", "")
        offer, _ = Offer.objects.get_or_create(name=offer_name)
        good.offer = offer
        good.short_name = item.get("short_name", "")
        good.save()

        properties = []
        properties.append(
            PropertySchemaIncoming(
                good_id=str(good.id), name="Объём, мл", value=item.get("volume", "")
            )
        )
        properties.append(
            PropertySchemaIncoming(
                good_id=str(good.id),
                name="Диаметр горловины, мм",
                value=item.get("d1", ""),
            )
        )
        properties.append(
            PropertySchemaIncoming(
                good_id=str(good.id), name="Диаметр дна, мм", value=item.get("d2", "")
            )
        )
        properties.append(
            PropertySchemaIncoming(
                good_id=str(good.id), name="Высота, мм", value=item.get("heigth", "")
            )
        )
        properties.append(
            PropertySchemaIncoming(
                good_id=str(good.id), name="Цвет", value=item.get("color", "")
            )
        )
        properties.append(
            PropertySchemaIncoming(
                good_id=str(good.id), name="Особенности", value=item.get("s1", "")
            )
        )
        properties.append(
            PropertySchemaIncoming(
                good_id=str(good.id), name="Размеры коробки", value=item.get("s2", "")
            )
        )
        properties.append(
            PropertySchemaIncoming(
                good_id=str(good.id), name="Вес брутто", value=item.get("weigt", "")
            )
        )
        properties.append(
            PropertySchemaIncoming(
                good_id=str(good.id),
                name="Кол-во в упаковке (тубе)",
                value=item.get("k1", ""),
            )
        )
        properties.append(
            PropertySchemaIncoming(
                good_id=str(good.id), name="Кол-во в коробке", value=item.get("k2", "")
            )
        )
        property_service.create_properties(properties)
