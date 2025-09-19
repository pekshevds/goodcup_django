from django.db import models
from server.models import Directory, Record


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


class Pin(Record):
    client = models.ForeignKey(Client, verbose_name="Клиента", on_delete=models.CASCADE)
    code = models.CharField("Код", max_length=6)

    class Meta:
        verbose_name = "Пин-код"
        verbose_name_plural = "Пин-коды"

    def __str__(self) -> str:
        return f"{self.code} ({self.client})"
