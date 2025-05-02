import pytest
from jose import jwt
from app import schemas
from app.config import settings


def test_create_user(client):
    response = client.post('/users', json={"name": "osama", "email": "osama@fakeemail.com", "password": "osama1399"})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "osama@fakeemail.com"
    assert response.status_code == 201

def test_login(client, test_user):
    response = client.post('/auth/login', data={'username':test_user['email'], 'password': test_user['password']})
    login_Res = schemas.Token(**response.json())
    payload = jwt.decode(login_Res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    user_id = payload.get("user_id")
    assert user_id == test_user["id"]
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
                                                ('wrong1@email.com', 'wrong_password1', 403),
                                                ('osama@fakeemail.com', 'wrong_password2', 403),
                                                ('wrong3@email.com', 'wrong_password3', 403),
                                                (None, 'sunny1399', 422),
                                                ('osama@fakeemail.com', None, 422)
                                            ])
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post('/auth/login', data={'username':email, 'password': password})
    assert response.status_code == 403
    # assert response.json().get('detail') == "Incorrect Credentials"
