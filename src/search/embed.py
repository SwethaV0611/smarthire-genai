import os
import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def get_secret(name: str):

    try:
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass

    return os.getenv(name)


def get_embedding_model():

    provider = get_secret("AI_PROVIDER")

    if provider and provider.lower() == "gemini":

        api_key = get_secret("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing.")

        return GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",
            google_api_key=api_key
        )

    # Local only
    from langchain_ollama import OllamaEmbeddings

    return OllamaEmbeddings(
        model="nomic-embed-text"
    )