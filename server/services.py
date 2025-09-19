from django.db.models import Model


def ganerate_new_number(model: Model) -> int:
    """Вычисляет максимальный (последний) номер документа для модели model
    и возвращает следующий. Если последний номер 345, то вернет 346.
    """
    last_order = model.objects.all().order_by("number").last()
    if last_order:
        return last_order.number + 1
    return 1
