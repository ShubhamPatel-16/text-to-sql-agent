import os
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = PROJECT_ROOT / "database" / "ecommerce.db"


def get_connection(db_path=None):
    selected_path = Path(
        db_path or os.getenv("TEXT_TO_SQL_DB_PATH", DEFAULT_DB_PATH)
    )

    connection = sqlite3.connect(
        f"file:{selected_path}?mode=ro",
        uri=True,
    )

    return connection