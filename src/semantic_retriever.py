from schema import get_schema
from schema_index import build_table_documents
from sentence_transformers import SentenceTransformer

from schema_retriever import expand_with_relationships


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def retrieve_semantic_schema(
    question: str,
    top_k: int = 3,
) -> str:
    documents = build_table_documents()

    document_names = list(documents.keys())
    document_texts = list(documents.values())

    question_embedding = model.encode(
        question,
        normalize_embeddings=True,
    )

    document_embeddings = model.encode(
        document_texts,
        normalize_embeddings=True,
    )

    similarities = document_embeddings @ question_embedding

    ranked = sorted(
        zip(document_names, similarities),
        key=lambda item: item[1],
        reverse=True,
    )

    selected_tables = {
        table_name
        for table_name, _ in ranked[:top_k]
    }
    selected_tables = expand_with_relationships(selected_tables)

    full_schema = get_schema()

    result = []
    include_table = False

    for line in full_schema.splitlines():
        if line.startswith("Table: "):
            table_name = line.replace("Table: ", "").strip()
            include_table = table_name in selected_tables

        if include_table:
            result.append(line)

    return "\n".join(result)