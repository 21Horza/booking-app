from httpx import AsyncClient
import pytest

@pytest.mark.parametrize("email,pwd,status_code", [
   ("email@test.com", "password", 200),
   ("email@test.com", "somepwd", 409),
   ("new_email@test.com", "password", 200),
   ("email", "password", 422),
])
async def test_register_user(email, pwd, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "pwd": pwd,
    })

    print(response.json()) 

    assert response.status_code == status_code

@pytest.mark.parametrize("email, pwd, status_code", [
    ("test@test.com", "test", 200),
    ("user1@example.com", "user1", 200),
])
async def test_login_user(email, pwd, status_code, ac: AsyncClient):
    response = await ac.post("auth/login", json={
        "email": email,
        "pwd": pwd
    })

    assert response.status_code == status_code