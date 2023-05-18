from app.presentation.services.users_service import UsersService
import pytest

@pytest.mark.parametrize("id, email, is_present", [
    (1, "test@test.com", True),
    (2, "user1@example.com", True),
    (5, "not exist", False),
])
async def test_get_user_by_id(id, email, is_present):
    user = await UsersService.get_one_by_id(id)

    if is_present:
        assert user
        assert user.id == id
        assert user.email == email
    else:
        assert not user