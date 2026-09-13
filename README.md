# SmartHire AI

## Resume Matching & AI Career Mentor

SmartHire AI is a Generative AI-based career assistance platform that analyzes resumes, finds relevant job opportunities, provides CV improvement suggestions, and offers an AI Career Mentor using Retrieval-Augmented Generation (RAG).

---

## Features

### 1. Resume Analysis

Users can upload a PDF or DOCX resume.

The system extracts:

- Name
- Skills
- Experience
- Education
- Target Role

The resume is processed using an LLM and returned as structured JSON.

---

### 2. Semantic Job Matching

SmartHire converts job descriptions into embeddings and stores them in a FAISS vector database.

The candidate profile is also converted into an embedding.

The system then retrieves the most relevant jobs using semantic similarity.

---

### 3. CV Improvement

The system compares the candidate resume with the best matching job and generates:

- Missing skills
- Weak resume points
- Improved resume bullets
- Improved professional summary
- Actionable recommendations

The system is instructed not to invent qualifications or experience.

---

### 4. AI Career Mentor

The Career Mentor uses Retrieval-Augmented Generation.

It retrieves relevant information from:

- Job corpus
- Career notes

The retrieved information is provided to the local LLM to generate grounded career guidance.

---

### 5. Guardrails

The system validates user questions before sending them to the AI system.

It rejects:

- Unsafe requests
- Off-topic questions
- Questions outside the career assistance scope

---

### 6. Evaluation

The project evaluates:

- Job retrieval relevance
- Mentor correctness
- Mentor grounding
- Mentor helpfulness
- Hallucination handling
- Prompt improvements

---

## Technologies

- Python
- Streamlit
- LangChain
- FAISS
- Ollama
- Llama 3.2
- Nomic Embed Text
- Pandas
- NumPy
- PyPDF
- python-docx

---

## System Architecture

Resume Upload

↓

Document Loader

↓

Resume Chunking

↓

LLM Resume Parser

↓

Structured Candidate Profile

↓

Candidate Embedding

↓

FAISS Semantic Search

↓

Top Matching Jobs

↓

CV Improvement Generator

↓

AI Career Mentor

↓

RAG + Career Knowledge Base

↓

Guardrails

↓

Streamlit Portal

---

## Project Structure

```text
smarthire-genai/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── jobs/
│   ├── resumes/
│   └── career_notes/
│
├── vectorstore/
│
├── notebooks/
│
├── src/
│   ├── parsing/
│   ├── search/
│   ├── generate/
│   ├── mentor/
│   ├── safety/
│   └── evaluate.py
│
└── reports/
    └── answer_quality.md