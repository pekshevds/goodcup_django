from typing import Any
from django.http import HttpRequest
from django.conf import settings
from client_app.models import Client
from client_app.schemas import (
    ClientCredentialSchema,
    ClientSchemaIncoming,
    RequestSchemaIncoming,
)
from repositories import client_repository
from services.jwt_tokens import HS256


def check_clients_pin(client: Client, code: str) -> bool:
    return code in [
        pin.code for pin in client_repository.fetch_active_clients_pins(client)
    ]


def check_credentials(client_schema: ClientCredentialSchema) -> bool:
    client = client_repository.fetch_client_by_name(name=client_schema.name)
    if not client:
        return False
    if not check_clients_pin(client, client_schema.pin):
        return False
    return True


def fetch_token_by_credentials(client_schema: ClientCredentialSchema) -> str:
    if not check_credentials(client_schema):
        return ""
    return HS256.get_token(client_schema.name, settings.SECRET_KEY)


def fetch_pin_by_client(client_schema: ClientSchemaIncoming) -> str:
    client = client_repository.fetch_client_by_name(name=client_schema.name)
    if not client:
        return ""
    return client_repository.create_new_pin(client)


def client_by_token(token: str) -> Client | None:
    payload = HS256.extract_data(token, settings.SECRET_KEY)
    if not payload:
        return None
    return client_repository.fetch_client_by_name(name=payload.name)


def __extract_token_from(token_storage: dict[str, Any]) -> str:
    raw_token = token_storage.get("Authorization")
    if raw_token:
        return raw_token.replace("Bearer", "").strip()
    return ""


def extract_token_from_headers(request: HttpRequest) -> str:
    return __extract_token_from(request.META)


def extract_token_from_cookies(request: HttpRequest) -> str:
    return __extract_token_from(request.COOKIES)


def process_incoming_request(request: RequestSchemaIncoming) -> None:
    pass
