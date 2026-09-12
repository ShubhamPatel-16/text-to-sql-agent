import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is not set in the .env file")

client = Groq(api_key=api_key)


def generate_sql(question: str, schema: str) -> str:
    prompt =prompt = f"""
You are a SQL generator.

Convert the user's question into a SQLite SQL query.

Database schema:
{schema}

User question:
{question}

Rules:
1. Return only the SQL query.
2. Select only the columns necessary to answer the user's question.
3. Do not use SELECT * unless the question explicitly asks for all columns.
4. Do not include identifier columns such as IDs unless they are requested.
5. Use the table and column names exactly as provided in the schema.
6. Prefer clear and simple SQL.
"""

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
    )

    return response.choices[0].message.content.strip()