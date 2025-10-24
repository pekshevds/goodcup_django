from django.contrib import admin
from order_app.models import Order, OrderItem, CartItem, WishItem, StatusOrder
from client_app.models import Client


@admin.register(StatusOrder)
class StatusOrderAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "comment",
                )
            },
        ),
    )
    list_display = ("name", "is_active", "created_at", "updated_at", "id")
    search_fields = ("name",)


class OrderItemInLine(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInLine]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "number",
                        "date",
                    ),
                    "is_active",
                    (
                        "contract",
                        "status",
                        "comment",
                    ),
                )
            },
        ),
    )
    list_display = (
        "__str__",
        "is_active",
        "contract",
        "client",
        "status",
        "updated_at",
        "id",
    )
    list_filter = (
        "contract__client",
        "status",
    )
    readonly_fields = (
        "number",
        "date",
    )
    search_fields = ("contract__name",)

    def client(self, obj: Order) -> Client | None:
        if obj.contract:
            return obj.contract.client
        return None

    setattr(client, "short_description", "Клиент")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "client",
                    "good",
                    "quantity",
                )
            },
        ),
    )
    list_display = ("client", "good", "quantity", "id")
    list_filter = ("client",)


@admin.register(WishItem)
class WishItemAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "client",
                    "good",
                )
            },
        ),
    )
    list_display = ("client", "good", "id")
    list_filter = ("client",)
