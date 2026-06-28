import time
import uuid
from dataclasses import dataclass

import requests

from data import DEFAULT_PASSWORD
from urls import API_URL


@dataclass
class TestUser:
    email: str
    password: str
    name: str
    access_token: str
    refresh_token: str


def create_user():
    email = f"ui_{int(time.time())}_{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "email": email,
        "password": DEFAULT_PASSWORD,
        "name": "UI Test",
    }
    response = requests.post(f"{API_URL}/auth/register", json=payload, timeout=30)
    response.raise_for_status()
    body = response.json()
    return TestUser(
        email=email,
        password=DEFAULT_PASSWORD,
        name=payload["name"],
        access_token=body["accessToken"],
        refresh_token=body["refreshToken"],
    )


def delete_user(access_token):
    response = requests.delete(
        f"{API_URL}/auth/user",
        headers={"Authorization": access_token},
        timeout=30,
    )
    if response.status_code not in (202, 401, 403, 404):
        response.raise_for_status()