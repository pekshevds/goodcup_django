from django.contrib import admin
from price_app.models import PriceItem


@admin.register(PriceItem)
class PriceItemAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "region",
                    "good",
                    "price",
                    "balance",
                )
            },
        ),
    )
    list_display = (
        "good",
        "region",
        "price",
        "balance",
    )
    list_filter = ("region",)
