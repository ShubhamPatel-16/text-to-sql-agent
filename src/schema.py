from database import get_connection

def get_schema() -> str:
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
        """)

        tables = [row[0] for row in cursor.fetchall()]

        schema_parts = []

        for table in tables:
            cursor.execute(f"PRAGMA table_info('{table}')")
            columns = cursor.fetchall()

            schema_parts.append(f"Table: {table}")

            for column in columns:
                # PRAGMA table_info:
                # cid, name, type, notnull, default_value, pk
                column_name = column[1]
                column_type = column[2]

                schema_parts.append(
                    f"  - {column_name} ({column_type})"
                )

            schema_parts.append("")

        return "\n".join(schema_parts)
    

    finally:
        conn.close()

def get_relationships() -> list[tuple[str, str, str, str]]:
    """
    Return foreign-key relationships as:

    (child_table, child_column, parent_table, parent_column)
    """
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
        """)

        tables = [row[0] for row in cursor.fetchall()]

        relationships = []

        for table in tables:
            cursor.execute(f"PRAGMA foreign_key_list('{table}')")

            for row in cursor.fetchall():
                # PRAGMA foreign_key_list:
                # id, seq, table, from, to, on_update, on_delete, ...
                parent_table = row[2]
                child_column = row[3]
                parent_column = row[4]

                relationships.append(
                    (
                        table,
                        child_column,
                        parent_table,
                        parent_column,
                    )
                )

        return relationships

    finally:
        conn.close()