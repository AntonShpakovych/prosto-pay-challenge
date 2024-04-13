import pytest

from task2.database.models import User


@pytest.mark.asyncio
async def test_add(simple_user, user_repository):
    new_user = await user_repository.add(
        user=User(**simple_user.model_dump())
    )

    result = [new_user.email, new_user.password]
    expected_result = [simple_user.email, simple_user.password]

    assert result == expected_result  # hashing implemented in user service
    assert new_user.id is not None


@pytest.mark.asyncio
async def test_get_user_by_existing_id(simple_user, user_repository):
    expected_result = await user_repository.add(
        user=User(**simple_user.model_dump())
    )

    result = await user_repository.get(identifier=expected_result.id)

    assert result == expected_result


@pytest.mark.asyncio
async def test_get_user_by_existing_email(simple_user, user_repository):
    expected_result = await user_repository.add(
        user=User(**simple_user.model_dump())
    )

    result = await user_repository.get(identifier=expected_result.email)

    assert result == expected_result


@pytest.mark.asyncio
async def test_get_user_by_not_existing_email(user_repository):
    expected_result = None
    result = await user_repository.get(identifier="random@gmail.com")

    assert result is expected_result


@pytest.mark.asyncio
async def test_get_user_by_not_existing_id(user_repository):
    expected_result = None
    result = await user_repository.get(identifier=1)

    assert result is expected_result
