from client_app.models import Client


def fetch_client_by_name(name: str) -> Client | None:
    return Client.objects.filter(name=name).first()
