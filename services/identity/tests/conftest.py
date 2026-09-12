import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.core.config import Settings
from app.core.database import get_engine, get_session_factory, init_db, reset_engine_cache
from app.main import create_app

TEST_DATABASE_URL = "postgresql+psycopg://zayvora:zayvora@localhost:5432/zayvora_identity_test"

_ALL_TABLES = (
    "role_permissions",
    "user_organization_roles",
    "audit_logs",
    "roles",
    "permissions",
    "users",
    "organizations",
)


@pytest.fixture(scope="session", autouse=True)
def _prepare_database():
    settings = Settings(database_url=TEST_DATABASE_URL, environment="development", jwt_secret="")
    reset_engine_cache()
    import app.core.config as config_module

    config_module.get_settings.cache_clear()
    import os

    os.environ["ZAYVORA_IDENTITY_DATABASE_URL"] = TEST_DATABASE_URL
    os.environ["ZAYVORA_IDENTITY_ENVIRONMENT"] = "development"
    config_module.get_settings.cache_clear()
    init_db()
    yield


@pytest.fixture(autouse=True)
def _clean_tables():
    """Truncate every table before each test so tests don't leak state
    into one another, without paying the cost of recreating the schema
    per test."""
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


@pytest.fixture()
def db_session():
    session_factory = get_session_factory()
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


def seed_org_role_permission(db_session, *, org_slug="clinic-1", role_name="Doctor", permission_codes=("patient.create",)):
    """Test helper: seeds an organization, a role, and permissions, then
    commits — mirrors what an admin bootstrap flow would do."""
    from app.models.identity import Organization, Permission, Role

    org = Organization(name="Clinic One", slug=org_slug, tier="clinic")
    db_session.add(org)
    db_session.flush()

    perms = []
    for code in permission_codes:
        perm = Permission(code=code, description=code)
        db_session.add(perm)
        perms.append(perm)
    db_session.flush()

    role = Role(organization_id=org.id, name=role_name, description=f"{role_name} role", permissions=perms)
    db_session.add(role)
    db_session.commit()
    db_session.refresh(org)
    db_session.refresh(role)
    return org, role
