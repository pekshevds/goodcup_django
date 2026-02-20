from django.db import models
from server.models import Directory
from client_app.models import Region


class NewOrderRecipient(Directory):
    email = models.EmailField(verbose_name="E-mail", max_length=150)
    region = models.ForeignKey(
        Region, verbose_name="Регион", null=True, blank=True, on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели извещений о получении нового заказа"
