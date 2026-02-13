from typing import Any
from django.db import models
from server.models import Directory, Document, Record
from catalog_app.models import Good
from client_app.models import Client, Contract


class DeliveryChoice(models.IntegerChoices):
    PICKUP = 1, "Самовывоз"
    DELIVERY = 2, "Транспортная компания"


class StatusOrder(Directory):
    class Meta:
        verbose_name = "Статус заказа"
        verbose_name_plural = "Статусы заказов"

    def __str__(self) -> str:
        return self.name


class Order(Document):
    contract = models.ForeignKey(
        Contract,
        verbose_name="Договор",
        related_name="orders",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    status = models.ForeignKey(
        StatusOrder,
        verbose_name="Статус",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    full_name = models.CharField(
        verbose_name="Наименование (ФИО)",
        max_length=150,
        blank=True,
        null=True,
        default="",
    )
    email = models.CharField(
        verbose_name="Почта",
        max_length=150,
        blank=True,
        null=True,
        default="",
    )
    phone = models.CharField(
        verbose_name="Телефон",
        max_length=150,
        blank=True,
        null=True,
        default="",
    )
    delivery = models.SmallIntegerField(
        choices=DeliveryChoice.choices,
        default=DeliveryChoice.PICKUP,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-number"]

    def __str__(self, name: str = "Заказ") -> str:
        return super().__str__(name)

    def save(self, *args: list[Any], **kwargs: dict[str, Any]) -> None:
        super().save(*args, **kwargs)


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
        unique_together = [("client", "good")]


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
