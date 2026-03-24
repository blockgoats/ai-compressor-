"""Create tables (use Alembic for production migrations)."""

from sqlalchemy import create_engine

from app.core.config import get_settings
from app.db.base import Base

# Import models so metadata is populated
import app.models.tables  # noqa: F401


def main() -> None:
    settings = get_settings()
    engine = create_engine(settings.sync_database_url, echo=False)
    Base.metadata.create_all(bind=engine)
    print("Database tables ensured.")


if __name__ == "__main__":
    main()
