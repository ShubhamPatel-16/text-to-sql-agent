from src.sql_executor import execute_sql


def test_execute_select():
    result = execute_sql("SELECT 1")

    assert result == [(1,)]