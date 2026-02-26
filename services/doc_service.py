from doc_app.schemas import DocListSchemaOutgoing, DocSchemaOutgoing
from doc_app.converters import doc_to_outgoing_schema
from repositories import doc_repository


def fetch_all_docs() -> DocListSchemaOutgoing:
    query = doc_repository.fetch_all_active_docs()
    return DocListSchemaOutgoing(
        docs=[doc_to_outgoing_schema(doc) for doc in query], count=len(query)
    )


def fetch_doc_by_slug(slug: str) -> DocSchemaOutgoing | None:
    doc = doc_repository.fetch_doc_by_slug(slug)
    if doc:
        return doc_to_outgoing_schema(doc)
    return None
