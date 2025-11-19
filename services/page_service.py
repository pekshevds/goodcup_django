from page_app.schemas import PageListSchemaOutgoing, PageSchemaOutgoing
from page_app.converters import page_to_outgoing_schema
from repositories import page_repository


def fetch_page_by_name(page_name: str) -> PageSchemaOutgoing | None:
    page = page_repository.fetch_page_by_name(page_name)
    if page:
        return page_to_outgoing_schema(page)
    return None


def fetch_all_pages() -> PageListSchemaOutgoing:
    query = page_repository.fetch_all_active_pages()
    return PageListSchemaOutgoing(
        pages=[page_to_outgoing_schema(page) for page in query], count=len(query)
    )
