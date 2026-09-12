import uuid

import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.core.config import Settings
from app.core.database import get_engine, init_db, reset_engine_cache
from app.main import create_app

TEST_DATABASE_URL = "postgresql+psycopg://zayvora:zayvora@localhost:5432/zayvora_therapeutic_test"
TEST_JWT_SECRET_FALLBACK = "development-only-insecure-secret-do-not-use-in-production"

_ALL_TABLES = ("ghiza_plans", "tadbeer_plans", "nuskha_drafts")

ALL_THERAPEUTIC_PERMISSIONS = [
    "nuskha.create",
    "nuskha.read",
    "nuskha.approve",
    "tadbeer.create",
    "tadbeer.read",
    "ghiza.create",
    "ghiza.read",
]


@pytest.fixture(scope="session", autouse=True)
def _prepare_database():
    import os

    os.environ["ZAYVORA_THERAPEUTIC_DATABASE_URL"] = TEST_DATABASE_URL
    os.environ["ZAYVORA_THERAPEUTIC_ENVIRONMENT"] = "development"
    reset_engine_cache()
    init_db()
    yield


@pytest.fixture(autouse=True)
def _clean_tables():
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {', '.join(_ALL_TABLES)} RESTART IDENTITY CASCADE"))
    yield


@pytest.fixture()
def app():
    settings = Settings(database_url=TEST_DATABASE_URL, environment="development", jwt_secret="")
    return create_app(settings=settings)


@pytest.fixture()
def client(app):
    with TestClient(app) as c:
        yield c


def make_token(*, organization_id: str | None = None, user_id: str | None = None, permissions=None) -> str:
    payload = {
        "sub": user_id or str(uuid.uuid4()),
        "org": organization_id or str(uuid.uuid4()),
        "roles": ["Doctor"],
        "permissions": permissions if permissions is not None else ALL_THERAPEUTIC_PERMISSIONS,
        "iat": 0,
        "exp": 9999999999,
    }
    return jwt.encode(payload, TEST_JWT_SECRET_FALLBACK, algorithm="HS256")


@pytest.fixture()
def org_id():
    return str(uuid.uuid4())


@pytest.fixture()
def auth_headers(org_id):
    return {"Authorization": f"Bearer {make_token(organization_id=org_id)}"}


@pytest.fixture()
def other_org_headers():
    return {"Authorization": f"Bearer {make_token()}"}
