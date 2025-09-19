from django.contrib import admin
from client_app.models import Region, Client


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "is_active",
                    "comment",
                )
            },
        ),
    )
    list_display = ("name", "is_active", "created_at", "updated_at", "id")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "region",
                    "is_active",
                    "comment",
                )
            },
        ),
    )
    list_display = ("name", "region", "is_active", "created_at", "updated_at", "id")
    list_filter = ("region",)
