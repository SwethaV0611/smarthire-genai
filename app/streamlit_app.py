import os
import sys
import tempfile

import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# IMPORT PROJECT MODULES
# ============================================================

from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume

from src.search.job_search import search_jobs

from src.generate.cv_suggestions import (
    generate_cv_suggestions
)

from src.mentor.rag_chain import (
    ask_career_mentor
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SmartHire AI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("💼 SmartHire AI")

    st.write(
        "AI-powered career assistant"
    )

    st.divider()

    st.subheader("Features")

    st.write("📄 Resume Analysis")
    st.write("🔎 Semantic Job Matching")
    st.write("✍️ CV Improvement")
    st.write("🤖 AI Career Mentor")

    st.divider()

    st.subheader("Technology")

    st.caption("Python")
    st.caption("LangChain")
    st.caption("FAISS")
    st.caption("Ollama")
    st.caption("Llama 3.2")
    st.caption("Streamlit")


# ============================================================
# HEADER
# ============================================================

st.title("💼 SmartHire AI")

st.subheader(
    "Your career, smarter with AI."
)

st.write(
    "Analyze your resume, discover relevant jobs, "
    "improve your CV and get personalized career guidance."
)

st.divider()


# ============================================================
# FEATURES
# ============================================================

st.header("Everything you need to grow")

st.write(
    "One platform for resume analysis, job discovery "
    "and career guidance."
)

f1, f2, f3, f4 = st.columns(4)

with f1:

    st.info(
        "📄 Resume Analysis\n\n"
        "Extract skills, education, experience "
        "and target role from your resume."
    )

with f2:

    st.info(
        "🔎 Smart Job Matching\n\n"
        "Find relevant jobs using semantic "
        "similarity and FAISS."
    )

with f3:

    st.info(
        "✍️ CV Improvement\n\n"
        "Identify missing skills and improve "
        "your resume content."
    )

with f4:

    st.info(
        "🤖 AI Career Mentor\n\n"
        "Get career guidance using RAG and "
        "your career knowledge base."
    )


st.divider()


# ============================================================
# TABS
# ============================================================

tab_resume, tab_jobs, tab_cv, tab_mentor = st.tabs(
    [
        "📄 Resume Analysis",
        "🔎 Job Matches",
        "✍️ CV Improvement",
        "🤖 AI Career Mentor"
    ]
)


# ============================================================
# RESUME ANALYSIS TAB
# ============================================================

with tab_resume:

    st.header("Analyze Your Resume")

    st.write(
        "Upload your resume in PDF or DOCX format."
    )

    uploaded_file = st.file_uploader(
        "Choose your resume",
        type=["pdf", "docx"]
    )

    if uploaded_file:

        st.success(
            f"Selected: {uploaded_file.name}"
        )

        if st.button(
            "🚀 Analyze Resume",
            type="primary",
            use_container_width=True
        ):

            temp_path = None

            try:

                # ----------------------------------------
                # Save uploaded file
                # ----------------------------------------

                extension = os.path.splitext(
                    uploaded_file.name
                )[1]

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=extension
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getbuffer()
                    )

                    temp_path = temp_file.name


                # ----------------------------------------
                # Extract resume
                # ----------------------------------------

                with st.spinner(
                    "Reading your resume..."
                ):

                    chunks = load_resume(
                        temp_path
                    )

                    resume_text = "\n".join(
                        chunks
                    )


                # ----------------------------------------
                # Parse resume
                # ----------------------------------------

                with st.spinner(
                    "Analyzing your professional profile..."
                ):

                    profile = parse_resume(
                        resume_text
                    )


                # ----------------------------------------
                # Job matching
                # ----------------------------------------

                with st.spinner(
                    "Finding matching jobs..."
                ):

                    results = search_jobs(
                        profile,
                        top_n=5
                    )


                # ----------------------------------------
                # CV suggestions
                # ----------------------------------------

                suggestions = ""

                if results:

                    best_job = results[0]

                    job_text = (
                        f"Job Title: "
                        f"{best_job['title']}\n"
                        f"Skills: "
                        f"{best_job['skills']}\n"
                        f"Description: "
                        f"{best_job['description']}"
                    )

                    with st.spinner(
                        "Generating CV improvement suggestions..."
                    ):

                        suggestions = (
                            generate_cv_suggestions(
                                resume_text,
                                job_text
                            )
                        )


                # ----------------------------------------
                # Save results
                # ----------------------------------------

                st.session_state[
                    "resume_text"
                ] = resume_text

                st.session_state[
                    "profile"
                ] = profile

                st.session_state[
                    "job_results"
                ] = results

                st.session_state[
                    "cv_suggestions"
                ] = suggestions

                st.session_state[
                    "resume_name"
                ] = uploaded_file.name


                st.success(
                    "Resume analysis completed successfully!"
                )


            except Exception as e:

                st.error(
                    f"Analysis failed: {e}"
                )


            finally:

                if (
                    temp_path
                    and os.path.exists(temp_path)
                ):

                    os.remove(temp_path)


    # ========================================================
    # PROFILE
    # ========================================================

    if "profile" in st.session_state:

        profile = st.session_state[
            "profile"
        ]

        st.divider()

        st.header("👤 Your Professional Profile")

        p1, p2, p3 = st.columns(3)

        with p1:

            st.metric(
                "Candidate",
                profile.get(
                    "name",
                    "Not available"
                )
            )

        with p2:

            st.metric(
                "Target Role",
                profile.get(
                    "target_role",
                    "Not available"
                )
            )

        with p3:

            st.metric(
                "Education",
                profile.get(
                    "education",
                    "Not available"
                )
            )


        st.subheader("Skills")

        skills = profile.get(
            "skills",
            []
        )

        if skills:

            st.write(
                " • ".join(skills)
            )

        else:

            st.write(
                "No skills identified."
            )


        st.subheader("Experience")

        st.info(
            profile.get(
                "experience",
                "No experience information available."
            )
        )


