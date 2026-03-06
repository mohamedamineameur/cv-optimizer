import json
import os
from typing import Any

import docx
import pdfplumber
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

from cv_generator import build_cv_pdf


# =========================
# LOAD ENV
# =========================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env")

client = OpenAI(api_key=api_key)


# =========================
# PYDANTIC SCHEMA
# =========================

class HeaderModel(BaseModel):
    name: str = ""
    title: str = ""
    phone: str = ""
    location: str = ""
    email: str = ""
    linkedin: str = ""
    portfolio: str = ""
    github: str = ""
    languages: list[str] = Field(default_factory=list)


class WorkExperienceItem(BaseModel):
    title: str = ""
    company: str = ""
    location: str = ""
    date: str = ""
    description: str = ""
    bullets: list[str] = Field(default_factory=list)
    links: dict[str, str] = Field(default_factory=dict)


class EducationItem(BaseModel):
    date: str = ""
    title: str = ""
    school: str = ""
    location: str = ""
    notes: str = ""


class ResumeModel(BaseModel):
    keywords: list[str] = Field(default_factory=list)
    header: HeaderModel = Field(default_factory=HeaderModel)
    work_experience: list[WorkExperienceItem] = Field(default_factory=list)
    education: list[EducationItem] = Field(default_factory=list)
    technical_skills: dict[str, list[str]] = Field(default_factory=dict)


# =========================
# HELPERS
# =========================

def extract_text_from_pdf(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def extract_text_from_docx(file):

    doc = docx.Document(file)

    return "\n".join(p.text for p in doc.paragraphs if p.text)


def parse_cv(uploaded_file):

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)

    if filename.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)

    return ""


def empty_resume_dict():

    return {
        "keywords": [],
        "header": {
            "name": "",
            "title": "",
            "phone": "",
            "location": "",
            "email": "",
            "linkedin": "",
            "portfolio": "",
            "github": "",
            "languages": [],
        },
        "work_experience": [],
        "education": [],
        "technical_skills": {},
    }


def deep_merge_resume(base: dict[str, Any], incoming: dict[str, Any]):

    result = empty_resume_dict()

    result["header"] = {**result["header"], **incoming.get("header", {})}

    if isinstance(incoming.get("keywords"), list):
        result["keywords"] = incoming["keywords"]

    if isinstance(incoming.get("work_experience"), list):

        jobs = incoming["work_experience"]

        for job in jobs:

            if "links" not in job or job["links"] is None:
                job["links"] = {}

        result["work_experience"] = jobs

    if isinstance(incoming.get("education"), list):
        result["education"] = incoming["education"]

    if isinstance(incoming.get("technical_skills"), dict):
        result["technical_skills"] = incoming["technical_skills"]

    return result


def is_resume_complete(data):

    missing = []

    header = data.get("header", {})

    if not header.get("name"):
        missing.append("header.name")

    if not header.get("title"):
        missing.append("header.title")

    if not data.get("work_experience"):
        missing.append("work_experience")

    if not data.get("education"):
        missing.append("education")

    if not data.get("technical_skills"):
        missing.append("technical_skills")

    return len(missing) == 0, missing


# =========================
# OPENAI CALL
# =========================

def optimize_cv_structured(cv_text, job_offer, language):

    cv_language = "French" if language == "FR" else "English"

    system_prompt = f"""
You are an expert ATS resume optimizer. Your task is to extract ALL information from the CV text and structure it into a complete JSON resume.

CRITICAL INSTRUCTIONS:
- Extract EVERY piece of information from the CV text provided
- Fill ALL fields with actual data from the CV - do NOT leave fields empty if information exists
- The resume language must be {cv_language}
- Optimize wording for ATS keyword matching with the job offer
- Do NOT invent or add information that is not in the CV
- Return ONLY valid JSON, no explanations or markdown

REQUIRED STRUCTURE:

{{
  "keywords": ["list", "of", "ATS", "keywords", "from", "job", "offer", "that", "match", "CV"],
  "header": {{
    "name": "Full name from CV",
    "title": "Professional title/role",
    "phone": "Phone number if present",
    "location": "City, Country",
    "email": "Email address",
    "linkedin": "LinkedIn URL if present",
    "portfolio": "Portfolio URL if present",
    "github": "GitHub URL if present",
    "languages": ["Language1", "Language2"]
  }},
  "work_experience": [
    {{
      "title": "Job title",
      "company": "Company name",
      "location": "City, Country",
      "date": "Start date - End date",
      "description": "Brief description",
      "bullets": ["Achievement 1", "Achievement 2"],
      "links": {{"project": "url"}}
    }}
  ],
  "education": [
    {{
      "date": "Graduation date",
      "title": "Degree name",
      "school": "School/University name",
      "location": "City, Country",
      "notes": "Additional info"
    }}
  ],
  "technical_skills": {{
    "Category1": ["skill1", "skill2"],
    "Category2": ["skill3", "skill4"]
  }}
}}

EXTRACTION RULES:
- Extract ALL work experiences from the CV, even if there are many
- Extract ALL education entries from the CV
- Extract ALL technical skills and organize them by category
- Extract ALL contact information (name, email, phone, location, LinkedIn, GitHub, etc.)
- For keywords: identify the most relevant ATS terms from the job offer that are honestly supported by the CV content
- If a field truly doesn't exist in the CV, use empty string "" or empty array []
- DO NOT create empty work_experience or education entries if there are none in the CV
"""

    user_prompt = f"""
Extract ALL information from the CV below and create a complete structured JSON resume optimized for ATS matching with the job offer.

JOB OFFER:
{job_offer}

CV TEXT (extract ALL information from this):
{cv_text}

IMPORTANT: Extract every work experience, education entry, skill, and contact detail from the CV. Do not leave fields empty if the information exists in the CV text above.
"""

    completion = client.chat.completions.create(
        model="gpt-4.1",
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )

    content = completion.choices[0].message.content

    start = content.find("{")
    end = content.rfind("}") + 1

    json_text = content[start:end]

    return json.loads(json_text)


def optimize_cv(cv_text, job_offer, language):

    base_resume = empty_resume_dict()

    first_pass = optimize_cv_structured(cv_text, job_offer, language)

    merged = deep_merge_resume(base_resume, first_pass)

    return ResumeModel.model_validate(merged).model_dump()


# =========================
# STREAMLIT UI
# =========================

st.set_page_config(page_title="ATS Resume Optimizer", page_icon="📄")

st.title("📄 ATS Resume Optimizer")

language = st.selectbox("CV language", ["EN", "FR"])

uploaded_cv = st.file_uploader("Upload CV", type=["pdf", "docx"])

job_offer = st.text_area("Paste job offer", height=300)

show_json = st.checkbox("Show JSON", value=False)


if st.button("Optimize CV"):

    if not uploaded_cv:
        st.error("Please upload CV")
        st.stop()

    if not job_offer.strip():
        st.error("Paste job offer")
        st.stop()

    with st.spinner("Parsing CV..."):

        cv_text = parse_cv(uploaded_cv)

    if not cv_text:
        st.error("Could not parse CV")
        st.stop()

    with st.spinner("Optimizing CV..."):

        data = optimize_cv(cv_text, job_offer, language)

    if show_json:
        st.json(data)

    with st.spinner("Generating PDF..."):

        pdf_path = build_cv_pdf(data)

    with open(pdf_path, "rb") as f:

        st.download_button(
            label="Download optimized CV",
            data=f.read(),
            file_name="optimized_cv.pdf",
            mime="application/pdf",
        )