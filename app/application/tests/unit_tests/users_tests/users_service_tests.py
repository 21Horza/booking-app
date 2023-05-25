import pytest

from app.presentation.services.users_service import UsersService


@pytest.mark.parametrize("email, is_present", [
    ("test@test.com", True),
    ("user1@example.com", True),
    (".....", False),
])
async def test_get_user_by_email(email, is_present):
    user = await UsersService.get_one_or_none(email=email)

    if is_present:
        assert user
        assert user.email == email
    else:
        assert not user