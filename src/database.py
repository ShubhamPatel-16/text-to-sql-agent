import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).parent.parent / "database" / "ecommerce.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(
        f"file:{DB_PATH}?mode=ro",
        uri=True,
    )

    return connection