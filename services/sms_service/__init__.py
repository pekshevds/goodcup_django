import httpx
from .dto import SMSProvider, SMSData, Beeline, BeelineSMS


class SMSTransport:
    def __init__(self, provider: SMSProvider, data: SMSData) -> None:
        self._provider = provider
        self._data = data

    def send(self) -> None:
        client = httpx.Client()
        client.headers.update(self._provider.headers)
        response = client.post(
            url=self._provider.url,
            json=self._data.to_dict(),
        )
        print(response.json())


def send_pin_by_sms(transport: SMSTransport) -> None:
    transport.send()


__all__ = ["send_pin_by_sms", "SMSTransport", "Beeline", "BeelineSMS"]
