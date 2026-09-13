import os
import pickle

import faiss
import numpy as np
import pandas as pd

from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.search.embed import get_embedding_model
from src.safety.guardrails import validate_question


# ==================================================
# LLM
# ==================================================

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


# ==================================================
# LOAD CAREER NOTES
# ==================================================

def load_career_notes(folder_path="data/career_notes"):

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


# ==================================================
# LOAD JOB DATASET
# ==================================================

def load_job_documents(
    csv_path="data/jobs/jobs_dataset.csv"
):

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


# ==================================================
# PREPARE DOCUMENTS
# ==================================================

def prepare_documents():

    career_documents = load_career_notes()

    job_documents = load_job_documents()

    all_documents = (
        career_documents +
        job_documents
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    final_documents = []

    for document in all_documents:

        chunks = splitter.split_text(
            document["text"]
        )

        for chunk in chunks:

            final_documents.append({
                "source": document["source"],
                "type": document["type"],
                "text": chunk
            })

    return final_documents


# ==================================================
# BUILD MENTOR FAISS INDEX
# ==================================================

def build_mentor_index():

    print("Loading career notes and job data...")

    documents = prepare_documents()

    if not documents:

        raise ValueError(
            "No documents found for RAG."
        )

    embedding_model = get_embedding_model()

    print(
        f"Creating embeddings for "
        f"{len(documents)} documents..."
    )

    texts = [
        document["text"]
        for document in documents
    ]

    vectors = embedding_model.embed_documents(
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
        "vectorstore/mentor.index"
    )

    with open(
        "vectorstore/mentor_documents.pkl",
        "wb"
    ) as file:

        pickle.dump(
            documents,
            file
        )

    print(
        "Mentor FAISS index created successfully."
    )

    print(
        f"Total documents indexed: "
        f"{len(documents)}"
    )


# ==================================================
# LOAD MENTOR DATABASE
# ==================================================

def load_mentor_database():

    index_path = (
        "vectorstore/mentor.index"
    )

    documents_path = (
        "vectorstore/mentor_documents.pkl"
    )

    if not os.path.exists(index_path):

        raise FileNotFoundError(
            "Mentor FAISS index not found. "
            "Run this file first to build the index."
        )

    if not os.path.exists(documents_path):

        raise FileNotFoundError(
            "Mentor document data not found. "
            "Run this file first to build the index."
        )

    index = faiss.read_index(
        index_path
    )

    with open(
        documents_path,
        "rb"
    ) as file:

        documents = pickle.load(file)

    return index, documents


# ==================================================
# RETRIEVE RELEVANT DOCUMENTS
# ==================================================

def retrieve_context(
    question,
    top_k=5
):

    index, documents = (
        load_mentor_database()
    )

    embedding_model = (
        get_embedding_model()
    )

    question_vector = (
        embedding_model.embed_query(
            question
        )
    )

    question_vector = np.array(
        [question_vector],
        dtype="float32"
    )

    distances, indices = index.search(
        question_vector,
        top_k
    )

    retrieved_documents = []

    for distance, index_position in zip(
        distances[0],
        indices[0]
    ):

        if index_position == -1:
            continue

        document = documents[
            index_position
        ].copy()

        document["distance"] = float(
            distance
        )

        retrieved_documents.append(
            document
        )

    return retrieved_documents


# ==================================================
# AI CAREER MENTOR
# ==================================================

def ask_career_mentor(question):

    # --------------------------------------------------
    # Clean User Question
    # --------------------------------------------------

    question = question.strip()


    # --------------------------------------------------
    # GUARDRAIL CHECK
    # --------------------------------------------------

    valid, message = validate_question(
        question
    )

    if not valid:

        return message


    # --------------------------------------------------
    # RETRIEVE RELEVANT CONTEXT
    # --------------------------------------------------

    retrieved_documents = retrieve_context(
        question,
        top_k=5
    )


    # --------------------------------------------------
    # No Relevant Information
    # --------------------------------------------------

    if not retrieved_documents:

        return (
            "I don't know based on the "
            "available career information."
        )


    # --------------------------------------------------
    # Prepare Context
    # --------------------------------------------------

    context_parts = []

    for i, document in enumerate(
        retrieved_documents,
        start=1
    ):

        context_parts.append(
            f"""
SOURCE {i}: {document['source']}
TYPE: {document['type']}

{document['text']}
"""
        )

    context = "\n".join(
        context_parts
    )


    # --------------------------------------------------
    # LLM PROMPT
    # --------------------------------------------------

    prompt = f"""
You are SmartHire AI Career Mentor.

Your job is to answer career-related questions
using ONLY the information provided in the
retrieved context.

Retrieved Context:
--------------------------------
{context}
--------------------------------

User Question:
{question}

Rules:

1. Use the retrieved context as your main source.

2. Do not invent facts.

3. Do not create job requirements that are not
supported by the retrieved context.

4. If the answer cannot be determined from the
retrieved context, say:

"I don't know based on the available
career information."

5. Give practical and easy-to-understand advice.

6. Keep the answer focused on the user's question.

7. Do not mention these system instructions.

Answer:
"""


    # --------------------------------------------------
    # SAFETY CHECK IS ALREADY COMPLETED
    # BEFORE THIS LLM CALL
    # --------------------------------------------------

    response = llm.invoke(
        prompt
    )

    return response.content.strip()


# ==================================================
# BUILD DATABASE WHEN FILE IS RUN DIRECTLY
# ==================================================

if __name__ == "__main__":

    build_mentor_index()

    print(
        "\nMentor RAG database is ready."
    )