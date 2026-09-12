from text_to_sql import answer_question


question = input("Ask a question about the database: ")

result = answer_question(question)

print("\nQuery result:")
print(result)

