from django.contrib import admin
from settings_app.models import NewOrderRecipient


@admin.register(NewOrderRecipient)
class NewOrderRecipientAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "email",
                    "region",
                    (
                        "is_active",
                        "sort_ordering",
                    ),
                    "comment",
                )
            },
        ),
    )
    list_display = (
        "name",
        "email",
        "region",
        "is_active",
        "created_at",
        "updated_at",
        "id",
    )
    list_filter = (
        "region",
        "is_active",
    )
