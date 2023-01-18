import jwt
from uuid import uuid4
from passlib.context import CryptContext

from app.core.common.base.types import UserId
from app.core.common.base.types import SessionId
from ..exceptions.auth import InvalidTokenException
from ..entities.user import RawPassword


class AuthUserService:

    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(
        self,
        secret_key: str,
        token_expiration: int,
    ):
        self._secret_key = secret_key
        self._token_expiration = token_expiration

    def create_token(self, user_id: UserId) -> str:
        return jwt.encode(
            payload={"user_id": str(user_id)},
            key=self._secret_key,
            algorithm="HS256",
        )

    def decode_token(self, token: str) -> str:
        try:
            data = jwt.decode(
                jwt=token,
                key=self._secret_key,
                algorithms=["HS256"],
            )
        except jwt.exceptions.InvalidTokenError:
            raise InvalidTokenException
        return data["user_id"]

    def generate_session_id(self) -> SessionId:
        return SessionId(uuid4())

    def hash_pass(self, raw_password: RawPassword) -> str:
        return self._pwd_context.hash(raw_password.value)

    def verify_pass(
        self, raw_password: RawPassword, hashed_password: str
    ) -> bool:
        return self._pwd_context.verify(raw_password.value, hashed_password)
