from page_app.models import Page
from page_app.schemas import PageSchemaOutgoing


def page_to_outgoing_schema(page: Page) -> PageSchemaOutgoing:
    return PageSchemaOutgoing(
        name=page.name,
        seo_description=page.seo_description,
        seo_keywords=page.seo_keywords,
        seo_title=page.seo_title,
    )
