from django.contrib import admin
from doc_app.models import Doc


@admin.register(Doc)
class DocAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "name",
                        "file",
                    ),
                    "is_active",
                    "show_in_docs",
                    "comment",
                )
            },
        ),
    )
    list_display = (
        "name",
        "is_active",
        "show_in_docs",
        "slug",
        "created_at",
        "updated_at",
        "id",
    )
