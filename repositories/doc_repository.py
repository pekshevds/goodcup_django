from django.db.models import QuerySet
from doc_app.models import Doc


def fetch_all_docs() -> QuerySet[Doc]:
    return Doc.objects.all()


def fetch_all_active_docs() -> QuerySet[Doc]:
    return Doc.active_objects.filter(show_in_docs=True).all()


def fetch_doc_by_slug(slug: str) -> Doc | None:
    return Doc.objects.filter(slug=slug).first()
