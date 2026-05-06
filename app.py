import streamlit as st
from groq import Groq
import pdfplumber
import os

# ---------------------------
# API KEY
# ---------------------------
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("❌ GROQ_API_KEY not found")
    st.stop()

client = Groq(api_key=api_key)

# ---------------------------
# PDF TEXT EXTRACTION
# ---------------------------
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# ---------------------------
# UI
# ---------------------------
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")
st.title("📄 AI Resume Analyzer")

st.write("Upload your resume and compare it with a job description.")

# Upload resume
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Job description input
job_desc = st.text_area("Paste Job Description", height=200)

# ---------------------------
# ANALYZE BUTTON
# ---------------------------
if st.button("Analyze Resume"):

    if not uploaded_file or not job_desc:
        st.warning("Please upload resume and enter job description")
        st.stop()

    resume_text = extract_text_from_pdf(uploaded_file)

    prompt = f"""
You are an expert ATS resume analyzer.

Compare the resume with job description and provide:

1. Skill Match Score (0-100%)
2. Missing Skills
3. Strengths
4. Weaknesses
5. Resume Improvement Suggestions
6. Improved Resume Bullet Points

Resume:
{resume_text}

Job Description:
{job_desc}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message.content

        st.subheader("📊 Analysis Result")
        st.write(result)

    except Exception as e:
        st.error(f"Error: {e}")

        #git rm --cached .streamlit/secrets.toml
        #git reset --soft HEAD~1