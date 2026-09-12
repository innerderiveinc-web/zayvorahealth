import uuid

import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.clients.clinical_client import FakeClinicalClient
from app.clients.knowledge_client import FakeKnowledgeClient
from app.core.config import Settings
from app.core.database import get_engine, init_db, reset_engine_cache
from app.main import create_app
from app.providers.fake_provider import ScriptedFakeProvider

TEST_DATABASE_URL = "postgresql+psycopg://zayvora:zayvora@localhost:5432/zayvora_ai_test"
TEST_JWT_SECRET_FALLBACK = "development-only-insecure-secret-do-not-use-in-production"

_ALL_TABLES = ("ai_consultations",)


@pytest.fixture(scope="session", autouse=True)
def _prepare_database():
    import os

    os.environ["ZAYVORA_AI_DATABASE_URL"] = TEST_DATABASE_URL
    os.environ["ZAYVORA_AI_ENVIRONMENT"] = "development"
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
def sample_patient_id():
    return str(uuid.uuid4())


@pytest.fixture()
def fake_clinical_client(sample_patient_id):
    return FakeClinicalClient(
        patients={
            sample_patient_id: {
                "age": 35,
                "pregnancy_status": "not_applicable",
                "lactation_status": "no",
                "allergies": ["penicillin"],
                "current_medications": [],
                "comorbidities": [],
                "full_name": "Test Patient",
            }
        }
    )


@pytest.fixture()
def fake_knowledge_client():
    return FakeKnowledgeClient(mufradat_by_axis={"meda-amaa": [{"name": "Sonf"}, {"name": "Asrul"}]})


@pytest.fixture()
def fake_ai_provider():
    return ScriptedFakeProvider()


@pytest.fixture()
def app(fake_clinical_client, fake_knowledge_client, fake_ai_provider):
    settings = Settings(database_url=TEST_DATABASE_URL, environment="development", jwt_secret="")
    return create_app(
        settings=settings,
        clinical_client=fake_clinical_client,
        knowledge_client=fake_knowledge_client,
        ai_provider=fake_ai_provider,
    )


@pytest.fixture()
def client(app):
    with TestClient(app) as c:
        yield c


def make_token(*, organization_id: str | None = None, permissions=None) -> str:
    payload = {
        "sub": str(uuid.uuid4()),
        "org": organization_id or str(uuid.uuid4()),
        "roles": ["Doctor"],
        "permissions": permissions if permissions is not None else ["hakeem.consult"],
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
