from transliterate import translit
from django.utils.text import slugify

from django.db import models
from server.models import Directory


class ActiveDocumentManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_active=True)


class Doc(Directory):
    file = models.FileField(verbose_name="Файл", upload_to="uploads/")
    slug = models.CharField(
        verbose_name="Ссылка",
        max_length=300,
        blank=True,
        null=False,
        default="",
        db_index=True,
    )
    show_in_docs = models.BooleanField(
        verbose_name="Показывать в документах", default=False
    )

    def save(self) -> None:
        self.slug = slugify(translit(f"{self.name}", reversed=True))
        super().save()

    class Meta:
        verbose_name = "Файл для скачивания"
        verbose_name_plural = "Файлы для скачивания"
        ordering = ["-created_at"]
