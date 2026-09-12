from llm import generate_sql
from sql_executor import execute_sql
from sql_validator import validate_sql
from schema_retriever import retrieve_schema
from hybrid_retriever import retrieve_hybrid_schema
# from semantic_retriever import retrieve_semantic_schema



SCHEMA = """
customers(
    id INTEGER,
    name TEXT,
    email TEXT
)

orders(
    id INTEGER,
    customer_id INTEGER,
    amount REAL
)

products(
    id INTEGER,
    name TEXT,
    price REAL
)
"""


def answer_question(question: str):
    # schema = retrieve_semantic_schema(question)  
    schema = retrieve_hybrid_schema(question)  
    print("\nRetrieved schema:")
    print(schema)

    sql = generate_sql(question, schema)

    print("\nGenerated SQL:")
    print(sql)


    valid, message = validate_sql(sql)

    if not valid:
        raise ValueError(f"Unsafe SQL rejected: {message}")

    # result = execute_sql(sql)

    return execute_sql(sql)