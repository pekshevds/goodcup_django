from typing import Any


class SMSData:
    def __init__(self, target: str, message: str, sender: str) -> None:
        self._target: list[str] = [target]
        self._message: str = message
        self._sender: str = sender

    def to_dict(self) -> dict[str, Any]:
        return {
            "sender": self.sender,
            "message": self.message,
            "target": self.target,
        }

    @property
    def target(self) -> str:
        return ",".join(self._target)

    @property
    def message(self) -> str:
        return self._message

    @property
    def sender(self) -> str:
        return self._sender

    class Meta:
        abstract = True


class SMSProvider:
    _url: str = ""
    _headers: dict[str, Any] = {}

    @property
    def url(self) -> str:
        return self._url.strip()

    @property
    def headers(self) -> dict[str, Any]:
        return self._headers

    class Meta:
        abstract = True


class BeelineSMS(SMSData):
    def __init__(self, target: str, message: str, sender: str) -> None:
        self._target: list[str] = [target]
        self._message: str = message
        self._sender: str = sender
        self._action = "post_sms"

    def to_dict(self) -> dict[str, Any]:
        return {
            "sender": self.sender,
            "message": self.message,
            "target": self.target,
            "action": self.action,
        }

    @property
    def action(self) -> str:
        return self._action


class Beeline(SMSProvider):
    def __init__(self, api_key: str) -> None:
        self._url = "https://a2p-sms-https.beeline.ru/proto/http/rest"
        self._headers["Content-Type"] = "application/json;charset=utf-8"
        self._headers["X-ApiKey"] = f"ApiKey {api_key}"
