from doc_app.schemas import DocListSchemaOutgoing
from doc_app.converters import doc_to_outgoing_schema
from repositories import doc_repository


def fetch_all_docs() -> DocListSchemaOutgoing:
    query = doc_repository.fetch_all_docs()
    return DocListSchemaOutgoing(
        docs=[doc_to_outgoing_schema(doc) for doc in query], count=len(query)
    )
