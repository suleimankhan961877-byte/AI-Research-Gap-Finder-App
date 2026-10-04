# AI Research Gap Finder

A simple Streamlit application that reads a research article PDF and uses Groq AI to identify research gaps.

## What it does

1. Upload one research article PDF.
2. Extract text from the PDF.
3. Send the article text to Groq.
4. Identify author-stated limitations and AI-inferred research gaps.
5. Classify gaps into knowledge, methodological, data, application/validation, and parameter/scope gaps.
6. Suggest future research directions.
7. Download the analysis as a text file.

## Setup on Windows

```powershell
python -m venv venv
venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your Groq API key:

```text
GROQ_API_KEY=your_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

Run:

```powershell
streamlit run app.py
```

## Important

This tool assists with literature analysis. Always check the original paper and verify every proposed research gap before using it in a thesis, paper, or proposal.

For scanned/image-only PDFs, OCR should be added in a later version.
