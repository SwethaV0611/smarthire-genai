# SmartHire GenAI - Evaluation Report

## 1. Retrieval Relevance

**Retrieval Hit Rate:** 100.00%

| Resume | Target Role | Top Job | Relevant |
|---|---|---|---|
| resume1.pdf | Software Engineer | Software Engineer | Yes |
| resume2.pdf | Data Analyst | Data Analyst | Yes |
| resume3.docx | Data Scientist | Data Scientist | Yes |
| resume4.pdf | Machine Learning Engineer | Machine Learning Engineer | Yes |
| resume5.docx | Software Developer | Software Engineer | Yes |

## 2. Mentor Answer Quality

| Question | Correctness | Grounding | Helpfulness |
|---|---:|---:|---:|
| What skills are important for a Data Scientist? | 4 | 3 | 2 |
| What skills should I learn for a Software Engineer role? | 2 | 4 | 5 |
| What skills are useful for a Machine Learning Engineer? | 3 | 2 | 4 |
| How can I improve my career skills? | 3 | 5 | 2 |

## 3. Hallucination / Guardrail Test

| Question | Result |
|---|---|
| What is the weather today? | PASS |

## 4. Prompt Comparison

A before/after prompt comparison should be added after testing the original and improved prompts.

**Before Prompt:**

Describe the original prompt used.

**Before Output:**

Paste the original model output.

**After Prompt:**

Describe the improved prompt.

**After Output:**

Paste the improved model output.

## 5. Observations

- Evaluate whether retrieved jobs are relevant to candidate profiles.
- Check whether mentor answers stay grounded in the knowledge base.
- Check whether unsupported questions are rejected appropriately.
- Record limitations and possible future improvements.
