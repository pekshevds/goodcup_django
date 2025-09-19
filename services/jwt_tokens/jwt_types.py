from typing import Any
from dataclasses import dataclass, field, asdict
from enum import Enum


class Alg(Enum):
    HS256 = "HS256"
    HS384 = "HS384"
    HS512 = "HS512"
    ES256 = "ES256"
    RS256 = "RS256"
    PS256 = "PS256"


@dataclass(frozen=True, slots=True)
class Header:
    alg: str = field(default=Alg.HS256.value)
    typ: str = field(default="JWT")


@dataclass(frozen=True, slots=True)
class Payload:
    """
    *name (Name) — собственник токена. Как правило — Имя пользователя
    *iat (Issued At) — время создания токена
    *exp (Expiration Time) — время, в течение которого токен считается валидным.
    sub (Subject) — собственник токена. Как правило — uuid пользователя
    admin (Admin) — true/false
    nbf (Not Before) — временная метка, до которй токен не считается валидным
    iss (Issuer) — издатель токена. Как правило — uuid приложения, выпустившего токен.
    aud (Audience) — массив url серверов, для которых предназначен токен
    jti (JWT ID) — уникальный идентификатор токена"""

    name: str
    iat: int
    exp: int
    sub: str = field(default="")
    admin: bool = field(default=False)
    nbf: int = field(default=0)
    iss: str = field(default="")
    aud: str = field(default="")
    jti: str = field(default="")


def to_dict(data: Any) -> dict:
    return asdict(data)


__all__ = ["Alg", "Header", "Payload", "to_dict"]
