from src.mentor.rag_chain import ask_career_mentor


print("\n================================")
print("     SMART HIRE AI MENTOR")
print("================================\n")


questions = [
    "What skills are important for a Data Scientist?",
    "What skills should I learn for a Software Engineer role?",
    "What skills are useful for a Machine Learning Engineer?"
]


for question in questions:

    print("QUESTION:")
    print(question)

    answer = ask_career_mentor(
        question
    )

    print("\nANSWER:")
    print(answer)

    print("\n" + "-" * 60 + "\n")