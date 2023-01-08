import jwt
from uuid import uuid4, UUID
from passlib.context import CryptContext

from ..exceptions.auth import InvalidTokenException
from app.settings import Settings


class AuthUserService:

    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(
        self,
        settings: Settings,
    ):
        self._secret_key = settings.secret_key
        self._token_expiration = settings.token_expiration

    def create_token(self, user_id: str) -> str:
        return jwt.encode(
            payload={"user_id": user_id},
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

    def generate_session_id(self) -> UUID:
        return uuid4()

    def hash_pass(self, raw_password: str) -> str:
        return self._pwd_context.hash(raw_password)

    def verify_pass(self, raw_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(raw_password, hashed_password)
