from django.db import models
from server.models import Directory


class NewOrderRecipient(Directory):
    email = models.EmailField(verbose_name="E-mail", max_length=150)

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели извещений о получении нового заказа"
