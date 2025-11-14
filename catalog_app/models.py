from transliterate import translit
from django.utils.text import slugify
from django.db import models
from server.models import Directory, Record


class Image(Directory):
    image = models.ImageField(verbose_name="Изображение", upload_to="catalog/images/")

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class Category(Directory):
    slug = models.CharField(
        verbose_name="Ссылка",
        max_length=300,
        blank=True,
        null=False,
        default="",
        db_index=True,
    )
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
    pic_name = models.CharField(
        verbose_name="Имя пиктограммы",
        max_length=150,
        blank=True,
        null=False,
        default="",
    )

    def save(self) -> None:
        self.slug = slugify(translit(f"{self.name}", reversed=True))
        super().save()

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
    slug = models.CharField(
        verbose_name="Ссылка",
        max_length=300,
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
    k = models.DecimalField(
        verbose_name="К.",
        max_digits=15,
        decimal_places=3,
        blank=True,
        null=True,
        default=1,
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
    seo_title = models.TextField(
        verbose_name="<title>", null=True, blank=True, default=""
    )
    seo_description = models.TextField(
        verbose_name="<description>",
        null=True,
        blank=True,
        default="",
    )
    seo_keywords = models.TextField(
        verbose_name="<keywords>",
        null=True,
        blank=True,
        default="",
    )

    def save(self) -> None:
        self.slug = slugify(translit(f"{self.name}-{self.art}", reversed=True))
        super().save()

    class Meta:
        verbose_name = "Номенклатура"
        verbose_name_plural = "Номенклатура"


class GoodImage(Record):
    good = models.ForeignKey(
        Good, verbose_name="Товар", on_delete=models.CASCADE, related_name="images"
    )
    image = models.ForeignKey(
        Image, verbose_name="Изображение", on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"


class PropertyRecord(Record):
    good = models.ForeignKey(
        Good, verbose_name="Товар", on_delete=models.CASCADE, related_name="properties"
    )
    name = models.CharField(
        verbose_name="Свойство", max_length=150, blank=True, null=False, default=""
    )
    value = models.CharField(
        verbose_name="Значение", max_length=150, blank=True, null=False, default=""
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Запись свойство/значение"
        verbose_name_plural = "Свойства товара"


class Compilation(Directory):
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    slug = models.CharField(
        verbose_name="Ссылка",
        max_length=300,
        blank=True,
        null=False,
        default="",
        db_index=True,
    )
    preview_image = models.ForeignKey(
        Image, verbose_name="Превью", on_delete=models.PROTECT, null=True, blank=True
    )
    description = models.CharField(
        verbose_name="Описание", max_length=2048, blank=True, null=False, default=""
    )

    def save(self) -> None:
        self.slug = slugify(translit(f"{self.name}", reversed=True))
        super().save()

    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"


class CompilationItem(Record):
    compilation = models.ForeignKey(
        Compilation, verbose_name="Подборка", on_delete=models.CASCADE
    )
    good = models.ForeignKey(Good, verbose_name="Товар", on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Элемент подборки"
        verbose_name_plural = "Элементы подборок"
