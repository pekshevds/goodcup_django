from django.db.models import QuerySet
from doc_app.models import Doc


def fetch_all_docs() -> QuerySet[Doc]:
    return Doc.objects.all()


def fetch_all_active_docs() -> QuerySet[Doc]:
    return Doc.active_objects.all()
