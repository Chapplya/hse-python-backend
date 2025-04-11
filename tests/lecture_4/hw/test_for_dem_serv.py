from datetime import datetime
from http import HTTPStatus
from faker import Faker
from pydantic import SecretStr
import pytest
from fastapi.testclient import TestClient

from hw_4.demo_service.api.main import create_app
from hw_4.demo_service.api.utils import initialize
from lecture_4.demo_service.api.contracts import UserResponse
from hw_4.demo_service.core.users import (
    UserInfo,
    UserRole,
    UserService,
    password_is_longer_than_8,
)

app = create_app()


fake = Faker()


@pytest.fixture()
def client():
    with TestClient(app) as client:
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

        yield client

        if hasattr(app.state, "user_service"):
            app.state.user_service._data.clear()
            app.state.user_service._username_index.clear()
            app.state.user_service._last_id = 0


@pytest.fixture()
def user(client):
    username = "test_user_1"

    name = "test_name_1"
    birthdate = str(fake.date_time().isoformat())
    password = "12345678910"
    resp = client.post(
        "/user-register",
        json={
            "username": username,
            "name": name,
            "birthdate": birthdate,
            "password": password,
        },
    )
    json = resp.json()
    return UserResponse(
        uid=json["uid"],
        username=username,
        name=name,
        birthdate=birthdate,
        role=json["role"],
    )


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


def test_fail_register_usename(client, user):
    response = client.post(
        "/user-register",
        json={
            "username": user.username,
            "name": "Test User New",
            "birthdate": "2000-01-01",
            "role": "USER",
            "password": "1234567899",
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_by_username(client):
    response = client.post("/user-get", params={"id": 1}, auth=("kaban", "123456789"))

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert data["uid"] == 1
    assert data["username"] == "kaban"
    assert data["name"] == "papa"
    assert data["role"] == "admin"


@pytest.mark.parametrize(
    "parameters, excpected_code",
    [
        ({"id": 10, "username": "test_user"}, HTTPStatus.BAD_REQUEST),
        ({}, HTTPStatus.BAD_REQUEST),
    ],
)
def test_error_none_params_user_get(client, parameters, excpected_code):
    response = client.post("/user-get", params=parameters, auth=("kaban", "123456789"))

    assert response.status_code == excpected_code


def test_error_password(client):
    response = client.post("/user-get", params={"id": 1}, auth=("kaban", "12345678900"))

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_usename(client):
    response = client.post(
        "/user-get", params={"username": "kaban"}, auth=("kaban", "123456789")
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert data["uid"] == 1
    assert data["username"] == "kaban"
    assert data["name"] == "papa"
    assert data["role"] == "admin"


def test_error_by_username(client, user):
    response = client.post(
        "/user-get", params={"username": user.username}, auth=("kaban", "123456789")
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_user_promote(client, user):
    response = client.post(
        "/user-promote",
        params={"id": user.uid},
        auth=("kaban", "123456789"),
    )
    assert response.status_code == HTTPStatus.OK


def test_error_id_user_promote(client):
    response = client.post(
        "/user-promote", params={"id": 52}, auth=("kaban", "123456789")
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_fail_403_promote_user_without_admin(client, user):
    response = client.post(
        "/user-promote",
        params={"id": user.uid},
        auth=(user.uid, "123456789"),
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
        assert admin.info.birthdate == str(fake.date_time().isoformat())
        assert admin.info.role == UserRole.ADMIN
        assert admin.info.password == SecretStr("superSecretAdminPassword123")