# ============================================================
# JOB MATCHES TAB
# ============================================================

with tab_jobs:

    st.header("🔎 Recommended Job Opportunities")

    st.write(
        "Jobs ranked according to the semantic similarity "
        "between your profile and the job descriptions."
    )

    if "job_results" not in st.session_state:

        st.info(
            "Analyze your resume first to see recommended jobs."
        )

    else:

        results = st.session_state[
            "job_results"
        ]

        if not results:

            st.warning(
                "No matching jobs were found."
            )

        else:

            for i, job in enumerate(
                results,
                start=1
            ):

                with st.container(
                    border=True
                ):

                    col1, col2 = st.columns(
                        [5, 1]
                    )

                    with col1:

                        st.subheader(
                            f"{i}. {job['title']}"
                        )

                        st.caption(
                            f"Job ID: {job['job_id']}"
                        )

                    with col2:

                        score = float(
                            job["similarity_score"]
                        )

                        st.metric(
                            "Match",
                            f"{score:.1f}%"
                        )


                    st.progress(
                        min(
                            max(
                                score / 100,
                                0.0
                            ),
                            1.0
                        )
                    )


                    with st.expander(
                        "View Job Details"
                    ):

                        st.write(
                            "**Required Skills**"
                        )

                        st.write(
                            job["skills"]
                        )

                        st.write(
                            "**Description**"
                        )

                        st.write(
                            job["description"]
                        )


# ============================================================
# CV IMPROVEMENT TAB
# ============================================================

with tab_cv:

    st.header("✍️ AI CV Improvement")

    st.write(
        "Improve your resume based on the strongest "
        "matching job."
    )

    if "cv_suggestions" not in st.session_state:

        st.info(
            "Analyze your resume first to generate "
            "personalized CV recommendations."
        )

    elif not st.session_state[
        "cv_suggestions"
    ]:

        st.warning(
            "No CV recommendations were generated."
        )

    else:

        st.success(
            "Personalized recommendations are ready."
        )

        st.markdown(
            st.session_state[
                "cv_suggestions"
            ]
        )


# ============================================================
# AI CAREER MENTOR TAB
# ============================================================

with tab_mentor:

    st.header("🤖 SmartHire AI Career Mentor")

    st.write(
        "Ask questions about careers, skills, jobs, "
        "resumes, interviews and professional development."
    )

    st.divider()

    st.subheader("Suggested Questions")

    q1, q2, q3 = st.columns(3)

    with q1:

        st.info(
            "What skills should I learn for Data Science?"
        )

    with q2:

        st.info(
            "How can I improve my resume?"
        )

    with q3:

        st.info(
            "What should I prepare for interviews?"
        )


    # --------------------------------------------------------
    # Chat history
    # --------------------------------------------------------

    if "mentor_messages" not in st.session_state:

        st.session_state[
            "mentor_messages"
        ] = []


    for message in st.session_state[
        "mentor_messages"
    ]:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # --------------------------------------------------------
    # Chat input
    # --------------------------------------------------------

    question = st.chat_input(
        "Ask SmartHire about your career..."
    )


    if question:

        st.session_state[
            "mentor_messages"
        ].append(
            {
                "role": "user",
                "content": question
            }
        )


        with st.chat_message("user"):

            st.write(question)


        with st.chat_message("assistant"):

            with st.spinner(
                "SmartHire is thinking..."
            ):

                answer = ask_career_mentor(
                    question
                )

            st.write(answer)


        st.session_state[
            "mentor_messages"
        ].append(
            {
                "role": "assistant",
                "content": answer
            }
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SmartHire AI • Resume Analysis • Semantic Job Matching "
    "• CV Improvement • RAG Career Mentor"
)

st.caption(
    "Built with Python, LangChain, FAISS, Ollama and Streamlit"
)