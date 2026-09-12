from semantic_retriever import retrieve_semantic_schema


questions = [
    "Which customer spent the most money?",
    "What products are the most expensive?",
    "How many orders were placed?",
]

for question in questions:
    print(f"\nQuestion: {question}")

    results = retrieve_semantic_schema(question)

    for table, score in results:
        print(f"{table}: {score:.4f}")