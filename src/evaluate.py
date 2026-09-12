import json
import re
from pathlib import Path

from text_to_sql import answer_question

PROJECT_ROOT = Path(__file__).resolve().parents[1]
QUESTION_FILE = PROJECT_ROOT / "test" / "evaluation" / "questions.json"


def load_questions():
    if not QUESTION_FILE.exists():
        raise FileNotFoundError(
            f"Evaluation questions file not found: {QUESTION_FILE}"
        )

    with QUESTION_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def normalize_sql(sql: str) -> str:
    """Collapse whitespace and remove the trailing SQL statement terminator."""
    normalized = re.sub(r"\s+", " ", sql.strip())
    normalized = normalized.strip(";").strip()
    return normalized


def normalize_value(value):
    if isinstance(value, float):
        return round(value, 6)
    return value


def normalize_result(result):
    normalized = []

    for row in result:
        normalized_row = tuple(normalize_value(value) for value in row)
        normalized.append(normalized_row)

    return normalized


def compare_results(actual, expected):
    actual_normalized = normalize_result(actual)
    expected_normalized = normalize_result(expected)
    return actual_normalized == expected_normalized


def main():
    questions = load_questions()

    correct_count = 0

    for index, item in enumerate(questions, start=1):
        question = item["question"]
        expected_result = item["expected_result"]

        print(f"{index}. {question}")

        try:
            actual_result = answer_question(question)

            if compare_results(actual_result, expected_result):
                correct_count += 1
                print("Result: correct")
            else:
                print("Result: incorrect")
                print(f"Expected: {expected_result}")
                print(f"Actual: {actual_result}")

        except Exception as exc:
            print("Result: ERROR")
            print(f"Error: {exc}")

        print()

    total = len(questions)
    accuracy = (correct_count / total) * 100 if total else 0

    print(f"Accuracy: {accuracy:.2f}% ({correct_count}/{total})")


if __name__ == "__main__":
    main()
