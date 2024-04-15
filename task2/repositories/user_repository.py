from sqlalchemy import select

from task2.repositories.base_repository import BaseRepository
from task2.database.models import User


class UserRepository(BaseRepository):
    """
    A repository class for user-related database operations.
    """
    async def add(self, user: User) -> User:
        """
        Add a new user to the database.
        """
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def get(self, identifier: str | int) -> User | None:
        """
        Retrieve a user from the database by ID or email.
        """
        stmt = (
            select(User)
            .filter(User.id == identifier)
            if isinstance(identifier, int)
            else select(User).filter(User.email == identifier)
        )

        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        return user
