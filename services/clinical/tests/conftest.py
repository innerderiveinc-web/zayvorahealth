import uuid

import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.core.config import Settings
from app.core.database import get_engine, init_db, reset_engine_cache
from app.main import create_app

TEST_DATABASE_URL = "postgresql+psycopg://zayvora:zayvora@localhost:5432/zayvora_clinical_test"

# Matches the identity service's fallback dev secret exactly (see
# services/identity/app/core/security.py) — in real dev/test both services
# leave JWT_SECRET unset and share this same fallback, so a token minted
# here verifies the same way a real identity-service-issued token would.
TEST_JWT_SECRET_FALLBACK = "development-only-insecure-secret-do-not-use-in-production"

_ALL_TABLES = ("appointments", "prescriptions", "clinical_notes", "encounters", "patients")


@pytest.fixture(scope="session", autouse=True)
def _prepare_database():
    import os

    os.environ["ZAYVORA_CLINICAL_DATABASE_URL"] = TEST_DATABASE_URL
    os.environ["ZAYVORA_CLINICAL_ENVIRONMENT"] = "development"
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


def make_token(*, organization_id: str | None = None, user_id: str | None = None, roles=None, permissions=None) -> str:
    """Mints a JWT with the same shape the identity service issues, signed
    with the same fallback dev secret, so the clinical service's auth
    dependency verifies it exactly as it would a real one."""
    payload = {
        "sub": user_id or str(uuid.uuid4()),
        "org": organization_id or str(uuid.uuid4()),
        "roles": roles or ["Doctor"],
        "permissions": permissions
        or [
            "patient.create",
            "patient.read",
            "patient.update",
            "encounter.create",
            "encounter.read",
            "encounter.close",
            "clinical_note.create",
            "clinical_note.read",
            "clinical_note.amend",
            "prescription.create",
            "prescription.read",
            "prescription.discontinue",
            "appointment.create",
            "appointment.read",
            "appointment.update",
        ],
        "iat": 0,
        "exp": 9999999999,
    }
    return jwt.encode(payload, TEST_JWT_SECRET_FALLBACK, algorithm="HS256")


@pytest.fixture()
def org_id():
    return str(uuid.uuid4())


@pytest.fixture()
def auth_headers(org_id):
    token = make_token(organization_id=org_id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def other_org_headers():
    """A second organization's token — used to prove tenant isolation."""
    token = make_token()
    return {"Authorization": f"Bearer {token}"}
