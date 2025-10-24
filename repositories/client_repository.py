import datetime
from random import randrange
from django.utils import timezone
from django.db.models import Q
from client_app.models import Client, Pin, Contract


def fetch_client_by_name(name: str) -> Client | None:
    return Client.objects.filter(name=name).first()


def fetch_contract_by_name(name: str) -> Contract | None:
    return Contract.objects.filter(name=name).first()


def fetch_contract_by_id(id: str) -> Contract | None:
    return Contract.objects.filter(id=id).first()


def create_new_pin(client: Client) -> str:
    code = str(randrange(100000, 999999))
    Pin.objects.create(client=client, code=code)
    return code


def fetch_active_clients_pins(client: Client) -> list[Pin]:
    created_at = timezone.now() - datetime.timedelta(minutes=5)
    return Pin.objects.filter(Q(client=client), Q(created_at__gt=created_at))
