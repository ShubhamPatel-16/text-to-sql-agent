from schema import get_relationships


relationships = get_relationships()

for relationship in relationships:
    child_table, child_column, parent_table, parent_column = relationship

    print(
        f"{child_table}.{child_column} "
        f"→ "
        f"{parent_table}.{parent_column}"
    )