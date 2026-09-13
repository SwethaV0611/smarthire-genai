from src.ai_provider import get_llm

from src.generate.prompts import CV_IMPROVEMENT_PROMPT


# Create the LLM using the selected provider
llm = get_llm()


def generate_cv_suggestions(
    resume_text: str,
    job_text: str
) -> str:
    """
    Generate CV improvement suggestions by comparing
    the candidate resume with a target job.
    """

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text is empty.")

    if not job_text or not job_text.strip():
        raise ValueError("Target job information is empty.")

    prompt = CV_IMPROVEMENT_PROMPT.format(
        resume_text=resume_text,
        job_text=job_text
    )

    response = llm.invoke(prompt)

    return response.content.strip()