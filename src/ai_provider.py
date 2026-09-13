import os

from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI


def get_secret(name: str):
    """
    Get a secret from environment variables or
    Streamlit secrets.
    """

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


def get_llm():

    provider = os.getenv(
        "AI_PROVIDER",
        "ollama"
    ).lower()

    # ==================================================
    # GEMINI
    # ==================================================

    if provider == "gemini":

        api_key = get_secret(
            "GEMINI_API_KEY"
        )

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=api_key
        )

    # ==================================================
    # OLLAMA - LOCAL
    # ==================================================

    return ChatOllama(
        model="llama3.2",
        temperature=0
    )