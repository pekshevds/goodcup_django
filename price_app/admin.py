from django.contrib import admin
from price_app.models import PriceItem, IndividualPriceItem


@admin.register(PriceItem)
class PriceItemAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "region",
                    "good",
                    "balance",
                    "price",
                )
            },
        ),
    )
    list_display = (
        "good",
        "region",
        "balance",
        "price",
    )
    search_fields = ("good__name",)
    list_filter = ("region",)


@admin.register(IndividualPriceItem)
class IndividualPriceItemAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "client",
                    "good",
                    "price",
                )
            },
        ),
    )
    list_display = (
        "good",
        "client",
        "price",
    )
    search_fields = ("good__name",)
    list_filter = ("client",)
