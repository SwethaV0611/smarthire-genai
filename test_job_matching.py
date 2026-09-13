from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume
from src.search.job_search import search_jobs


# Resume to test
resume_path = "data/resumes/resume3.docx"


# Step 1: Load resume
chunks = load_resume(resume_path)

resume_text = "\n".join(chunks)


# Step 2: Parse resume
profile = parse_resume(resume_text)


print("\n===== CANDIDATE PROFILE =====\n")

print(profile)


# Step 3: Search matching jobs
results = search_jobs(
    profile,
    top_n=5
)


print("\n===== TOP MATCHING JOBS =====\n")


for i, job in enumerate(
    results,
    start=1
):

    print(f"--- Match {i} ---")

    print(
        "Job ID:",
        job["job_id"]
    )

    print(
        "Job Title:",
        job["title"]
    )

    print(
        "Skills:",
        job["skills"]
    )

    print(
        "Similarity Score:",
        f"{job['similarity_score']}%"
    )

    print(
        "Description:",
        job["description"]
    )

    print()