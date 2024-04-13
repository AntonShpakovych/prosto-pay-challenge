import pytest

from task2.schemas.user_schemas import UserOutDTO
from task2.services.user_service import pwd_context


@pytest.mark.asyncio
async def test_protected__is_email_exists_if_exists(
    simple_user,
    user_service
):
    await user_service.create_user(user=simple_user)

    res = await user_service._is_email_exists(email=simple_user.email)

    assert res is True


@pytest.mark.asyncio
async def test_protected_is_email_exists_if_not_exists(
    simple_user,
    user_service
):
    res = await user_service._is_email_exists(email=simple_user.email)

    assert res is False


@pytest.mark.asyncio
async def test_protected_hash_password(simple_user, user_service):
    plain_password = simple_user.password
    hashed_password = user_service._hash_password(
        plain_password=plain_password
    )

    assert hashed_password != plain_password
    assert pwd_context.verify(plain_password, hashed_password)


@pytest.mark.asyncio
async def test_create_user_if_not_exists(simple_user, user_service):
    result = await user_service.create_user(user=simple_user)
    expected_result = UserOutDTO.model_validate(result)

    assert result == expected_result


@pytest.mark.asyncio
async def test_create_user_if_exists(simple_user, user_service):
    await user_service.create_user(user=simple_user)

    with pytest.raises(ValueError):
        await user_service.create_user(user=simple_user)


@pytest.mark.asyncio
async def test_get_user_if_exists(simple_user, user_service):
    user = await user_service.create_user(user=simple_user)

    res = await user_service.get_user(user_id=user.id)
    expected_result = UserOutDTO.model_validate(res)

    assert res == expected_result


@pytest.mark.asyncio
async def test_get_user_if_not_exists(user_service):
    res = await user_service.get_user(user_id=1)
    expected_result = None

    assert res == expected_result
