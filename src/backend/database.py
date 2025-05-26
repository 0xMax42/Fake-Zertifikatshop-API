from sqlmodel import SQLModel, create_engine, Session
from typing import Optional
from sqlalchemy.engine import Engine

# The default URL for the SQLite database file (used in production).
DATABASE_URL = "sqlite:///./products.db"

# Creates a global SQLAlchemy engine for the application.
engine = create_engine(DATABASE_URL, echo=True)


def init_db(custom_engine: Optional[Engine] = None) -> None:
    """
    Initializes the database by creating all tables defined in the SQLModel metadata.

    Args:
        custom_engine (Optional[Engine]): A custom SQLAlchemy engine to use for table creation.
                                          If not provided, the default engine is used.
                                          This is useful for testing with in-memory databases.
    """
    SQLModel.metadata.create_all(custom_engine or engine)


def get_session() -> Session:
    """
    Provides a new SQLModel session connected to the default database engine.

    Returns:
        Session: A session object bound to the default database engine.
    """
    return Session(engine)
