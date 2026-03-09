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
    presentation: str = ""
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
        "presentation": "",
        "work_experience": [],
        "education": [],
        "technical_skills": {},
    }


def deep_merge_resume(base: dict[str, Any], incoming: dict[str, Any]):

    result = empty_resume_dict()

    result["header"] = {**result["header"], **incoming.get("header", {})}

    if isinstance(incoming.get("keywords"), list):
        result["keywords"] = incoming["keywords"]

    if isinstance(incoming.get("presentation"), str) and incoming.get("presentation"):
        result["presentation"] = incoming["presentation"]

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
- OPTIMIZE and ADAPT wording for ATS keyword matching with the job offer
- REWRITE work experience descriptions to be highly relevant to the job offer
- REMOVE non-relevant experiences or bullet points if they don't match the job requirements
- The title in header.title must match the job offer title BUT TRANSLATED to {cv_language} if the job offer is in a different language
- All text including titles, descriptions, and bullet points must be in {cv_language}
- Do NOT invent or add information that is not in the CV
- Prioritize relevance over completeness - quality over quantity
- Return ONLY valid JSON, no explanations or markdown

REQUIRED STRUCTURE:

{{
  "keywords": ["keywords", "that", "appear", "in", "BOTH", "job", "offer", "AND", "CV"],
  "header": {{
    "name": "Full name from CV",
    "title": "Professional title/role (TRANSLATED to {cv_language} to match the job offer)",
    "phone": "Phone number if present",
    "location": "City, Country",
    "email": "Email address",
    "linkedin": "LinkedIn URL if present",
    "portfolio": "Portfolio URL if present",
    "github": "GitHub URL if present",
    "languages": ["Language1", "Language2"]
  }},
  "presentation": "A compelling professional summary (3-5 sentences) that highlights the candidate's most relevant skills, experience, and achievements that match the job offer. This should be highly tailored to the specific position.",
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
- If a field truly doesn't exist in the CV, use empty string "" or empty array []
- DO NOT create empty work_experience or education entries if there are none in the CV

WORK EXPERIENCE OPTIMIZATION (CRITICAL):
- ADAPT the wording of each work experience to be HIGHLY RELEVANT to the job offer
- REWRITE job descriptions and bullet points using keywords and terminology from the job offer
- TRANSLATE job titles (work_experience.title) to {cv_language} if they are in a different language
- EMPHASIZE achievements and responsibilities that match the job requirements
- REMOVE or minimize bullet points and descriptions that are NOT relevant to the job offer
- If an experience has many bullet points, keep only the 3-5 most relevant ones for this position
- If an entire work experience is not relevant to the job offer, you may OMIT it completely
- Prioritize quality and relevance over quantity - fewer but highly relevant experiences are better
- Use action verbs and technical terms from the job offer in descriptions
- Make descriptions ATS-friendly while remaining truthful to the actual work done
- Focus on achievements that demonstrate skills mentioned in the job offer
- Write all descriptions, titles, and bullet points in {cv_language} language

PRESENTATION SECTION (CRITICAL):
- Create a compelling professional summary (3-5 sentences) that is HIGHLY RELEVANT to the job offer
- Highlight the candidate's most relevant skills, experience, and achievements that directly match the job requirements
- Use keywords from the job offer naturally in the presentation
- Focus on what makes the candidate an ideal fit for THIS specific position
- Write in {cv_language} language
- Make it impactful and ATS-friendly while remaining truthful
- This presentation should appear BEFORE the work experience section in the final resume

KEYWORDS SELECTION RULES (CRITICAL):
- Keywords MUST appear explicitly in the job offer text
- Keywords MUST also be present or clearly supported by the CV content
- Only include keywords that are BOTH in the job offer AND in the CV
- Focus on technical skills, technologies, tools, methodologies mentioned in BOTH documents
- Do NOT include generic terms that are not specifically mentioned in the job offer
- Do NOT include keywords that are only in the job offer but NOT in the CV
- Do NOT include keywords that are only in the CV but NOT in the job offer
- Maximum 15-20 most relevant keywords that match both documents
- Examples of valid keywords: "Python", "PostgreSQL", "AWS", "Docker", "React", "Microservices"
- Examples of invalid keywords: generic terms like "communication", "teamwork" unless specifically required in the offer
"""

    # Créer un prompt complet avec instructions + données
    full_prompt = f"""
You are an expert ATS resume optimizer. Your task is to extract ALL information from the CV text and structure it into a complete JSON resume.

CRITICAL INSTRUCTIONS:
- Extract EVERY piece of information from the CV text provided
- Fill ALL fields with actual data from the CV - do NOT leave fields empty if information exists
- The resume language must be {cv_language}
- OPTIMIZE and ADAPT wording for ATS keyword matching with the job offer
- REWRITE work experience descriptions to be highly relevant to the job offer
- REMOVE non-relevant experiences or bullet points if they don't match the job requirements
- The title in header.title must match the job offer title BUT TRANSLATED to {cv_language} if the job offer is in a different language
- All text including titles, descriptions, and bullet points must be in {cv_language}
- Do NOT invent or add information that is not in the CV
- Prioritize relevance over completeness - quality over quantity
- Return ONLY valid JSON, no explanations or markdown

REQUIRED STRUCTURE:

{{
  "keywords": ["keywords", "that", "appear", "in", "BOTH", "job", "offer", "AND", "CV"],
  "header": {{
    "name": "Full name from CV",
    "title": "Professional title/role (TRANSLATED to {cv_language} to match the job offer)",
    "phone": "Phone number if present",
    "location": "City, Country",
    "email": "Email address",
    "linkedin": "LinkedIn URL if present",
    "portfolio": "Portfolio URL if present",
    "github": "GitHub URL if present",
    "languages": ["Language1", "Language2"]
  }},
  "presentation": "A compelling professional summary (3-5 sentences) that highlights the candidate's most relevant skills, experience, and achievements that match the job offer. This should be highly tailored to the specific position.",
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
- If a field truly doesn't exist in the CV, use empty string "" or empty array []
- DO NOT create empty work_experience or education entries if there are none in the CV

WORK EXPERIENCE OPTIMIZATION (CRITICAL):
- ADAPT the wording of each work experience to be HIGHLY RELEVANT to the job offer
- REWRITE job descriptions and bullet points using keywords and terminology from the job offer
- TRANSLATE job titles (work_experience.title) to {cv_language} if they are in a different language
- EMPHASIZE achievements and responsibilities that match the job requirements
- REMOVE or minimize bullet points and descriptions that are NOT relevant to the job offer
- If an experience has many bullet points, keep only the 3-5 most relevant ones for this position
- If an entire work experience is not relevant to the job offer, you may OMIT it completely
- Prioritize quality and relevance over quantity - fewer but highly relevant experiences are better
- Use action verbs and technical terms from the job offer in descriptions
- Make descriptions ATS-friendly while remaining truthful to the actual work done
- Focus on achievements that demonstrate skills mentioned in the job offer
- Write all descriptions, titles, and bullet points in {cv_language} language

PRESENTATION SECTION (CRITICAL):
- Create a compelling professional summary (3-5 sentences) that is HIGHLY RELEVANT to the job offer
- Highlight the candidate's most relevant skills, experience, and achievements that directly match the job requirements
- Use keywords from the job offer naturally in the presentation
- Focus on what makes the candidate an ideal fit for THIS specific position
- Write in {cv_language} language
- Make it impactful and ATS-friendly while remaining truthful
- This presentation should appear BEFORE the work experience section in the final resume

KEYWORDS SELECTION RULES (CRITICAL):
- Keywords MUST appear explicitly in the job offer text
- Keywords MUST also be present or clearly supported by the CV content
- Only include keywords that are BOTH in the job offer AND in the CV
- Focus on technical skills, technologies, tools, methodologies mentioned in BOTH documents
- Do NOT include generic terms that are not specifically mentioned in the job offer
- Do NOT include keywords that are only in the job offer but NOT in the CV
- Do NOT include keywords that are only in the CV but NOT in the job offer
- Maximum 15-20 most relevant keywords that match both documents
- Examples of valid keywords: "Python", "PostgreSQL", "AWS", "Docker", "React", "Microservices"
- Examples of invalid keywords: generic terms like "communication", "teamwork" unless specifically required in the offer

JOB OFFER:
{job_offer}

CV TEXT (extract ALL information from this):
{cv_text}

IMPORTANT INSTRUCTIONS:
1. Extract every work experience, education entry, skill, and contact detail from the CV
2. OPTIMIZE each work experience for the job offer:
   - Rewrite descriptions and bullet points using keywords from the job offer
   - Remove or minimize non-relevant information
   - Keep only the most relevant experiences and achievements (3-5 bullet points max per experience)
   - You may completely omit experiences that are not relevant to the position
   - Prioritize relevance over completeness
3. Create a compelling professional presentation (3-5 sentences) that is HIGHLY RELEVANT to the job offer
   - Highlight the candidate's most relevant skills and achievements that match the job requirements
   - Use keywords from the job offer naturally
   - Make it impactful and tailored to THIS specific position
4. Do not leave fields empty if the information exists in the CV text above
5. For keywords: Select ONLY keywords that appear in BOTH the job offer AND the CV
   - Read the job offer carefully and identify key technical terms, technologies, tools
   - Check if these terms are also mentioned or supported in the CV
   - Only include keywords that match BOTH documents
   - Be selective: quality over quantity (15-20 most relevant keywords maximum)
"""

    # Envoyer le prompt complet deux fois pour meilleure compréhension
    completion = client.chat.completions.create(
        model="gpt-4.1",
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt},
            {"role": "user", "content": full_prompt},
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

# Section pour ajouter une expérience avant l'optimisation
st.divider()
st.subheader("➕ Add Work Experience (before optimization)")

additional_experiences = st.session_state.get('additional_experiences', [])

with st.expander("Add new work experience to include in CV", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        new_title = st.text_input("Job Title", key="pre_exp_title")
        new_company = st.text_input("Company", key="pre_exp_company")
        new_location = st.text_input("Location", key="pre_exp_location")
        new_date = st.text_input("Date (e.g., Jan 2020 - Dec 2022)", key="pre_exp_date")
    
    with col2:
        new_description = st.text_area("Description", height=100, key="pre_exp_desc")
        new_bullets_text = st.text_area(
            "Bullet points (one per line)", 
            height=100, 
            key="pre_exp_bullets",
            help="Enter one bullet point per line"
        )
    
    if st.button("Add Experience", key="add_pre_exp", type="primary"):
        if new_title and new_company:
            new_experience = {
                "title": new_title,
                "company": new_company,
                "location": new_location,
                "date": new_date,
                "description": new_description,
                "bullets": [b.strip() for b in new_bullets_text.split("\n") if b.strip()],
            }
            
            if 'additional_experiences' not in st.session_state:
                st.session_state['additional_experiences'] = []
            st.session_state['additional_experiences'].append(new_experience)
            st.success(f"Experience '{new_title}' at '{new_company}' added!")
            st.rerun()
        else:
            st.error("Please fill at least Title and Company")

# Afficher les expériences ajoutées
if additional_experiences:
    st.write(f"**{len(additional_experiences)} experience(s) added:**")
    for i, exp in enumerate(additional_experiences):
        with st.expander(f"{exp.get('title', 'N/A')} at {exp.get('company', 'N/A')} - {exp.get('date', '')}"):
            st.write(f"**Company:** {exp.get('company', '')}")
            st.write(f"**Location:** {exp.get('location', '')}")
            st.write(f"**Date:** {exp.get('date', '')}")
            st.write(f"**Description:** {exp.get('description', '')}")
            if exp.get('bullets'):
                st.write("**Bullet points:**")
                for bullet in exp.get('bullets', []):
                    st.write(f"- {bullet}")
            
            if st.button(f"Remove", key=f"remove_exp_{i}"):
                st.session_state['additional_experiences'].pop(i)
                st.rerun()

st.divider()

show_json = st.checkbox("Show JSON", value=False)

highlight_keywords = st.checkbox("Highlight keywords in PDF", value=False)


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

    # Ajouter les expériences supplémentaires au texte du CV
    additional_experiences = st.session_state.get('additional_experiences', [])
    if additional_experiences:
        cv_text += "\n\n=== ADDITIONAL WORK EXPERIENCE ===\n\n"
        for exp in additional_experiences:
            cv_text += f"Job Title: {exp.get('title', '')}\n"
            cv_text += f"Company: {exp.get('company', '')}\n"
            if exp.get('location'):
                cv_text += f"Location: {exp.get('location', '')}\n"
            if exp.get('date'):
                cv_text += f"Date: {exp.get('date', '')}\n"
            if exp.get('description'):
                cv_text += f"Description: {exp.get('description', '')}\n"
            if exp.get('bullets'):
                cv_text += "Achievements:\n"
                for bullet in exp.get('bullets', []):
                    cv_text += f"- {bullet}\n"
            cv_text += "\n"

    with st.spinner("Optimizing CV..."):

        data = optimize_cv(cv_text, job_offer, language)
        st.session_state['cv_data'] = data
        st.session_state['cv_language'] = language

    st.success("CV optimized successfully!")

# Afficher les données si disponibles
if 'cv_data' in st.session_state:
    data = st.session_state['cv_data']
    
    if show_json:
        st.json(data)
    
    # Génération du PDF
    st.divider()
    
    if st.button("Generate PDF", type="primary"):
        with st.spinner("Generating PDF..."):
            cv_language = st.session_state.get('cv_language', 'EN')
            pdf_path = build_cv_pdf(data, highlight=highlight_keywords, language=cv_language)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Download optimized CV",
                data=f.read(),
                file_name="optimized_cv.pdf",
                mime="application/pdf",
            )