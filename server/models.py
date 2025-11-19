import uuid
from typing import Any
from django.utils.dateformat import format
from django.db import models
from server.services import ganerate_new_number


class ActiveObjectsManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_active=True).order_by("sort_ordering")


class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(
        verbose_name="Создан", blank=False, null=True, auto_now_add=True
    )

    def as_dict(self) -> dict[str, Any]:
        result = {}
        for field in self._meta.fields:
            value = getattr(self, field.name)
            if isinstance(value, models.Model):
                # value = value.as_dict()
                continue
            if isinstance(value, uuid.UUID):
                value = str(value)
            result[field.name] = value
        return result

    class Meta:
        abstract = True


class Directory(Record):
    name = models.CharField(
        verbose_name="Наименование",
        max_length=150,
        blank=False,
        db_index=True,
        default="",
    )
    comment = models.TextField(verbose_name="Комментарий", blank=True, default="")
    is_active = models.BooleanField(verbose_name="Активный", default=False)
    updated_at = models.DateTimeField(
        verbose_name="Изменен", blank=False, null=True, auto_now=True
    )
    sort_ordering = models.IntegerField(
        verbose_name="Порядок сортировки", blank=True, null=True, default=0
    )

    objects = models.Manager()
    active_objects = ActiveObjectsManager()

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ("sort_ordering",)
        abstract = True


class Document(Record):
    number = models.IntegerField(
        verbose_name="Номер", null=True, blank=True, editable=False, default=0
    )
    date = models.DateTimeField(
        verbose_name="Дата", blank=False, null=True, auto_now_add=True
    )
    comment = models.TextField(verbose_name="Комментарий", blank=True, default="")
    is_active = models.BooleanField(verbose_name="Активный", default=False)
    updated_at = models.DateTimeField(
        verbose_name="Изменен", blank=False, null=True, auto_now=True
    )

    def __str__(self, name: str = "Документ") -> str:
        return f"{name} №{self.number} от {format(self.date, 'd F Y')}"

    def save(self, *args: list[Any], **kwargs: dict[str, Any]) -> None:
        if not self.number:
            self.number = ganerate_new_number(model=self.__class__)
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
