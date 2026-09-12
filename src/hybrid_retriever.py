import re

from schema import get_schema
from schema_retriever import get_schema_items
from semantic_retriever import model, expand_with_relationships


def normalize_words(text: str) -> set[str]:
    words = re.findall(
        r"[a-zA-Z_]+",
        text.lower(),
    )

    normalized = set()

    for word in words:
        normalized.add(word)

        if "_" in word:
            normalized.update(word.split("_"))

    return normalized


def retrieve_hybrid_schema(
    question: str,
    top_k: int = 3,
) -> str:

    tables = get_schema_items()

    question_words = normalize_words(question)

    documents = {}

    for table_name, columns in tables.items():
        documents[table_name] = (
            f"Table: {table_name}. "
            f"Columns: {', '.join(columns)}."
        )

    document_names = list(documents.keys())
    document_texts = list(documents.values())

    # Semantic scores
    question_embedding = model.encode(
        question,
        normalize_embeddings=True,
    )

    document_embeddings = model.encode(
        document_texts,
        normalize_embeddings=True,
    )

    semantic_scores = document_embeddings @ question_embedding

    ranked = []

    for index, table_name in enumerate(document_names):

        schema_words = normalize_words(
            table_name + " " + " ".join(tables[table_name])
        )

        keyword_matches = len(
            question_words & schema_words
        )

        semantic_score = float(
            semantic_scores[index]
        )

        # Simple hybrid score.
        combined_score = (
            0.4 * keyword_matches
            + 0.6 * semantic_score
        )

        ranked.append(
            (table_name, combined_score)
        )

    ranked.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    selected_tables = {
        table_name
        for table_name, _ in ranked[:top_k]
    }

    selected_tables = expand_with_relationships(
        selected_tables
    )

    full_schema = get_schema()

    result = []
    include_table = False

    for line in full_schema.splitlines():

        if line.startswith("Table: "):
            table_name = line.replace(
                "Table: ",
                "",
            ).strip()

            include_table = (
                table_name in selected_tables
            )

        if include_table:
            result.append(line)

    return "\n".join(result)