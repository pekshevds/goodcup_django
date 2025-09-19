from django.db import models
from server.models import Document, Record
from catalog_app.models import Good
from client_app.models import Client


class Order(Document):
    client = models.ForeignKey(
        Client,
        verbose_name="Клиент",
        related_name="orders",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-number"]

    def __str__(self, name: str = "Заказ") -> str:
        return super().__str__(name)


class OrderItem(Record):
    order = models.ForeignKey(
        Order, verbose_name="Строки", on_delete=models.CASCADE, related_name="items"
    )
    good = models.ForeignKey(
        Good,
        verbose_name="Номенклатура",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    quantity = models.DecimalField(
        verbose_name="Количество",
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
    amount = models.DecimalField(
        verbose_name="Сумма",
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )

    def __str__(self) -> str:
        return f"{super().__str__()}, {self.good}"

    class Meta:
        verbose_name = "Строка заказа"
        verbose_name_plural = "Строки заказа"


class CartItem(Record):
    client = models.ForeignKey(
        Client,
        verbose_name="Клиент",
        related_name="cart",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    good = models.ForeignKey(
        Good,
        verbose_name="Номенклатура",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    quantity = models.DecimalField(
        verbose_name="Количество",
        max_digits=15,
        decimal_places=3,
        blank=True,
        null=True,
        default=0,
    )

    def __str__(self) -> str:
        return f"{self.client}, {self.good}"

    class Meta:
        verbose_name = "Строка корзины"
        verbose_name_plural = "Корзина"
        # unique_together = [("client", "good")]


class WishItem(Record):
    client = models.ForeignKey(
        Client,
        verbose_name="Клиент",
        related_name="wish",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    good = models.ForeignKey(
        Good,
        verbose_name="Номенклатура",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.client}, {self.good}"

    class Meta:
        verbose_name = "Строка избранного"
        verbose_name_plural = "Избранное"
        unique_together = [("client", "good")]
