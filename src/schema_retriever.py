import re

from schema import get_schema
from schema import get_relationships


def get_schema_items() -> dict[str, list[str]]:
    """
    Convert the database schema into:

    {
        "customers": ["id", "name", "email"],
        "orders": ["id", "customer_id", "amount"],
        ...
    }
    """
    schema = get_schema()

    tables: dict[str, list[str]] = {}
    current_table = None

    for line in schema.splitlines():
        line = line.strip()

        if line.startswith("Table: "):
            current_table = line.replace("Table: ", "").strip()
            tables[current_table] = []

        elif line.startswith("- ") and current_table:
            column_name = line[2:].split(" (", 1)[0].strip()
            tables[current_table].append(column_name)

    return tables


def normalize_words(text: str) -> set[str]:
    """
    Convert text into simple searchable words.
    """
    words = re.findall(r"[a-zA-Z_]+", text.lower())

    normalized = set()

    for word in words:
        normalized.add(word)

        # Also split snake_case words.
        if "_" in word:
            normalized.update(word.split("_"))

    return normalized


def retrieve_schema(question: str) -> str:
    """
    Retrieve tables whose names or columns have words
    matching the user's question.
    """
    tables = get_schema_items()
    question_words = normalize_words(question)

    selected_tables = []

    for table_name, columns in tables.items():
        searchable_text = " ".join([table_name] + columns)
        schema_words = normalize_words(searchable_text)

        if question_words & schema_words:
            selected_tables.append(table_name)

    # Baseline fallback:
    # if nothing matched, return the complete schema.
    if not selected_tables:
        return get_schema()

    full_schema = get_schema()
    result = []

    include_table = False

    for line in full_schema.splitlines():
        if line.startswith("Table: "):
            table_name = line.replace("Table: ", "").strip()
            include_table = table_name in selected_tables

        if include_table:
            result.append(line)

    return "\n".join(result)


def expand_with_relationships(
    selected_tables: set[str],
) -> set[str]:
    relationships = get_relationships()

    expanded_tables = set(selected_tables)

    for (
        child_table,
        child_column,
        parent_table,
        parent_column,
    ) in relationships:

        if child_table in selected_tables:
            expanded_tables.add(parent_table)

        if parent_table in selected_tables:
            expanded_tables.add(child_table)

    return expanded_tables