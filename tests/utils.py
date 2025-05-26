import os
from sqlalchemy.engine import Engine


def cleanup_database(engine: Engine, path: str):
    """
    Disposes the engine and deletes the SQLite database file.

    Args:
        engine (Engine): The SQLAlchemy engine to dispose.
        path (str): The path to the SQLite database file to remove.
    """
    # Close all connections and dispose the engine
    engine.dispose()

    # Remove the SQLite database file if it exists
    if os.path.exists(path):
        os.remove(path)
