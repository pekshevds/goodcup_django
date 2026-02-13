from django.db.models import QuerySet
from settings_app.models import NewOrderRecipient


def fetch_all_active_new_order_recipients() -> QuerySet[NewOrderRecipient]:
    return NewOrderRecipient.active_objects.all()
