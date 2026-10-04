import os
import re
import fitz
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

st.set_page_config(page_title="Research Gap Finder", page_icon="🔎", layout="wide")
st.title("🔎 AI Research Gap Finder")
st.write("Upload research article PDFs and identify research gaps using Groq AI.")

if not API_KEY:
    st.warning("Add GROQ_API_KEY to your .env file before running the app.")
    st.stop()

client = OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")


def extract_pdf_text(uploaded_file):
    data = uploaded_file.read()
    doc = fitz.open(stream=data, filetype="pdf")
    pages = []
    for page_number, page in enumerate(doc, start=1):
        text = page.get_text("text")
        if text.strip():
            pages.append(f"\n--- PAGE {page_number} ---\n{text}")
    return "\n".join(pages)


def analyze_gap(text, research_topic):
    max_chars = 50000
    if len(text) > max_chars:
        text = text[:max_chars]

    prompt = f"""
You are a careful academic research-gap analyst.

Research topic supplied by the user:
{research_topic or 'Not specified'}

Analyze ONLY the supplied article text. Do not invent facts, references, results, or gaps.

Return a concise structured analysis with these headings:

1. Article Summary
- Research objective
- Problem addressed
- Method used
- Main findings

2. What the Article Already Covers
- Established knowledge from this article

3. Limitations Reported by the Authors
- List limitations explicitly stated or clearly supported by the text

4. Research Gaps
Identify specific gaps that remain after this study. Separate them into:
- Knowledge gaps
- Methodological gaps
- Data gaps
- Application/validation gaps
- Parameter/scope gaps

5. Potential Future Research
Give practical research directions that directly follow from the identified gaps.

6. Evidence and Confidence
For every important gap, briefly explain what part of the article supports it. If page information is available in the text, mention the page number. Mark conclusions as HIGH, MEDIUM, or LOW confidence.

Important rules:
- Do not claim a gap merely because the paper did not discuss a topic.
- Distinguish an author-stated limitation from an AI-inferred gap.
- Do not call something a "novel research gap" without sufficient evidence.
- If the article does not provide enough evidence, say so.

ARTICLE TEXT:
{text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a rigorous academic research assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content or "No analysis returned."


uploaded = st.file_uploader(
    "Upload a research article PDF",
    type=["pdf"],
    accept_multiple_files=False,
)

research_topic = st.text_input(
    "Optional research topic",
    placeholder="e.g. Laser wire additive manufacturing of aerospace alloys",
)

if uploaded:
    with st.spinner("Reading PDF..."):
        article_text = extract_pdf_text(uploaded)

    if not article_text.strip():
        st.error("No readable text was found in this PDF. Try a text-based PDF.")
        st.stop()

    st.success(f"PDF loaded: {uploaded.name}")
    st.caption(f"Extracted approximately {len(article_text):,} characters.")

    with st.expander("Preview extracted text"):
        st.text(article_text[:5000])

    if st.button("🔎 Find Research Gaps", type="primary"):
        with st.spinner("Analyzing the article for research gaps..."):
            try:
                result = analyze_gap(article_text, research_topic)
                st.session_state["gap_result"] = result
            except Exception as exc:
                st.error(f"Analysis error: {exc}")

if "gap_result" in st.session_state:
    st.divider()
    st.subheader("Research Gap Analysis")
    st.markdown(st.session_state["gap_result"])

    st.download_button(
        "📄 Download Analysis",
        st.session_state["gap_result"],
        file_name="research_gap_analysis.txt",
        mime="text/plain",
    )
