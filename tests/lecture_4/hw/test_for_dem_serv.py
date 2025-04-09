from datetime import datetime
from http import HTTPStatus

from pydantic import SecretStr
import pytest
from fastapi.testclient import TestClient

from  hw_4.demo_service.api.main import create_app
from  hw_4.demo_service.api.utils import initialize
from  hw_4.demo_service.core.users import UserInfo, UserRole, UserService, password_is_longer_than_8

app = create_app()


@pytest.fixture
def client():
    app = create_app()
    user_service = UserService(password_validators=[password_is_longer_than_8])
    user_service.register(
        UserInfo(
            username="kaban",
            name="papa",
            birthdate=datetime(2001, 12, 10),
            role=UserRole.ADMIN,
            password=SecretStr("123456789"),
        )
    )
    app.state.user_service = user_service
    return TestClient(app)

def test_correct_register(client):
    response = client.post(
        "/user-register",
        json={
            "username": "Vadik",
            "name": "Vadim",
            "birthdate": "2000-10-10",
            "password": "123456789",
        },
    )
    assert response.status_code == HTTPStatus.OK
    
def test_fail_register_usename(client):
    client.post(
        "/user-register",
        json = {
            "username": "test_user",
            "name": "Test User",
            "birthdate": "2000-01-01",
            "role": "USER",
            "password": "123456789"
        },
    )
    
    response = client.post(
        "/user-register",
        json = {
            "username": "test_user",
            "name": "Test User New",
            "birthdate": "2000-01-01",
            "role": "USER",
            "password": "1234567899"
        },
    )
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    
def test_error_username_register(client):
    client.post(
        "/user-register",
        json = {
            "username": "test_user",
            "name": "Test User",
            "birthdate": "2000-01-01",
            "role": "USER",
            "password": "123456789"
        },
    )
    
    response = client.post(
        "/user-register",
        json = {
            "username": "test_user",
            "name": "Test User New",
            "birthdate": "2000-01-01",
            "role": "USER",
            "password": "1234567899"
        },
    )
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    
def test_get_by_username(client):
    response = client.post(
        "/user-get",
        params = {"id": 1},
        auth = ("kaban", "123456789")
    )
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    
    assert data["uid"] == 1
    assert data['username'] == "kaban"
    assert data['name'] == "papa"
    assert data['birthdate'] == "2001-12-10T00:00:00"
    assert data['role'] == "admin"
    
def test_error_params_user_get(client):
    response = client.post(
        "/user-get",
        params = {"id": 10, "username": "test_user"},
        auth = ("kaban", "123456789")
    )
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    
def test_error_none_params_user_get(client):
    response = client.post(
        "/user-get",
        params = {},
        auth = ("kaban", "123456789")
    )
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    
def test_error_password(client):
    response = client.post(
        "/user-get",
        params = {"id":1},
        auth = ("kaban", "12345678900")
    )
    
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    
def test_get_usename(client):
    response = client.post(
        "/user-get",
        params = {"username" : "kaban"},
        auth = ("kaban", "123456789")
    )
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    
    assert data["uid"] == 1
    assert data['username'] == "kaban"
    assert data['name'] == "papa"
    assert data['birthdate'] == "2001-12-10T00:00:00"
    assert data['role'] == "admin"
    
def test_error_by_username(client):
    response = client.post("/user-get", params = {"username" : "kabaniha"}, auth = ('kaban', "123456789"))
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_user_promote(client):
    client.post(
        "/user-register",
        json={
            "username": "test_user",
            "name": "Joe",
            "birthdate": "2000-05-20",
            "password": "123456789",
        },
    )

    response = client.post(
        "/user-promote",
        params={"id": 2},
        auth=("kaban", "123456789"),
    )
    assert response.status_code == HTTPStatus.OK

    
def test_error_id_user_promote(client):
    response = client.post(
        "/user-promote",
        params = {"id": 52},
        auth = ("kaban", "123456789")
    )
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    

def test_fail_403_promote_user_without_admin(client):
    client.post(
        "/user-register",
        json={
            "username": "test_user",
            "name": "Joe",
            "birthdate": "2000-05-20",
            "password": "123456789",
        },
    )

    response = client.post(
        "/user-promote",
        params={"id": 1},
        auth=("test_user", "123456789"),
    )
    assert response.status_code == HTTPStatus.FORBIDDEN

@pytest.mark.asyncio
async def test_initialize():
    app = create_app()
    async with initialize(app):
        user_service = app.state.user_service
        admin = user_service.get_by_username("admin")
        
        assert admin.uid == 1
        assert admin.info.username == "admin"
        assert admin.info.name == "admin"
        assert admin.info.birthdate == datetime.fromtimestamp(0.0)
        assert admin.info.role == UserRole.ADMIN
        assert admin.info.password == SecretStr("superSecretAdminPassword123")