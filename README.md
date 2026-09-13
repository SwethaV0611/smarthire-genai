# SmartHire GenAI — Resume Matching & AI Career Mentor

SmartHire GenAI is an AI-powered career assistance system that analyzes resumes, finds relevant job opportunities using semantic search, generates CV improvement suggestions, and provides grounded career guidance through an AI Career Mentor.

## Project Overview

Traditional job-search systems often depend on keyword matching, which may fail when a candidate's resume and a job description use different terminology.

SmartHire GenAI uses Large Language Models, embeddings, FAISS vector search, Retrieval-Augmented Generation (RAG), and prompt engineering to provide intelligent and personalized career assistance.

The system performs four major tasks:

1. Resume Analysis
2. Semantic Job Matching
3. CV Improvement
4. AI Career Mentor

---

## Key Features

### 1. Resume Analysis

The system accepts resumes in PDF and DOCX formats.

It extracts and structures:

- Candidate Name
- Skills
- Experience
- Education
- Target Role

The resume information is converted into structured JSON using an LLM.

### 2. Semantic Job Matching

The system matches candidates with relevant jobs using semantic similarity instead of simple keyword matching.

Process:

```text
Candidate Resume
       ↓
Resume Profile
       ↓
Embedding Generation
       ↓
FAISS Vector Search
       ↓
Top-N Relevant Jobs
