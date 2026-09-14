import os

from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI


def get_secret(name: str):
    # First try environment variables
    value = os.getenv(name)

    if value:
        return value

    # Then try Streamlit secrets
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


def get_llm():

    provider = get_config("AI_PROVIDER", "ollama").lower()

    if provider == "gemini":

        api_key = get_secret("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. "
                "Add it to .streamlit/secrets.toml "
                "or your environment variables."
            )

        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=api_key
        )

    # Local Ollama option
    return ChatOllama(
        model="llama3.2",
        temperature=0
    )