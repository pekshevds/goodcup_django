from django.contrib import admin
from order_app.models import Order, OrderItem, CartItem, WishItem


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
                        "comment",
                    ),
                )
            },
        ),
    )
    list_display = ("__str__", "is_active", "client", "id")
    list_filter = ("client",)
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
