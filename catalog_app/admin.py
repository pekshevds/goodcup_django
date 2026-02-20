from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.urls import path


from django.utils.html import format_html
from django.contrib import admin
from catalog_app.models import (
    Good,
    Category,
    Offer,
    Image,
    PropertyRecord,
    GoodImage,
    Compilation,
    CompilationItem,
)
from services import upload_properties_file
from server.admin import make_active

admin.site.site_header = "Панель администрирования goodcup"
admin.site.site_title = "Панель администрирования goodcup"
admin.site.index_title = "Добро пожаловать!"


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    (
                        "image",
                        "preview",
                    ),
                    "is_active",
                    "comment",
                )
            },
        ),
    )
    list_display = ("name", "is_active", "preview", "created_at", "updated_at", "id")
    readonly_fields = ("preview",)
    actions = [make_active]

    def preview(self, obj: Image) -> str:
        if obj.image:
            str = f"'<img src={obj.image.url} style='max-height: 75px;'>"
            return format_html(str)
        return ""

    setattr(preview, "short_description", "Изображение (превью)")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "parent",
                    (
                        "preview_image",
                        "preview",
                    ),
                    "pic_name",
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
        "is_active",
        "parent",
        "preview",
        "created_at",
        "updated_at",
        "slug",
        "id",
    )
    readonly_fields = ("preview",)
    actions = [make_active]

    def preview(self, obj: Category) -> str:
        if obj.preview_image:
            str = f"'<img src={obj.preview_image.image.url} style='max-height: 75px;'>"
            return format_html(str)
        return ""

    setattr(preview, "short_description", "Изображение (превью)")


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
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
        "is_active",
        "created_at",
        "updated_at",
        "slug",
        "id",
    )
    actions = [make_active]


class PropertyRecordInLine(admin.TabularInline):
    model = PropertyRecord


class GoodImageInLine(admin.TabularInline):
    model = GoodImage


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    inlines = [PropertyRecordInLine, GoodImageInLine]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "name",
                        "art",
                        "code",
                        "short_name",
                    ),
                    (
                        "category",
                        "offer",
                    ),
                    (
                        "preview_image",
                        "preview",
                    ),
                    (
                        "balance",
                        "price",
                    ),
                    (
                        "is_active",
                        "sort_ordering",
                    ),
                    "comment",
                )
            },
        ),
        (
            "SEO",
            {
                "fields": (
                    "seo_title",
                    "seo_description",
                    "seo_keywords",
                )
            },
        ),
    )
    list_display = (
        "name",
        "art",
        "code",
        "okei",
        "k",
        "is_active",
        "category",
        "balance",
        "price",
        "preview",
        "offer",
        "created_at",
        "updated_at",
        "id",
        "slug",
    )
    readonly_fields = ("preview",)
    search_fields = ("name", "art", "code")
    list_filter = ("is_active",)
    actions = [make_active]

    def get_urls(self) -> list[Any]:
        urls = super().get_urls()
        custom_urls = [
            path("upload-excel/", self.upload_excel, name="upload-from-excel"),
        ]
        return custom_urls + urls

    def upload_excel(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            return render(request, "admin/catalog_app/good/upload_form.html", {})
        filename = "data.xlsx"
        upload_properties_file.upload_data(filename, request.FILES["file"])
        return redirect("../")

    def preview(self, obj: Good) -> str:
        if obj.preview_image:
            str = f"'<img src={obj.preview_image.image.url} style='max-height: 75px;'>"
            return format_html(str)
        return ""

    setattr(preview, "short_description", "Изображение (превью)")


class CompilationItemInLine(admin.TabularInline):
    model = CompilationItem


@admin.register(Compilation)
class СompilationAdmin(admin.ModelAdmin):
    inlines = [CompilationItemInLine]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "name",
                        "category",
                    ),
                    "preview_image",
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
        "category",
        "is_active",
        "preview",
        "created_at",
        "updated_at",
        "id",
        "slug",
    )
    readonly_fields = ("preview",)
    search_fields = ("name",)
    list_filter = (
        "is_active",
        "category",
    )
    actions = [make_active]

    def preview(self, obj: Good) -> str:
        if obj.preview_image:
            str = f"'<img src={obj.preview_image.image.url} style='max-height: 75px;'>"
            return format_html(str)
        return ""

    setattr(preview, "short_description", "Изображение (превью)")
