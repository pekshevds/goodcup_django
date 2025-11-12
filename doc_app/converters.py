from pathlib import Path
from django.conf import settings
from doc_app.models import Doc
from doc_app.schemas import DocSchemaOutgoing


def doc_to_outgoing_schema(doc: Doc) -> DocSchemaOutgoing:
    file_path = Path(doc.file.file.name)
    return DocSchemaOutgoing(
        name=doc.name,
        file_name=file_path.name,
        path=f"https://{settings.BACKEND_NAME}{doc.file.url}",
    )
