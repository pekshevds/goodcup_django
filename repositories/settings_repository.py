from django.db.models import QuerySet
from settings_app.models import NewOrderRecipient
from client_app.models import Region


def fetch_all_active_new_order_recipients(
    region: Region | None = None,
) -> QuerySet[NewOrderRecipient]:
    return NewOrderRecipient.active_objects.filter(region=region).all()
