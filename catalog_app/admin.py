from django.utils.html import format_html
from django.contrib import admin
from catalog_app.models import Good, Category, Image

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
    list_display = ("name", "is_active", "preview", "id")
    readonly_fields = ("preview",)

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
                    "is_active",
                    "comment",
                )
            },
        ),
    )
    list_display = ("name", "is_active", "parent", "preview", "id")
    readonly_fields = ("preview",)

    def preview(self, obj: Category) -> str:
        if obj.preview_image:
            str = f"'<img src={obj.preview_image.image.url} style='max-height: 75px;'>"
            return format_html(str)
        return ""

    setattr(preview, "short_description", "Изображение (превью)")


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("name", "art", "code"),
                    "category",
                    (
                        "preview_image",
                        "preview",
                    ),
                    ("balance", "price"),
                    "is_active",
                    "comment",
                )
            },
        ),
    )
    list_display = (
        "name",
        "is_active",
        "category",
        "balance",
        "price",
        "preview",
        "id",
    )
    readonly_fields = ("preview",)

    def preview(self, obj: Good) -> str:
        if obj.preview_image:
            str = f"'<img src={obj.preview_image.image.url} style='max-height: 75px;'>"
            return format_html(str)
        return ""

    setattr(preview, "short_description", "Изображение (превью)")
