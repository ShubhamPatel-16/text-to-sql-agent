import argparse
import json
import os
from collections import Counter
from pathlib import Path

from database import get_connection
from sql_validator import validate_sql


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SPIDER_DATA_FILE = PROJECT_ROOT / "benchmark_data" / "spider" / "dev.json"
SPIDER_DATABASE_DIR = PROJECT_ROOT / "benchmark_data" / "spider" / "database"
FLOAT_PRECISION = 6


def load_spider_examples(data_file: Path = SPIDER_DATA_FILE) -> list[dict]:
    if not data_file.exists():
        raise FileNotFoundError(f"Spider dev file not found: {data_file}")

    with data_file.open("r", encoding="utf-8") as file:
        examples = json.load(file)

    if not isinstance(examples, list):
        raise ValueError(f"Expected a list of Spider examples in {data_file}")

    return examples


def get_spider_db_path(db_id: str, database_dir: Path = SPIDER_DATABASE_DIR) -> Path:
    db_path = database_dir / db_id / f"{db_id}.sqlite"

    if not db_path.exists():
        raise FileNotFoundError(
            f"SQLite database not found for db_id '{db_id}': {db_path}"
        )

    return db_path


def execute_validated_sql(sql: str):
    valid, message = validate_sql(sql)

    if not valid:
        raise ValueError(f"Unsafe SQL rejected: {message}")

    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()


def normalize_value(value):
    if isinstance(value, float):
        return round(value, FLOAT_PRECISION)

    return value


def normalize_row(row):
    return tuple(normalize_value(value) for value in row)


def normalize_result(result):
    return Counter(normalize_row(row) for row in result)


def compare_results(generated_result, gold_result) -> bool:
    return normalize_result(generated_result) == normalize_result(gold_result)


def evaluate_examples(examples: list[dict]) -> tuple[int, int]:
    if not examples:
        return 0, 0

    from text_to_sql import answer_question

    correct_count = 0

    for index, example in enumerate(examples, start=1):
        db_id = example["db_id"]
        question = example["question"]
        gold_sql = example["query"]
        db_path = get_spider_db_path(db_id)

        print(f"{index}. [{db_id}] {question}")

        previous_db_path = os.environ.get("TEXT_TO_SQL_DB_PATH")
        os.environ["TEXT_TO_SQL_DB_PATH"] = str(db_path)

        try:
            generated_result = answer_question(question)
            gold_result = execute_validated_sql(gold_sql)

            if compare_results(generated_result, gold_result):
                correct_count += 1
                print("Result: correct")
            else:
                print("Result: incorrect")
                print(f"Gold SQL: {gold_sql}")
                print(f"Expected: {gold_result}")
                print(f"Actual: {generated_result}")

        except Exception as exc:
            print("Result: ERROR")
            print(f"Error: {exc}")

        finally:
            if previous_db_path is None:
                os.environ.pop("TEXT_TO_SQL_DB_PATH", None)
            else:
                os.environ["TEXT_TO_SQL_DB_PATH"] = previous_db_path

        print()

    return correct_count, len(examples)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Evaluate execution accuracy on Spider dev examples."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Evaluate only the first N Spider dev examples.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    examples = load_spider_examples()

    if args.limit is not None:
        if args.limit < 0:
            raise ValueError("--limit must be non-negative")

        examples = examples[: args.limit]

    correct_count, total = evaluate_examples(examples)
    accuracy = (correct_count / total) * 100 if total else 0

    print(f"Execution accuracy: {accuracy:.2f}% ({correct_count}/{total})")


if __name__ == "__main__":
    main()
