from django.http import HttpRequest
from django.conf import settings
from django.core.exceptions import PermissionDenied
from client_app.models import Client
from client_app.schemas import ClientCredentialSchema, ClientSchema
from repositories import client_repository
from services.jwt_tokens import HS256


def check_clients_pin(client: Client, code: str) -> bool:
    return code in [
        pin.code for pin in client_repository.fetch_active_clients_pins(client)
    ]


def check_credentials(client_schema: ClientCredentialSchema) -> None:
    client = client_repository.fetch_client_by_name(name=client_schema.name)
    if not client:
        raise PermissionDenied("invalid clientname or pin")
    if not check_clients_pin(client, client_schema.pin):
        raise PermissionDenied("invalid clientname or pin")


def fetch_token_by_credentials(client_schema: ClientCredentialSchema) -> str:
    check_credentials(client_schema)
    return HS256.get_token(client_schema.name, settings.SECRET_KEY)


def fetch_pin_by_client(client_schema: ClientSchema) -> str:
    client = client_repository.fetch_client_by_name(name=client_schema.name)
    if not client:
        raise PermissionDenied("invalid clientname or pin")
    return client_repository.create_new_pin(client)


def check_token(token: str) -> None:
    payload = HS256.extract_data(token, settings.SECRET_KEY)
    if not payload:
        raise PermissionDenied("invalid token")
    user = client_repository.fetch_client_by_name(name=payload.name)
    if not user:
        raise PermissionDenied("invalid token")


def extract_token_from_headers(request: HttpRequest) -> str:
    raw_token = request.META.get("HTTP_AUTHORIZATION")
    if raw_token:
        return raw_token.replace("Bearer", "").strip()
    return ""


def extract_token_from_cookies(request: HttpRequest) -> str:
    raw_token = request.COOKIES.get("Authorization")
    if raw_token:
        return raw_token.strip()
    return ""


def extract_token(request: HttpRequest) -> str:
    token_from_header = extract_token_from_headers(request)
    token_from_cookie = extract_token_from_cookies(request)
    return token_from_header or token_from_cookie
