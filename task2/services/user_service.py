from passlib.context import CryptContext

from task2.database.models import User
from task2.services.base_service import BaseService

from task2.schemas.user_schemas import UserInDTO, UserOutDTO


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService(BaseService):
    """A service class for user-related operations."""
    async def create_user(self, user: UserInDTO) -> UserOutDTO:
        """
        Create a new user.
        """
        if await self._is_email_exists(email=user.email):
            raise ValueError("User already exists")

        user.password = self._hash_password(plain_password=user.password)
        user_model = await self.repository.add(
            user=User(**user.model_dump())
        )

        return UserOutDTO.model_validate(user_model)

    async def get_user(self, user_id: int) -> UserOutDTO | None:
        """
        Get a user by ID.
        """
        user_model = await self.repository.get(identifier=user_id)
        return UserOutDTO.model_validate(user_model) if user_model else None

    async def _is_email_exists(self, email: str) -> bool:
        """
        Check if an email exists in the database.
        """
        return await self.repository.get(identifier=email) is not None

    @staticmethod
    def _hash_password(plain_password: str) -> str:
        """
        Hash a plain password.
        """
        return pwd_context.hash(plain_password)
