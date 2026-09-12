from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings
from app.models.identity import Base

_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)
    return _engine


def get_session_factory() -> sessionmaker:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine(), autoflush=False, autocommit=False, future=True)
    return _SessionLocal


def init_db() -> None:
    """Create all tables. In production this should be replaced by Alembic
    migrations (see database/migrations/) — this exists for local dev and
    for the test suite's isolated SQLite databases."""
    Base.metadata.create_all(bind=get_engine())


def get_db() -> Generator[Session, None, None]:
    session_factory = get_session_factory()
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


def reset_engine_cache() -> None:
    """Test-only helper: forces get_engine()/get_session_factory() to
    rebuild against whatever DATABASE_URL is current, so each test can
    point at its own isolated database."""
    global _engine, _SessionLocal
    _engine = None
    _SessionLocal = None
