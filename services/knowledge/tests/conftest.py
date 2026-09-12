"""
IMPORTANT: by default these fixtures inject InMemoryGraphRepository, not a
real Neo4j connection — see the module-level explanation this originally
shipped with in docs/PHASE2-KNOWLEDGE-CORE.md.

To run this EXACT SAME test suite against a real Neo4j instance instead
(recommended before trusting this service — do this on a machine with
Docker/internet, e.g. not the sandbox this was built in):

    cd infrastructure && docker compose up -d neo4j
    cd ../services/knowledge
    export ZAYVORA_KNOWLEDGE_TEST_USE_REAL_NEO4J=1
    export ZAYVORA_KNOWLEDGE_NEO4J_URI=bolt://localhost:7687
    export ZAYVORA_KNOWLEDGE_NEO4J_PASSWORD=zayvora_dev_password
    .venv/bin/pytest -q

If ZAYVORA_KNOWLEDGE_TEST_USE_REAL_NEO4J is unset (the default), tests use
the fake and this file's docstring caveat applies. If it's set, tests run
against Neo4jGraphRepository for real — same 27 tests, same assertions,
just proving the actual Cypher instead of the fake's Python logic. A
_clean_graph fixture wipes the test data before each test either way, so
running against real Neo4j is safe to repeat.
"""
import os
import uuid

import jwt
import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.core.taxonomy import ORGAN_AXES
from app.graph.fake_repository import InMemoryGraphRepository
from app.main import create_app

USE_REAL_NEO4J = os.environ.get("ZAYVORA_KNOWLEDGE_TEST_USE_REAL_NEO4J") == "1"

TEST_JWT_SECRET_FALLBACK = "development-only-insecure-secret-do-not-use-in-production"

ALL_KNOWLEDGE_PERMISSIONS = [
    "pharmacopoeia.read",
    "pharmacopoeia.write",
    "evidence.read",
    "evidence.write",
]


def make_token(*, organization_id: str | None = None, permissions=None) -> str:
    payload = {
        "sub": str(uuid.uuid4()),
        "org": organization_id or str(uuid.uuid4()),
        "roles": ["Doctor"],
        "permissions": permissions if permissions is not None else ALL_KNOWLEDGE_PERMISSIONS,
        "iat": 0,
        "exp": 9999999999,
    }
    return jwt.encode(payload, TEST_JWT_SECRET_FALLBACK, algorithm="HS256")


@pytest.fixture()
def graph_repo():
    if USE_REAL_NEO4J:
        from app.graph.neo4j_repository import Neo4jGraphRepository

        settings = Settings(environment="development", jwt_secret="")
        repo = Neo4jGraphRepository(settings.neo4j_uri, settings.neo4j_user, settings.neo4j_password)
        repo.verify_connectivity()  # fails loudly and immediately if Neo4j isn't reachable
        repo.wipe_all_data()  # start each test from a clean graph
        repo.seed_organ_axes(ORGAN_AXES)
        yield repo
        repo.close()
    else:
        yield InMemoryGraphRepository(seed_axes=ORGAN_AXES)


@pytest.fixture()
def app(graph_repo):
    settings = Settings(environment="development", jwt_secret="")
    return create_app(settings=settings, graph_repository=graph_repo)


@pytest.fixture()
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def org_id():
    return str(uuid.uuid4())


@pytest.fixture()
def auth_headers(org_id):
    return {"Authorization": f"Bearer {make_token(organization_id=org_id)}"}


@pytest.fixture()
def other_org_headers():
    return {"Authorization": f"Bearer {make_token()}"}
