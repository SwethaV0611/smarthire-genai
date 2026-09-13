import os
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI


def get_secret(name):
    """Read a value from Streamlit Secrets or environment variables."""
    try:
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass

    return os.getenv(name)


def get_provider():
    """Get the selected AI provider."""

    provider = get_secret("AI_PROVIDER")

    if provider:
        return str(provider).strip().lower()

    # Streamlit Cloud should use Gemini by default.
    return "gemini"


def get_llm():
    provider = get_provider()

    if provider == "gemini":
        api_key = get_secret("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. "
                "Add GEMINI_API_KEY in Streamlit Cloud Secrets."
            )

        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0,
        )

    # Ollama is only used when explicitly selected.
    if provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model="llama3.2",
            temperature=0,
        )

    raise ValueError(
        f"Unsupported AI_PROVIDER: {provider}. "
        "Use 'gemini' or 'ollama'."
    )