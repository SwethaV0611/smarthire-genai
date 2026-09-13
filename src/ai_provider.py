import os
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI


def get_secret(name: str):
    # First check environment variables
    value = os.getenv(name)

    if value:
        return value

    # Then check Streamlit Cloud secrets
    try:
        import streamlit as st

        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass

    return None


def get_provider():
    provider = get_secret("AI_PROVIDER")

    if provider:
        return provider.lower()

    return "ollama"


def get_llm():
    provider = get_provider()

    if provider == "gemini":
        api_key = get_secret("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=api_key
        )

    return ChatOllama(
        model="llama3.2",
        temperature=0
    )