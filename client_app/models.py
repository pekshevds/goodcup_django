from django.db import models
from server.models import Directory, Record


class Region(Directory):
    code = models.CharField(
        verbose_name="Код (1С:ERP)", max_length=11, blank=True, null=False, default=""
    )

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"


class Organization(Directory):
    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Наши организации"


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


class Contract(Directory):
    client = models.ForeignKey(
        Client,
        verbose_name="Клиент",
        related_name="contracts",
        on_delete=models.CASCADE,
    )
    organization = models.ForeignKey(
        Organization,
        verbose_name="Организация",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    name = models.CharField(
        verbose_name="Наименование",
        max_length=25,
        blank=False,
        db_index=True,
        default="",
    )
    address = models.CharField(
        verbose_name="Адрес доставки",
        max_length=255,
        blank=True,
        default="",
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.client})"

    class Meta:
        verbose_name = "Договор"
        verbose_name_plural = "Договора"


class Pin(Record):
    client = models.ForeignKey(Client, verbose_name="Клиент", on_delete=models.CASCADE)
    code = models.CharField("Код", max_length=6)

    class Meta:
        verbose_name = "Пин-код"
        verbose_name_plural = "Пин-коды"

    def __str__(self) -> str:
        return f"{self.code} ({self.client})"
