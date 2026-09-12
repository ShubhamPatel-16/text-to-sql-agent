import re


FORBIDDEN_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "REPLACE",
    "TRUNCATE",
    "ATTACH",
    "DETACH",
}


def validate_sql(query: str) -> tuple[bool, str]:
    """
    Validate that a SQL query is a read-only SELECT query.

    Returns:
        (True, "OK") when the query is allowed.
        (False, reason) when the query is rejected.
    """

    cleaned_query = query.strip()

    if not cleaned_query:
        return False, "SQL query is empty"

    # Remove trailing semicolon(s)
    cleaned_query = cleaned_query.rstrip(";").strip()

    # Must begin with SELECT or WITH.
    # WITH is allowed because valid read-only queries can use CTEs.
    if not re.match(r"^(SELECT|WITH)\b", cleaned_query, re.IGNORECASE):
        return False, "Only SELECT or WITH queries are allowed"

    # Check for dangerous SQL keywords.
    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", cleaned_query, re.IGNORECASE):
            return False, f"Forbidden SQL keyword detected: {keyword}"

    return True, "OK"