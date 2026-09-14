import os

from langchain_ollama import OllamaEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def get_secret(name: str):
    value = os.getenv(name)

    if value:
        return value

    try:
        import streamlit as st

        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass

    return None


def get_config(name: str, default=None):
    value = os.getenv(name)

    if value:
        return value

    try:
        import streamlit as st

        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass

    return default


def get_embedding_model():

    provider = get_config("AI_PROVIDER", "ollama").lower()

    if provider == "gemini":

        api_key = get_secret("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. "
                "Add it to .streamlit/secrets.toml "
                "or your environment variables."
            )

        return GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",
            google_api_key=api_key
        )

    # Local Ollama option
    return OllamaEmbeddings(
        model="nomic-embed-text"
    )