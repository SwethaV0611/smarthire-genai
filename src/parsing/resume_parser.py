import json

from src.ai_provider import get_llm


# Create the LLM using the selected provider
llm = get_llm()


def parse_resume(resume_text: str) -> dict:
    """
    Parse resume text and return a structured JSON profile.
    """

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text is empty.")

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
- Return valid JSON only.

Resume:
----------------
{resume_text}
----------------
"""

    response = llm.invoke(prompt)

    response_text = response.content.strip()

    # --------------------------------------------------
    # Remove accidental Markdown code fences
    # --------------------------------------------------
    if response_text.startswith("```json"):
        response_text = response_text[7:]

    elif response_text.startswith("```"):
        response_text = response_text[3:]

    if response_text.endswith("```"):
        response_text = response_text[:-3]

    response_text = response_text.strip()

    # --------------------------------------------------
    # Convert response to JSON
    # --------------------------------------------------
    try:
        profile = json.loads(response_text)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"The AI response was not valid JSON: {error}"
        )

    # --------------------------------------------------
    # Required fields
    # --------------------------------------------------
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

    # --------------------------------------------------
    # Validate field types
    # --------------------------------------------------
    if not isinstance(profile["name"], str):
        raise ValueError("The 'name' field must be a string.")

    if not isinstance(profile["skills"], list):
        raise ValueError("The 'skills' field must be a list.")

    if not isinstance(profile["experience"], str):
        raise ValueError(
            "The 'experience' field must be a string."
        )

    if not isinstance(profile["education"], str):
        raise ValueError(
            "The 'education' field must be a string."
        )

    if not isinstance(profile["target_role"], str):
        raise ValueError(
            "The 'target_role' field must be a string."
        )

    return profile