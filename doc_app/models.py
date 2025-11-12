from django.db import models
from server.models import Directory


class ActiveDocumentManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_active=True)


class Doc(Directory):
    file = models.FileField(verbose_name="Файл", upload_to="uploads/")

    objects = models.Manager()
    active_documents = ActiveDocumentManager()

    class Meta:
        verbose_name = "Файл для скачивания"
        verbose_name_plural = "Файлы для скачивания"
        ordering = ["-created_at"]
