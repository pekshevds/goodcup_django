from django.db import models
from server.models import Directory


class Page(Directory):
    seo_title = models.TextField(
        verbose_name="<title>", null=True, blank=True, default=""
    )
    seo_description = models.TextField(
        verbose_name="<description>",
        null=True,
        blank=True,
        default="",
    )
    seo_keywords = models.TextField(
        verbose_name="<keywords>",
        null=True,
        blank=True,
        default="",
    )

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
