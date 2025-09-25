from django.contrib import admin
from server.admin import make_active
from client_app.models import Region, Client, Pin


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
    actions = [make_active]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "region",
                    "contract",
                    "is_active",
                    "comment",
                )
            },
        ),
    )
    list_display = (
        "name",
        "region",
        "contract",
        "is_active",
        "created_at",
        "updated_at",
        "id",
    )
    search_fields = (
        "name",
        "contract",
    )
    list_filter = ("region",)
    actions = [make_active]


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {"fields": ("client", "code")},
        ),
    )
    list_display = ("code", "client", "created_at", "id")
    list_filter = ("client",)
