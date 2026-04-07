from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.urls import path
from django.contrib import admin
from server.admin import make_active
from client_app.models import (
    Region,
    Client,
    Pin,
    Contract,
    Organization,
    DeliveryAddress,
)
from services import upload_client_file


class DeliveryAddressInLine(admin.TabularInline):
    model = DeliveryAddress
    fields = ("name",)


class ContractsReadonlyInline(admin.TabularInline):
    model = Contract
    extra = 0
    verbose_name = "Договор"
    verbose_name_plural = "Договора"
    fieldsets = (
        (
            None,
            {"fields": ("name",)},
        ),
    )
    readonly_fields = ("name",)

    def has_add_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
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
    inlines = [ContractsReadonlyInline]
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
    list_display = (
        "name",
        "region",
        "is_active",
        "created_at",
        "updated_at",
        "id",
    )
    search_fields = ("name",)
    list_filter = ("region",)
    actions = [make_active]

    def get_urls(self) -> list[Any]:
        urls = super().get_urls()
        custom_urls = [
            path("upload-excel/", self.upload_excel, name="upload-client-from-excel"),
        ]
        return custom_urls + urls

    def upload_excel(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            return render(request, "admin/client_app/client/upload_form.html", {})
        filename = "data.xlsx"
        upload_client_file.upload_data(filename, request.FILES["file"])
        return redirect("../")


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    inlines = [DeliveryAddressInLine]
    fieldsets = (
        (
            None,
            {"fields": ("client", "name", "organization", "address")},
        ),
    )
    list_display = ("name", "client", "organization", "created_at", "updated_at", "id")
    list_filter = (
        "client",
        "organization",
    )


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
