import pytest
from httpx import AsyncClient
from main import app
from app.models.database import database

# Чтобы запустить тесты, используйте команду:
#
# pytest tests/


@pytest.fixture(scope="module")
async def test_app():
    # Подключение к базе данных перед тестами
    await database.connect()
    yield app  # Возвращаем приложение для тестирования
    await database.disconnect()  # Отключаемся после тестов


@pytest.fixture(scope="function")
async def client(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post("/register", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_login_user(client):
    # Регистрация пользователя перед тестом входа
    await client.post("/register", json={"email": "test@example.com", "password": "password123"})

    response = await client.post("/token", data={"username": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_create_referral_code(client):
    # Регистрация и вход пользователя перед созданием реферального кода
    await client.post("/register", json={"email": "test@example.com", "password": "password123"})

    login_response = await client.post("/token", data={"username": "test@example.com", "password": "password123"})
    access_token = login_response.json()["access_token"]

    referral_code_data = {"code": "REF123", "expires_at": "2023-12-31T23:59:59"}

    response = await client.post("/referral_code/create", json=referral_code_data,
                                 headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert response.json()["code"] == "REF123"


@pytest.mark.asyncio
async def test_get_referral_code(client):
    # Регистрация и создание реферального кода перед его получением
    await client.post("/register", json={"email": "test@example.com", "password": "password123"})

    login_response = await client.post("/token", data={"username": "test@example.com", "password": "password123"})
    access_token = login_response.json()["access_token"]

    referral_code_data = {"code": "REF123", "expires_at": "2023-12-31T23:59:59"}

    await client.post("/referral_code/create", json=referral_code_data,
                      headers={"Authorization": f"Bearer {access_token}"})

    response = await client.get("/referral_code/test@example.com")

    assert response.status_code == 200
    assert response.json()["code"] == "REF123"


@pytest.mark.asyncio
async def test_delete_referral_code(client):
    # Регистрация и создание реферального кода перед его удалением
    await client.post("/register", json={"email": "test@example.com", "password": "password123"})

    login_response = await client.post("/token", data={"username": "test@example.com", "password": "password123"})
    access_token = login_response.json()["access_token"]

    referral_code_data = {"code": "REF123", "expires_at": "2023-12-31T23:59:59"}
    await client.post("/referral_code/create", json=referral_code_data,
                      headers={"Authorization": f"Bearer {access_token}"})

    response = await client.delete("/referral_code/delete", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert response.json()["message"] == "Referral code deleted successfully."