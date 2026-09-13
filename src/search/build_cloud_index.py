import os
import pickle

import faiss
import numpy as np
import pandas as pd

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

# =========================================================
# CHECK GEMINI CONFIGURATION
# =========================================================

def get_gemini_embeddings():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not configured."
        )

    return GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=api_key
    )


# =========================================================
# LOAD JOB DATA
# =========================================================

def load_jobs():

    csv_path = "data/jobs/jobs_dataset.csv"

    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Job dataset not found: {csv_path}"
        )

    df = pd.read_csv(csv_path)

    required_columns = [
        "job_id",
        "title",
        "skills",
        "description"
    ]

    for column in required_columns:

        if column not in df.columns:
            raise ValueError(
                f"Missing column: {column}"
            )

    return df


# =========================================================
# BUILD JOB INDEX
# =========================================================

def build_job_index():

    print("Loading job dataset...")

    df = load_jobs()

    df["job_text"] = df.apply(
        lambda row:
        f"Job Title: {row['title']}\n"
        f"Skills: {row['skills']}\n"
        f"Description: {row['description']}",
        axis=1
    )

    embeddings = get_gemini_embeddings()

    print(
        f"Creating Gemini embeddings for "
        f"{len(df)} jobs..."
    )

    vectors = embeddings.embed_documents(
        df["job_text"].tolist()
    )

    vectors = np.array(
        vectors,
        dtype="float32"
    )

    dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(vectors)

    os.makedirs(
        "vectorstore",
        exist_ok=True
    )

    faiss.write_index(
        index,
        "vectorstore/jobs_gemini.index"
    )

    with open(
        "vectorstore/jobs_gemini_data.pkl",
        "wb"
    ) as file:

        pickle.dump(
            df,
            file
        )

    print(
        "Gemini job FAISS index created successfully."
    )


# =========================================================
# BUILD MENTOR INDEX
# =========================================================

def load_career_notes():

    folder_path = "data/career_notes"

    documents = []

    if not os.path.exists(folder_path):
        raise FileNotFoundError(
            f"Career notes folder not found: {folder_path}"
        )

    for filename in os.listdir(folder_path):

        if filename.lower().endswith(".txt"):

            file_path = os.path.join(
                folder_path,
                filename
            )

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                text = file.read().strip()

            if text:

                documents.append({
                    "source": filename,
                    "type": "career_note",
                    "text": text
                })

    return documents


def load_job_documents():

    df = load_jobs()

    documents = []

    for _, row in df.iterrows():

        text = (
            f"Job Title: {row['title']}\n"
            f"Skills: {row['skills']}\n"
            f"Description: {row['description']}"
        )

        documents.append({
            "source": f"Job ID {row['job_id']}",
            "type": "job",
            "text": text
        })

    return documents


def build_mentor_index():

    print("Preparing mentor documents...")

    documents = (
        load_career_notes()
        + load_job_documents()
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    final_documents = []

    for document in documents:

        chunks = splitter.split_text(
            document["text"]
        )

        for chunk in chunks:

            final_documents.append({
                "source": document["source"],
                "type": document["type"],
                "text": chunk
            })

    embeddings = get_gemini_embeddings()

    print(
        f"Creating Gemini embeddings for "
        f"{len(final_documents)} mentor documents..."
    )

    texts = [
        document["text"]
        for document in final_documents
    ]

    vectors = embeddings.embed_documents(
        texts
    )

    vectors = np.array(
        vectors,
        dtype="float32"
    )

    dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(vectors)

    os.makedirs(
        "vectorstore",
        exist_ok=True
    )

    faiss.write_index(
        index,
        "vectorstore/mentor_gemini.index"
    )

    with open(
        "vectorstore/mentor_gemini_documents.pkl",
        "wb"
    ) as file:

        pickle.dump(
            final_documents,
            file
        )

    print(
        "Gemini mentor FAISS index created successfully."
    )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("SmartHire - Gemini FAISS Index Builder")
    print("=" * 60)

    build_job_index()

    print()

    build_mentor_index()

    print()
    print("=" * 60)
    print("ALL GEMINI FAISS INDEXES CREATED")
    print("=" * 60)