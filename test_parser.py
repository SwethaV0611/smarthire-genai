from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume


resume_path = "data/resumes/resume3.docx"

chunks = load_resume(resume_path)

resume_text = "\n".join(chunks)

profile = parse_resume(resume_text)

print("\n===== PARSED RESUME =====\n")
print(profile)