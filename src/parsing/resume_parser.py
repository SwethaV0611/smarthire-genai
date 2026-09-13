import json
from langchain_ollama import ChatOllama


# Local LLM
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


def parse_resume(resume_text: str) -> dict:
    """
    Convert resume text into structured candidate information.
    """

    prompt = f"""
You are an expert resume parser.

Analyze the resume below and extract the candidate information.

Return ONLY valid JSON.

The JSON must contain exactly these fields:

{{
    "name": "",
    "skills": [],
    "experience": "",
    "education": "",
    "target_role": ""
}}

Rules:
- name: candidate's full name
- skills: list of technical and professional skills
- experience: summarize work or internship experience
- education: summarize educational qualifications
- target_role: most suitable job role based on the resume
- Do not invent information.
- If information is missing, use an empty string or empty list.
- Do not include markdown.
- Do not include explanations outside the JSON.

Resume:
----------------
{resume_text}
----------------
"""

    response = llm.invoke(prompt)

    response_text = response.content.strip()

    try:
        profile = json.loads(response_text)

    except json.JSONDecodeError:
        raise ValueError(
            "The AI response was not valid JSON."
        )

    required_fields = [
        "name",
        "skills",
        "experience",
        "education",
        "target_role"
    ]

    for field in required_fields:
        if field not in profile:
            raise ValueError(
                f"Missing required field: {field}"
            )

    return profile