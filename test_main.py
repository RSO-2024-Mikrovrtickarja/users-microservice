from fastapi.testclient import TestClient

import string
import random

from app.endpoints import users_app
from app.schemas import UserRegister

def generate_random_string(length: int = 12) -> str:
    return "".join([
        random.choice(string.ascii_letters + string.digits) 
        for _ in range(12)
    ])

client = TestClient(users_app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_user_register_and_login():
    username = generate_random_string(length=12)
    email = f"{username}@hello-world.com"
    password = generate_random_string(length=8) 
    
    response = client.post("/register", json=UserRegister(
        username=username,
        email=email,
        password=password
    ).model_dump())
    
    assert response.status_code == 201
    
    response = client.post("/login", data={
        "grant_type": "password",
        "username": email,
        "password": password
    })
    
    assert response.status_code == 200
    
    response_json = response.json()
    
    assert isinstance(response_json, dict)   
    assert "access_token" in response_json
