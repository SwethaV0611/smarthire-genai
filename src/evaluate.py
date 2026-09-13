import os

from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume

from src.search.job_search import search_jobs

from src.mentor.rag_chain import (
    ask_career_mentor,
    retrieve_context
)


# ============================================================
# CONFIGURATION
# ============================================================

RESUME_PATHS = [
    "data/resumes/resume1.pdf",
    "data/resumes/resume2.pdf",
    "data/resumes/resume3.docx",
    "data/resumes/resume4.pdf",
    "data/resumes/resume5.docx"
]


MENTOR_QUESTIONS = [
    "What skills are important for a Data Scientist?",
    "What skills should I learn for a Software Engineer role?",
    "What skills are useful for a Machine Learning Engineer?",
    "How can I improve my career skills?"
]


OUT_OF_SCOPE_QUESTION = (
    "What is the weather today?"
)


# ============================================================
# EVALUATION RESULT STORAGE
# ============================================================

retrieval_results = []
mentor_results = []
guardrail_results = []


# ============================================================
# RETRIEVAL RELEVANCE EVALUATION
# ============================================================

def evaluate_job_retrieval():

    print("\n")
    print("=" * 60)
    print("JOB RETRIEVAL RELEVANCE EVALUATION")
    print("=" * 60)

    total = 0
    relevant = 0

    for resume_path in RESUME_PATHS:

        if not os.path.exists(resume_path):

            print(
                f"\nSkipping missing file: {resume_path}"
            )

            continue

        try:

            chunks = load_resume(
                resume_path
            )

            resume_text = "\n".join(
                chunks
            )

            profile = parse_resume(
                resume_text
            )

            results = search_jobs(
                profile,
                top_n=5
            )

            total += 1

            print("\nResume:")
            print(
                os.path.basename(resume_path)
            )

            print(
                "Target Role:",
                profile.get(
                    "target_role",
                    ""
                )
            )

            print("\nTop Jobs:")

            for i, job in enumerate(
                results,
                start=1
            ):

                print(
                    f"{i}. {job['title']} "
                    f"({job['similarity_score']}%)"
                )

            # --------------------------------------------
            # Manual relevance decision
            # --------------------------------------------

            print(
                "\nIs the top result relevant?"
            )

            decision = input(
                "Enter Y/N: "
            ).strip().upper()

            if decision == "Y":

                relevant += 1

                result = "Yes"

            else:

                result = "No"

            retrieval_results.append({
                "resume": os.path.basename(
                    resume_path
                ),
                "target_role": profile.get(
                    "target_role",
                    ""
                ),
                "top_job": (
                    results[0]["title"]
                    if results
                    else "None"
                ),
                "relevant": result
            })

        except Exception as e:

            print(
                f"Error evaluating {resume_path}: {e}"
            )


    # --------------------------------------------
    # Hit Rate
    # --------------------------------------------

    if total > 0:

        hit_rate = (
            relevant / total
        ) * 100

    else:

        hit_rate = 0


    print("\n")
    print("-" * 60)
    print(
        f"Retrieval Hit Rate: "
        f"{hit_rate:.2f}%"
    )
    print("-" * 60)

    return hit_rate


# ============================================================
# MENTOR ANSWER EVALUATION
# ============================================================

def evaluate_mentor_answers():

    print("\n")
    print("=" * 60)
    print("AI CAREER MENTOR EVALUATION")
    print("=" * 60)

    for question in MENTOR_QUESTIONS:

        print("\n")
        print("QUESTION:")
        print(question)

        # --------------------------------------------
        # Retrieve context
        # --------------------------------------------

        context = retrieve_context(
            question,
            top_k=5
        )

        print(
            f"\nRetrieved Sources: "
            f"{len(context)}"
        )

        for document in context:

            print(
                f"- {document['source']}"
            )

        # --------------------------------------------
        # Generate answer
        # --------------------------------------------

        answer = ask_career_mentor(
            question
        )

        print("\nANSWER:")
        print(answer)

        # --------------------------------------------
        # Manual evaluation
        # --------------------------------------------

        print("\nEvaluation:")

        correctness = input(
            "Correctness (1-5): "
        ).strip()

        grounding = input(
            "Grounding (1-5): "
        ).strip()

        helpfulness = input(
            "Helpfulness (1-5): "
        ).strip()

        mentor_results.append({
            "question": question,
            "correctness": correctness,
            "grounding": grounding,
            "helpfulness": helpfulness
        })


