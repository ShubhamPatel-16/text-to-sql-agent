from database import get_connection

def execute_sql(query: str):
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        conn.close()