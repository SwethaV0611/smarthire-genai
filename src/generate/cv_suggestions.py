from langchain_ollama import ChatOllama

from src.generate.prompts import CV_IMPROVEMENT_PROMPT


llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


def generate_cv_suggestions(
    resume_text: str,
    job_text: str
) -> str:
    """
    Generate CV improvement suggestions
    based on a target job.
    """

    prompt = CV_IMPROVEMENT_PROMPT.format(
        resume_text=resume_text,
        job_text=job_text
    )

    response = llm.invoke(prompt)

    return response.content.strip()