import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from task2.database.config import Base
from task2.repositories.user_repository import UserRepository
from task2.schemas.user_schemas import UserInDTO
from task2.services.user_service import UserService


@pytest_asyncio.fixture()
async def async_engine():
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield test_engine
    await test_engine.dispose()


@pytest_asyncio.fixture()
async def async_session(async_engine):
    test_session = async_sessionmaker(async_engine, expire_on_commit=False)

    async with test_session() as session:
        yield session


@pytest_asyncio.fixture()
async def user_repository(async_session):
    return UserRepository(db=async_session)


@pytest_asyncio.fixture()
async def user_service(user_repository):
    return UserService(repository=user_repository)


@pytest_asyncio.fixture()
async def simple_user():
    return UserInDTO(email="color@black.com", password="Password123q!")
