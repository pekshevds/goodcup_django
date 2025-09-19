from django.db import models
from server.models import Record
from catalog_app.models import Good
from client_app.models import Region


class PriceItem(Record):
    region = models.ForeignKey(
        Region,
        verbose_name="Регион",
        related_name="prices",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    good = models.ForeignKey(
        Good,
        verbose_name="Товар",
        related_name="prices",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    balance = models.DecimalField(
        verbose_name="Остаток",
        max_digits=15,
        decimal_places=3,
        blank=True,
        null=True,
        default=0,
    )
    price = models.DecimalField(
        verbose_name="Цена",
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )

    class Meta:
        verbose_name = "Запись цен"
        verbose_name_plural = "Цены"
