import random
import string
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

from app.endpoints import users_app
from app.schemas import UserRegister


def generate_random_string(length: int = 12) -> str:
    return "".join([
        random.choice(string.ascii_letters + string.digits) 
        for _ in range(length)
    ])


@pytest_asyncio.fixture()
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=users_app),
        base_url="http://test"
    ) as async_client, LifespanManager(users_app):
        yield async_client
        

@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_user_register_and_login(client: AsyncClient):
    username = generate_random_string(length=12)
    email = f"{username}@hello-world.com"
    password = generate_random_string(length=8) 
    
    response = await client.post(
        "/register/", 
        json=UserRegister(
            username=username,
            email=email,
            password=password
        ).model_dump()
    )
    
    assert response.status_code == 201
    
    response = await client.post("/login", data={
        "grant_type": "password",
        "username": email,
        "password": password
    })
    
    assert response.status_code == 200
    
    response_json = response.json()
    
    assert isinstance(response_json, dict)   
    assert "access_token" in response_json
