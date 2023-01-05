import jwt
from typing import Optional
from uuid import uuid4
from passlib.context import CryptContext

from ..dto.user import UserCreateDto
from ..protocols.tokens_storage_dao import TokensStorageDAO
from ..entities.user import User
from ..exceptions.auth import (
    InvalidTokenException,
    InvalidCredentialsException,
    SessionNotFoundException,
)
from ..exceptions.users import UserAlreadyExistsException
from .user_service import UserService
from app.settings import Settings


class AuthUserService:

    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(
        self,
        tokens_dao: TokensStorageDAO,
        user_service: UserService,
        settings: Settings,
    ):
        self._tokens_dao = tokens_dao
        self._user_service = user_service
        self._secret_key = settings.secret_key
        self._token_expiration = settings.token_expiration

    async def login(self, email: str, raw_password: str) -> str:
        user = await self._user_service.get_user_by_email(email)

        if not user:
            raise InvalidCredentialsException

        if not self._verify_pass(raw_password, user.hashed_password):
            raise InvalidCredentialsException

        token = self._create_token(str(user.id))
        session_id = self._generate_session_id()
        await self._tokens_dao.save(session_id, token)
        return session_id

    async def logout(self, session_id: str) -> str:
        token = await self._tokens_dao.get_token(session_id)
        if not token:
            raise SessionNotFoundException

        await self._tokens_dao.delete_token(session_id)
        user_id = self._decode_token(token)
        return user_id

    async def get_current_user(self, session_id: str) -> Optional[User]:
        token = await self._tokens_dao.get_token(session_id)
        if not token:
            raise SessionNotFoundException

        try:
            user_id = self._decode_token(token)
        except jwt.exceptions.InvalidTokenError:
            raise InvalidTokenException

        return await self._user_service.get_user_by_id(user_id)

    async def create_user(self, user_create: UserCreateDto) -> None:
        exists = await self._user_service.get_user_by_email(user_create.email)
        if exists:
            raise UserAlreadyExistsException(
                "User with this email already exists"
            )
        hashed_password = self._hash_pass(user_create.password)
        user = User(
            id=User.generate_id(),
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
        )
        await self._user_service.create_user(user)

    def _create_token(self, user_id: str) -> str:
        return jwt.encode(
            payload={"user_id": user_id},
            key=self._secret_key,
            algorithm="HS256",
        )

    def _decode_token(self, token: str) -> str:
        data = jwt.decode(
            jwt=token,
            key=self._secret_key,
            algorithms=["HS256"],
        )
        return data["user_id"]

    def _generate_session_id(self) -> str:
        return str(uuid4())

    def _hash_pass(self, raw_password: str) -> str:
        return self._pwd_context.hash(raw_password)

    def _verify_pass(self, raw_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(raw_password, hashed_password)
