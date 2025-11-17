from django.db.models import QuerySet
from page_app.models import Page


def fetch_page_by_name(name: str) -> Page | None:
    return Page.objects.filter(name=name).first()


def fetch_all_pages() -> QuerySet[Page]:
    return Page.objects.all()


def fetch_all_active_pages() -> QuerySet[Page]:
    return Page.active_documents.all()
