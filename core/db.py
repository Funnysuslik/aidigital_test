from collections.abc import Generator

from sqlmodel import Session, create_engine

from core.settings import settings

engine = create_engine(str(settings.DATABASE_URI))


def get_db() -> Generator[Session, None, None]:
    """Get a database session."""
    with Session(engine) as session:
        yield session
