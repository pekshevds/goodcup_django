from jwt.exceptions import (
    InvalidSignatureError,
    InvalidAlgorithmError,
    ExpiredSignatureError,
    DecodeError,
)
from services.jwt_tokens.jwt_types import Header, Payload, Alg, to_dict
from datetime import datetime, timezone, timedelta

import jwt


class HS256:
    @classmethod
    def get_token(cls, name: str, secret: str, exp_min: int = 1440) -> str:
        now = datetime.now(tz=timezone.utc)
        iat = int(now.timestamp())
        exp = int((now + timedelta(minutes=exp_min)).timestamp())
        return jwt.encode(
            payload=to_dict(Payload(name=name, iat=iat, exp=exp)),
            key=secret,
            algorithm=Alg.HS256.value,
            headers=to_dict(Header()),
        )

    @classmethod
    def extract_data(cls, token: str, secret: str) -> Payload | None:
        try:
            return Payload(**jwt.decode(token, key=secret, algorithms=Alg.HS256.value))
        except (
            DecodeError,
            NotImplementedError,
            InvalidSignatureError,
            InvalidAlgorithmError,
            ExpiredSignatureError,
        ):
            return None


__all__ = ["HS256"]
