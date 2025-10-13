import httpx
from django.conf import settings
from .dto import SMSProvider, SMSData, Beeline


class SMSTransport:
    def __init__(self, provider: SMSProvider, data: SMSData) -> None:
        self._provider = provider
        self._data = data

    def send(self) -> None:
        client = httpx.Client()
        client.headers.update(self._provider.headers)
        client.post(
            url=self._provider.url,
            json=self._data.to_dict(),
        )


def send_pin_by_sms(sender: str, message: str, target: str) -> None:
    provider = Beeline(settings.SMS_ACCESS_TOKEN)
    data = SMSData()
    data.add_target(target)
    data.set_sender(sender)
    data.set_message(message)
    transport = SMSTransport(provider, data)
    transport.send()


__all__ = ["send_pin_by_sms"]
