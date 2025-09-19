from django.db import models
from server.models import Directory


class Region(Directory):
    code = models.CharField(
        verbose_name="Код (1С:ERP)", max_length=11, blank=True, null=False, default=""
    )

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"


class Client(Directory):
    region = models.ForeignKey(
        Region,
        verbose_name="Регион",
        related_name="clients",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
