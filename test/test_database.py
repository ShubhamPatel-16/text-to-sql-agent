from src.database import get_connection


def test_database_connection():
    conn = get_connection()

    cursor = conn.cursor()
    cursor.execute("SELECT 1")

    result = cursor.fetchone()

    conn.close()

    assert result == (1,)