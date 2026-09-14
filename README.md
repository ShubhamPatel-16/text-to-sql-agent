# Text-to-SQL Agent

Turn a question written in plain English into a SQL query — and get the answer directly from a database.

I built this project to understand what actually happens behind a Text-to-SQL system instead of just sending a prompt to an LLM and executing whatever it returns.

The main challenge I focused on was **schema management**: how do you give an LLM enough information about a database without dumping the entire schema into its context every time?

---

## What it does

You can ask questions like:

```text
How many customers are there?

Which customer spent the most money on orders?

Which product has been ordered in the highest quantity?
```

The system then:

```text
Question
   ↓
Find relevant database schema
   ↓
Generate SQL with Groq
   ↓
Validate the SQL
   ↓
Execute it in read-only mode
   ↓
Return the result
```

So this is better described as a **Text-to-SQL agent** rather than a chatbot. A chat interface could be added later, but the main focus here is the reasoning and database pipeline behind it.

---

## Why I built it this way

A simple approach would be to give the LLM the complete database schema every time.

That works for a small database, but it doesn't scale well.

Real databases can contain hundreds of tables and thousands of columns. Sending all of that to the model increases the amount of context and makes it harder for the model to focus on the relevant information.

So I experimented with different ways of retrieving only the useful parts of the schema.

---

## Key features

### Hybrid schema retrieval

The agent combines:

* keyword-based matching
* semantic similarity
* foreign-key relationships

This helps it identify which tables are relevant to a question.

For example, a question about:

```text
Which customer spent the most money?
```

may require:

```text
customers
   ↓
orders
   ↓
products
```

The relationship-aware retrieval step helps bring those connected tables into the model context.

### SQL validation

Generated SQL is checked before execution.

The validator only allows read-style queries such as:

```sql
SELECT ...
```

and:

```sql
WITH ...
```

Queries containing write or schema-changing operations are rejected.

### Read-only database execution

The SQLite connection itself is opened in read-only mode.

That gives the system another safety boundary between generated SQL and the actual database.

### Execution-based evaluation

I evaluate the generated query by executing it and comparing the returned result against the expected database result.

This is more useful than simply comparing generated SQL strings, because multiple SQL queries can produce the same correct answer.

---

## Evaluation

### Local evaluation

I created a small evaluation set using my own ecommerce database.

It contains questions covering:

* filtering
* sorting
* aggregation
* joins
* grouping
* multi-table queries
* calculations

### Spider 1.0

I also tested the agent on a **100-question sample of the Spider 1.0 development set**.

**Execution accuracy: 74.00% (74/100)**

This is the result for the evaluated 100-question sample, not the complete Spider development set.

---

## Tech stack

* **Python**
* **Groq** for LLM-based SQL generation
* **SQLite** for database execution
* **Sentence Transformers** for semantic schema retrieval
* **Pytest** for testing

---

## Project structure

```text
text-to-sql/
│
├── database/
│   └── ecommerce.db
│
├── src/
│   ├── app.py
│   ├── database.py
│   ├── embedding.py
│   ├── evaluate.py
│   ├── evaluate_spider.py
│   ├── hybrid_retriever.py
│   ├── llm.py
│   ├── main.py
│   ├── schema.py
│   ├── schema_index.py
│   ├── schema_retriever.py
│   ├── semantic_retriever.py
│   ├── show_relationships.py
│   ├── sql_executor.py
│   ├── sql_validator.py
│   └── text_to_sql.py
│
├── test/
│
├── benchmark/
│   └── spider/
│
├── benchmark_results/
│   └── spider_dev_results.txt
│
├── pytest.ini
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Getting started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd text-to-sql
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

The `.env` file is ignored by Git and should never be committed.

### 5. Run the agent

```bash
python src/main.py
```

You can then enter a natural-language question about the ecommerce database.

Example:

```text
Ask a question about the database: How many customers are there?
```

---

## Running tests

Run the project test suite with:

```bash
python -m pytest
```

---

## Running the Spider evaluation

The Spider dataset is kept outside version control.

To run the benchmark evaluator:

```bash
python src/evaluate_spider.py --limit 100
```

The evaluator reads Spider questions, loads the corresponding database, generates SQL, validates it, executes it, and compares the result with the gold query result.

---

## What I learned from this project

The biggest lesson for me was that building a Text-to-SQL system is not just about getting an LLM to write SQL.

The harder part is everything around the LLM:

* giving it the right schema
* handling table relationships
* validating generated SQL
* keeping database execution read-only
* evaluating whether the generated query actually answers the question

That is where most of the engineering work in this project went.

---

## Limitations

This is still a lightweight implementation.

The current system can struggle with more complex natural-language questions and larger schemas. The hybrid retrieval strategy is also fairly simple and can be improved further.

The Spider result is based on a **100-question sample** rather than the complete development set.

---

## Possible next improvements

Some things I'd explore next:

* run evaluation on the complete Spider development set
* add bounded SQL error recovery and retries
* improve schema retrieval for multi-hop relationships
* measure latency and token usage
* add a natural-language explanation of query results
* support additional SQL dialects

---

## License

MIT
