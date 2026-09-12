from llm import generate_sql


schema = """
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
"""


question = "Which customer has placed the most orders?"
sql = generate_sql(question, schema)

print("\nGenerated SQL:")
print(sql)