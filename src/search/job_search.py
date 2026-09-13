import os
import pickle

import faiss
import numpy as np
import pandas as pd

from src.search.embed import get_embedding_model


def load_jobs(csv_path: str):
    """
    Load job information from CSV.
    """

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
                f"Missing column in job dataset: {column}"
            )

    return df


def create_job_text(row):
    """
    Combine important job information
    into searchable text.
    """

    return (
        f"Job Title: {row['title']}\n"
        f"Skills: {row['skills']}\n"
        f"Description: {row['description']}"
    )


def build_faiss_index(csv_path: str):
    """
    Create embeddings for all jobs
    and store them in FAISS.
    """

    df = load_jobs(csv_path)

    df["job_text"] = df.apply(
        create_job_text,
        axis=1
    )

    embedding_model = get_embedding_model()

    print("Creating job embeddings...")

    vectors = embedding_model.embed_documents(
        df["job_text"].tolist()
    )

    vectors = np.array(
        vectors,
        dtype="float32"
    )

    dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(vectors)

    return index, df


def save_index(index, df):
    """
    Save FAISS index and job data.
    """

    os.makedirs(
        "vectorstore",
        exist_ok=True
    )

    faiss.write_index(
        index,
        "vectorstore/jobs.index"
    )

    with open(
        "vectorstore/jobs_data.pkl",
        "wb"
    ) as file:

        pickle.dump(
            df,
            file
        )

    print("FAISS index saved successfully.")


def load_faiss_database():
    """
    Load the existing FAISS index
    and job information.
    """

    index_path = "vectorstore/jobs.index"
    data_path = "vectorstore/jobs_data.pkl"

    if not os.path.exists(index_path):
        raise FileNotFoundError(
            "FAISS index not found. "
            "Run job_search.py first."
        )

    if not os.path.exists(data_path):
        raise FileNotFoundError(
            "Job data file not found. "
            "Run job_search.py first."
        )

    index = faiss.read_index(
        index_path
    )

    with open(
        data_path,
        "rb"
    ) as file:

        df = pickle.load(file)

    return index, df


def create_candidate_text(profile: dict) -> str:
    """
    Convert parsed resume profile
    into searchable candidate text.
    """

    skills = ", ".join(
        profile.get("skills", [])
    )

    return (
        f"Target Role: {profile.get('target_role', '')}\n"
        f"Skills: {skills}\n"
        f"Experience: {profile.get('experience', '')}\n"
        f"Education: {profile.get('education', '')}"
    )


def search_jobs(profile: dict, top_n: int = 5):
    """
    Find the most relevant jobs for
    the candidate profile.
    """

    index, df = load_faiss_database()

    embedding_model = get_embedding_model()

    candidate_text = create_candidate_text(
        profile
    )

    print("Creating candidate embedding...")

    candidate_vector = embedding_model.embed_query(
        candidate_text
    )

    candidate_vector = np.array(
        [candidate_vector],
        dtype="float32"
    )

    distances, indices = index.search(
        candidate_vector,
        top_n
    )

    results = []

    for distance, index_position in zip(
        distances[0],
        indices[0]
    ):

        if index_position == -1:
            continue

        job = df.iloc[index_position]

        # Convert FAISS distance into
        # an easy-to-understand similarity score.
        similarity_score = 1 / (1 + float(distance))

        results.append({
            "job_id": job["job_id"],
            "title": job["title"],
            "skills": job["skills"],
            "description": job["description"],
            "similarity_score": round(
                similarity_score * 100,
                2
            )
        })

    return results


if __name__ == "__main__":

    csv_path = "data/jobs/jobs_dataset.csv"

    # Build database if it doesn't already exist
    if not os.path.exists(
        "vectorstore/jobs.index"
    ):

        index, df = build_faiss_index(
            csv_path
        )

        save_index(
            index,
            df
        )

    print("\nFAISS job database is ready.")