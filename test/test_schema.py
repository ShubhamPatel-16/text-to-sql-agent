from src.schema import get_schema


def test_schema_contains_tables():
    schema = get_schema()

    assert "customers" in schema
    assert "orders" in schema
    assert "products" in schema


def test_schema_contains_columns():
    schema = get_schema()

    assert "id" in schema
    assert "customer_id" in schema
    assert "price" in schema