from typing import Any


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


class Beeline(SMSProvider):
    def __init__(self, api_key: str) -> None:
        self._url = "https://a2p-sms-https.beeline.ru/proto/http/rest"
        self._headers["Content-Type"] = "application/json;charset=utf-8"
        self._headers["X-ApiKey"] = f"ApiKey {api_key}"


class SMSData:
    def __init__(self) -> None:
        self._target: list[str] = []
        self._message: str = ""
        self._sender: str = ""
        self._action = "post_sms"

    def add_target(self, target: str) -> None:
        self._target.append(target.strip())

    def set_message(self, message: str = "") -> None:
        self._message = message.strip()

    def set_sender(self, sender: str = "") -> None:
        self._sender = sender.strip()

    def to_dict(self) -> dict[str, Any]:
        return {
            "sender": self.sender,
            "message": self.message,
            "target": self.target,
            "action": self.action,
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

    @property
    def action(self) -> str:
        return self._action
