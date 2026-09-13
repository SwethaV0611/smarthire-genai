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
````

The project uses a pre-collected job dataset containing:

* Job ID
* Job Title
* Required Skills
* Job Description

No live LinkedIn or Naukri scraping is used.

### 3. CV Improvement Generator

The system compares the candidate's resume with a target job and identifies:

* Missing Skills
* Weak Resume Points
* Improved Resume Bullets
* Improved Professional Summary
* Overall Recommendations

The system is instructed not to invent qualifications, experience, certifications, or achievements.

### 4. AI Career Mentor

The AI Career Mentor uses Retrieval-Augmented Generation (RAG).

Career questions are answered using information retrieved from the project's career knowledge base.

The knowledge base contains career notes related to areas such as:

* Software Engineering
* Data Analytics
* Data Science
* Machine Learning
* Cybersecurity

### 5. Guardrails

The system includes input validation and safety checks.

The guardrails:

* Validate user input
* Limit question length
* Reject unsafe requests
* Reject unrelated questions
* Restrict the mentor to career-related topics
* Reduce unsupported or hallucinated responses

---

## System Architecture

```text
                 ┌─────────────────────┐
                 │      User Resume    │
                 │      PDF / DOCX     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Resume Document   │
                 │      Loader         │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    LLM Resume       │
                 │      Parser         │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Structured Profile  │
                 │ Name / Skills /     │
                 │ Education / Role    │
                 └──────────┬──────────┘
                            │
                ┌───────────┴────────────┐
                │                        │
                ▼                        ▼
       ┌─────────────────┐     ┌──────────────────┐
       │ Job Embeddings  │     │ Candidate        │
       │                 │     │ Embedding        │
       └────────┬────────┘     └────────┬─────────┘
                │                       │
                └───────────┬───────────┘
                            ▼
                  ┌───────────────────┐
                  │   FAISS Search    │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ Ranked Job        │
                  │ Recommendations   │
                  └───────────────────┘

        Resume + Target Job
                 │
                 ▼
        ┌───────────────────┐
        │ CV Improvement    │
        │ Generator         │
        └───────────────────┘

 Career Question
        │
        ▼
 ┌───────────────┐
 │  Guardrails   │
 └───────┬───────┘
         │
         ▼
 ┌───────────────────┐
 │ Career Knowledge  │
 │ Base + FAISS      │
 └─────────┬─────────┘
           │
           ▼
 ┌───────────────────┐
 │ RAG Career Mentor │
 └───────────────────┘
```

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
│   │   └── jobs_dataset.csv
│   │
│   ├── resumes/
│   │   ├── resume1.pdf
│   │   ├── resume2.pdf
│   │   ├── resume3.docx
│   │   ├── resume4.pdf
│   │   └── resume5.docx
│   │
│   └── career_notes/
│       ├── cybersecurity.txt
│       ├── data_analyst.txt
│       ├── data_scientist.txt
│       ├── ml_engineer.txt
│       └── software_engineer.txt
│
├── src/
│   ├── parsing/
│   │   ├── loader.py
│   │   └── resume_parser.py
│   │
│   ├── search/
│   │   ├── embed.py
│   │   ├── job_search.py
│   │   └── build_cloud_index.py
│   │
│   ├── generate/
│   │   ├── prompts.py
│   │   └── cv_suggestions.py
│   │
│   ├── mentor/
│   │   └── rag_chain.py
│   │
│   ├── safety/
│   │   └── guardrails.py
│   │
│   ├── ai_provider.py
│   └── evaluate.py
│
├── vectorstore/
│   ├── jobs_gemini.index
│   ├── jobs_gemini_data.pkl
│   ├── mentor_gemini.index
│   └── mentor_gemini_documents.pkl
│
├── notebooks/
│
├── reports/
│   └── answer_quality.md
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Technologies Used

| Technology  | Purpose                       |
| ----------- | ----------------------------- |
| Python      | Core programming language     |
| LangChain   | LLM and RAG workflow          |
| Gemini      | Language model and embeddings |
| Ollama      | Local LLM support             |
| FAISS       | Vector similarity search      |
| Streamlit   | Application interface         |
| PyPDF       | PDF resume extraction         |
| python-docx | DOCX resume extraction        |
| Pandas      | Dataset processing            |
| NumPy       | Numerical processing          |

---

## AI Workflow

### Resume Parsing

```text
PDF / DOCX
    ↓
Text Extraction
    ↓
Text Cleaning
    ↓
LLM Prompt
    ↓
JSON Validation
    ↓
Candidate Profile
```

### Job Matching

```text
Job Descriptions
       ↓
Embeddings
       ↓
FAISS Index
       ↓
Candidate Profile
       ↓
Candidate Embedding
       ↓
Similarity Search
       ↓
Top-N Jobs
```

### Career Mentor

```text
Career Question
       ↓
Input Validation
       ↓
Safety / Scope Check
       ↓
Query Embedding
       ↓
FAISS Retrieval
       ↓
Relevant Career Documents
       ↓
LLM
       ↓
Grounded Career Answer
```

---

## Dataset

The project uses a pre-collected job dataset rather than live job-site scraping.

The dataset contains job records with:

* Job ID
* Job Title
* Skills
* Description

The project also includes sample resumes in PDF and DOCX formats for testing the system.

---

## Evaluation

The project includes an evaluation script:

```text
src/evaluate.py
```

The evaluation covers:

### Job Retrieval

Measures whether relevant jobs appear among the retrieved results.

### Career Mentor

Evaluates:

* Correctness
* Grounding
* Helpfulness

### Guardrails

Tests whether unrelated and unsafe questions are rejected.

### Hallucination Check

The mentor is expected to acknowledge when the available knowledge base does not contain sufficient information rather than inventing unsupported information.

Evaluation results are stored in:

```text
reports/answer_quality.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/SwethaV0611/smarthire-genai.git
cd smarthire-genai
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure the AI provider

Create a `.env` file based on:

```text
.env.example
```

Example:

```text
AI_PROVIDER=gemini
GEMINI_API_KEY=your_api_key
```

Never commit API keys to GitHub.

---

## Running the Application

The project includes a Streamlit interface:

```powershell
python -m streamlit run app/streamlit_app.py
```

The application provides:

* Resume Analysis
* Job Matching
* CV Improvement
* AI Career Mentor

---

## Research Components

The project demonstrates the use of:

* Large Language Models
* Prompt Engineering
* Structured JSON Generation
* Text Chunking
* Embeddings
* FAISS Vector Search
* Semantic Search
* Retrieval-Augmented Generation
* Input Guardrails
* Career Recommendation
* AI-based Resume Analysis
* Evaluation and Prompt Optimization

---

## Future Enhancements

Possible future improvements include:

* Explainable job recommendations
* Resume-to-job match percentage
* Citation support for mentor answers
* Personalized learning paths
* Conversation memory
* Multiple embedding model comparison
* More job categories
* Improved resume rewriting
* Additional evaluation datasets

---

## Project Objective

The main objective of SmartHire GenAI is to provide an intelligent career assistant that combines resume understanding, semantic job retrieval, CV improvement, and grounded career guidance in a single system.

---

## Author
**Swetha**

