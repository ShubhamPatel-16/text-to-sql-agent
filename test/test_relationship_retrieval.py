from src.semantic_retriever import expand_with_relationships


def test_related_tables_are_added():
    selected_tables = {"customers"}

    expanded = expand_with_relationships(selected_tables)

    assert "customers" in expanded
    assert "orders" in expanded