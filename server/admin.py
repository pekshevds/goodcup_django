from django.contrib import admin
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpRequest


@admin.action(description="Активировать выбранные")
def make_active(
    modeladmin: models.Model, request: HttpRequest, queryset: QuerySet
) -> None:
    queryset.update(is_active=True)
