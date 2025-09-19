from django.contrib import admin
from order_app.models import Order, OrderItem, CartItem, WishItem, StatusOrder


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
                        "client",
                        "status",
                        "comment",
                    ),
                )
            },
        ),
    )
    list_display = ("__str__", "is_active", "client", "status", "updated_at", "id")
    list_filter = (
        "client",
        "status",
    )
    readonly_fields = (
        "number",
        "date",
    )


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
