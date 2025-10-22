from django.conf import settings
from catalog_app.models import Category, Good, Image, PropertyRecord
from catalog_app.schemas import (
    CategorySchemaOutgoing,
    GoodSchemaOutgoing,
    ImageSchemaOutgoing,
    PropertySchemaOutgoing,
)


def image_to_outgoing_schema(image: Image) -> ImageSchemaOutgoing | None:
    if image:
        return ImageSchemaOutgoing(
            path=f"https://{settings.BACKEND_NAME}/{image.image.url}"
        )
    return None


def property_to_outgounig_schema(
    record: PropertyRecord,
) -> PropertySchemaOutgoing | None:
    if record:
        return PropertySchemaOutgoing(name=record.name, value=record.value)
    return None


def properties_to_outgoing_schema(
    records: list[PropertyRecord],
) -> list[PropertySchemaOutgoing] | None:
    if records:
        return [property_to_outgounig_schema(record) for record in records]
    return None


def images_to_outgoing_schema(
    images: list[Image],
) -> list[ImageSchemaOutgoing] | None:
    if images:
        return [image_to_outgoing_schema(image.image) for image in images]
    return None


def category_to_outgoing_schema(category: Category) -> CategorySchemaOutgoing:
    model = CategorySchemaOutgoing(
        id=str(category.id),
        name=category.name,
        slug=category.slug,
        pic_name=category.pic_name,
        preview_image=image_to_outgoing_schema(category.preview_image),
        childs=[category_to_outgoing_schema(c) for c in category.childs.all()],
    )
    return model


def good_to_outgoing_schema(good: Good) -> GoodSchemaOutgoing:
    model = GoodSchemaOutgoing(
        id=str(good.id),
        name=good.name,
        art=good.art,
        slug=good.slug,
        code=good.code,
        okei=good.okei,
        price=good.price,
        description=good.description,
        k=good.k,
        balance=good.balance,
        is_active=good.is_active,
        properties=properties_to_outgoing_schema(good.properties.all()),
        preview_image=image_to_outgoing_schema(good.preview_image),
        images=images_to_outgoing_schema(good.images.all()),
    )
    return model
