from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume

from src.search.job_search import (
    load_faiss_database,
    search_jobs
)

from src.generate.cv_suggestions import (
    generate_cv_suggestions
)


# Resume to test
resume_path = "data/resumes/resume3.docx"


# Load resume
chunks = load_resume(resume_path)

resume_text = "\n".join(chunks)


# Parse resume
profile = parse_resume(resume_text)


print("\n===== CANDIDATE =====")
print(profile["name"])

print("\n===== TARGET ROLE =====")
print(profile["target_role"])


# Find matching jobs
results = search_jobs(
    profile,
    top_n=1
)


if not results:
    raise ValueError(
        "No matching job found."
    )


# Select best matching job
best_job = results[0]


job_text = (
    f"Job Title: {best_job['title']}\n"
    f"Skills: {best_job['skills']}\n"
    f"Description: {best_job['description']}"
)


print("\n===== TARGET JOB =====")
print(best_job["title"])


# Generate suggestions
suggestions = generate_cv_suggestions(
    resume_text,
    job_text
)


print("\n===== CV IMPROVEMENT SUGGESTIONS =====\n")

print(suggestions)