from src.parsing.loader import load_resume


resume_path = "data/resumes/resume3.docx"

chunks = load_resume(resume_path)

print("Resume loaded successfully!")
print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks, 1):
    print(f"\n--- Chunk {i} ---")
    print(chunk)