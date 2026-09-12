import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from evaluate import QUESTION_FILE, load_questions, normalize_sql


def test_question_file_and_loader_shape():
    assert QUESTION_FILE.exists()
    questions = load_questions()
    assert isinstance(questions, list)
    assert questions


def test_normalize_sql_reduces_whitespace_and_semicolons():
    sql = "  SELECT   * FROM  customers ;  "
    assert normalize_sql(sql) == "SELECT * FROM customers"
