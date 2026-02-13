from django.contrib.auth.models import User


def fetch_user_by_name(username: str) -> User | None:
    return User.objects.filter(username=username).first()
