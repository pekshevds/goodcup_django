from django.contrib import admin
from page_app.models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "url",
                    "is_active",
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
    list_display = ("name", "url", "is_active", "created_at", "updated_at", "id")
