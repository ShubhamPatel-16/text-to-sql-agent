from src.sql_validator import validate_sql


def test_select_is_allowed():
    valid, message = validate_sql(
        "SELECT * FROM customers;"
    )

    assert valid is True
    assert message == "OK"


def test_with_query_is_allowed():
    valid, message = validate_sql(
        """
        WITH customer_orders AS (
            SELECT customer_id, COUNT(*) AS order_count
            FROM orders
            GROUP BY customer_id
        )
        SELECT * FROM customer_orders;
        """
    )

    assert valid is True
    assert message == "OK"


def test_delete_is_rejected():
    valid, message = validate_sql(
        "DELETE FROM customers;"
    )

    assert valid is False


def test_drop_is_rejected():
    valid, message = validate_sql(
        "DROP TABLE customers;"
    )

    assert valid is False


def test_update_is_rejected():
    valid, message = validate_sql(
        "UPDATE customers SET name='x';"
    )

    assert valid is False


def test_insert_is_rejected():
    valid, message = validate_sql(
        "INSERT INTO customers VALUES (1, 'Alice', 'a@example.com');"
    )

    assert valid is False