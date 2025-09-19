from django.db import models
from server.models import Directory


class Image(Directory):
    image = models.ImageField(verbose_name="Изображение", upload_to="catalog/images/")

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class Category(Directory):
    preview_image = models.ForeignKey(
        Image, verbose_name="Превью", on_delete=models.PROTECT, null=True, blank=True
    )
    parent = models.ForeignKey(
        "Category",
        verbose_name="Родитель",
        related_name="childs",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Good(Directory):
    art = models.CharField(
        verbose_name="Артикул",
        max_length=50,
        blank=True,
        null=False,
        default="",
        db_index=True,
    )
    code = models.CharField(
        verbose_name="Код (1С:ERP)", max_length=11, blank=True, null=False, default=""
    )
    okei = models.CharField(
        verbose_name="Ед.", max_length=50, blank=True, null=False, default=""
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
    preview_image = models.ForeignKey(
        Image, verbose_name="Превью", on_delete=models.PROTECT, null=True, blank=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    description = models.CharField(
        verbose_name="Описание", max_length=2048, blank=True, null=False, default=""
    )

    class Meta:
        verbose_name = "Номенклатура"
        verbose_name_plural = "Номенклатура"
