from schema_retriever import get_schema_items


def build_table_documents() -> dict[str, str]:
    tables = get_schema_items()

    documents = {}

    for table_name, columns in tables.items():
        documents[table_name] = (
            f"Table: {table_name}. "
            f"Columns: {', '.join(columns)}."
        )

    return documents