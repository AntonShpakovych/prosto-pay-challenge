from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from task2.database.models import Base


class BaseRepository(ABC):
    """
    An abstract base class for repository classes.
    """
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @abstractmethod
    async def add(self, *args, **kwargs) -> Base:
        pass

    @abstractmethod
    async def get(self, *args, **kwargs) -> Base | None:
        pass
