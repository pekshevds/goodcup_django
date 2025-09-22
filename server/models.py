import uuid
from typing import Any
from django.utils.dateformat import format
from django.db import models
from server.services import ganerate_new_number


class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(
        verbose_name="Создан", blank=False, null=True, auto_now_add=True
    )

    def as_dict(self) -> dict[str, Any]:
        result = {}
        for field in self._meta.fields:
            value = getattr(self, field.name)
            if isinstance(value, uuid.UUID):
                value = str(value)
            if isinstance(value, models.Model):
                value = value.as_dict()
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

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
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

    def save(self) -> None:
        if not self.number:
            self.number = ganerate_new_number(model=self.__class__)
        return super().save()

    class Meta:
        abstract = True
