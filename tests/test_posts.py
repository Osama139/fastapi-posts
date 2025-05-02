import pytest
from jose import jwt
from app import schemas
from app.config import settings


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts")
    print(response.json())
    assert response.status_code == 200


