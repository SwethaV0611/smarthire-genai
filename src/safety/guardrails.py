import re


# --------------------------------------------------
# Blocked / Unsafe Topics
# --------------------------------------------------

BLOCKED_PATTERNS = [
    r"\bhow to hack\b",
    r"\bhack someone\b",
    r"\bsteal password\b",
    r"\bsteal passwords\b",
    r"\bcreate malware\b",
    r"\bwrite malware\b",
    r"\bransomware\b",
    r"\bweapon\b",
    r"\bkill someone\b",
    r"\bmake a bomb\b",
    r"\bexploit someone\b"
]


# --------------------------------------------------
# Career-related Keywords
# --------------------------------------------------

CAREER_KEYWORDS = [
    "career",
    "job",
    "jobs",
    "resume",
    "cv",
    "skill",
    "skills",
    "interview",
    "internship",
    "intern",
    "experience",
    "education",
    "degree",
    "role",
    "developer",
    "engineer",
    "analyst",
    "scientist",
    "software",
    "python",
    "java",
    "machine learning",
    "data science",
    "cybersecurity",
    "programming",
    "project",
    "certification",
    "career path",
    "learning",
    "placement"
]


# --------------------------------------------------
# Input Validation
# --------------------------------------------------

def validate_input(question: str):

    if not question:
        return False, "Please enter a question."

    question = question.strip()

    if len(question) < 3:
        return False, "Please enter a meaningful question."

    if len(question) > 1000:
        return False, "Question is too long. Please keep it under 1000 characters."

    return True, ""


# --------------------------------------------------
# Safety Check
# --------------------------------------------------

def safety_check(question: str):

    question_lower = question.lower()

    for pattern in BLOCKED_PATTERNS:

        if re.search(pattern, question_lower):

            return False, (
                "I can only help with career, resume, "
                "job-search and professional development topics."
            )

    return True, ""


# --------------------------------------------------
# Career Scope Check
# --------------------------------------------------

def career_scope_check(question: str):

    question_lower = question.lower()

    for keyword in CAREER_KEYWORDS:

        if keyword in question_lower:
            return True, ""

    return False, (
        "This question is outside the scope of SmartHire. "
        "Please ask about careers, resumes, jobs, skills, "
        "interviews, education or professional development."
    )


# --------------------------------------------------
# Complete Guardrail Check
# --------------------------------------------------

def validate_question(question: str):

    # Step 1: Basic validation
    valid, message = validate_input(question)

    if not valid:
        return False, message

    # Step 2: Safety check
    safe, message = safety_check(question)

    if not safe:
        return False, message

    # Step 3: Career scope check
    in_scope, message = career_scope_check(question)

    if not in_scope:
        return False, message

    return True, ""