# ============================================================
# HALLUCINATION / OUT-OF-SCOPE TEST
# ============================================================

def evaluate_guardrails():

    print("\n")
    print("=" * 60)
    print("HALLUCINATION / GUARDRAIL EVALUATION")
    print("=" * 60)

    question = OUT_OF_SCOPE_QUESTION

    print("\nQuestion:")
    print(question)

    answer = ask_career_mentor(
        question
    )

    print("\nSystem Response:")
    print(answer)

    if (
        "outside the scope" in answer.lower()
        or "career" in answer.lower()
        or "available career information" in answer.lower()
    ):

        result = "PASS"

    else:

        result = "CHECK MANUALLY"

    guardrail_results.append({
        "question": question,
        "response": answer,
        "result": result
    })

    print(
        f"\nGuardrail Test: {result}"
    )


# ============================================================
# GENERATE REPORT
# ============================================================

def generate_report(
    hit_rate
):

    os.makedirs(
        "reports",
        exist_ok=True
    )

    report_path = (
        "reports/answer_quality.md"
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "# SmartHire GenAI - Evaluation Report\n\n"
        )

        file.write(
            "## 1. Retrieval Relevance\n\n"
        )

        file.write(
            f"**Retrieval Hit Rate:** "
            f"{hit_rate:.2f}%\n\n"
        )

        file.write(
            "| Resume | Target Role | "
            "Top Job | Relevant |\n"
        )

        file.write(
            "|---|---|---|---|\n"
        )

        for result in retrieval_results:

            file.write(
                f"| {result['resume']} | "
                f"{result['target_role']} | "
                f"{result['top_job']} | "
                f"{result['relevant']} |\n"
            )


        file.write(
            "\n## 2. Mentor Answer Quality\n\n"
        )

        file.write(
            "| Question | Correctness "
            "| Grounding | Helpfulness |\n"
        )

        file.write(
            "|---|---:|---:|---:|\n"
        )

        for result in mentor_results:

            file.write(
                f"| {result['question']} | "
                f"{result['correctness']} | "
                f"{result['grounding']} | "
                f"{result['helpfulness']} |\n"
            )


        file.write(
            "\n## 3. Hallucination / Guardrail Test\n\n"
        )

        file.write(
            "| Question | Result |\n"
        )

        file.write(
            "|---|---|\n"
        )

        for result in guardrail_results:

            file.write(
                f"| {result['question']} | "
                f"{result['result']} |\n"
            )


        file.write(
            "\n## 4. Prompt Comparison\n\n"
        )

        file.write(
            "A before/after prompt comparison should "
            "be added after testing the original and "
            "improved prompts.\n\n"
        )

        file.write(
            "**Before Prompt:**\n\n"
        )

        file.write(
            "Describe the original prompt used.\n\n"
        )

        file.write(
            "**Before Output:**\n\n"
        )

        file.write(
            "Paste the original model output.\n\n"
        )

        file.write(
            "**After Prompt:**\n\n"
        )

        file.write(
            "Describe the improved prompt.\n\n"
        )

        file.write(
            "**After Output:**\n\n"
        )

        file.write(
            "Paste the improved model output.\n\n"
        )

        file.write(
            "## 5. Observations\n\n"
        )

        file.write(
            "- Evaluate whether retrieved jobs "
            "are relevant to candidate profiles.\n"
        )

        file.write(
            "- Check whether mentor answers stay "
            "grounded in the knowledge base.\n"
        )

        file.write(
            "- Check whether unsupported questions "
            "are rejected appropriately.\n"
        )

        file.write(
            "- Record limitations and possible "
            "future improvements.\n"
        )


    print(
        f"\nEvaluation report created: "
        f"{report_path}"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 60)
    print("       SMART HIRE GENAI EVALUATION")
    print("=" * 60)

    hit_rate = evaluate_job_retrieval()

    evaluate_mentor_answers()

    evaluate_guardrails()

    generate_report(
        hit_rate
    )

    print("\n")
    print("=" * 60)
    print("       EVALUATION COMPLETED")
    print("=" * 60)