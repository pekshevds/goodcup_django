from services.jwt_tokens import HS256
from django.conf import settings
from django.contrib.auth.models import User
from repositories import user_repository


def user_by_token(token: str) -> User | None:
    payload = HS256.extract_data(token, settings.SECRET_KEY)
    if not payload:
        return None
    return user_repository.fetch_user_by_name(username=payload.name)
