"""
Gestion des prompts pour OpenAI
"""


def get_cv_optimization_prompt(cv_text: str, job_offer: str, cv_language: str) -> tuple[str, str]:
    """
    Génère les prompts pour l'optimisation du CV
    
    Returns:
        Tuple (system_prompt, full_prompt)
    """
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
"""

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
      "links": {{"Application": "https://example.com", "GitHub": "https://github.com/...", "Company website": "https://company.com"}}
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
- Extract ALL links from work experiences - look for URLs in formats like:
  * "Application: https://...", "App: https://...", "Website: https://..."
  * "GitHub: https://...", "Github: https://...", "Repo: https://..."
  * "Company website: https://...", "Portfolio: https://..."
  * Any URL pattern (http:// or https://) mentioned in the work experience section
- PRESERVE all links found in the CV - they are important and must be kept
- Store links in the links field as a dictionary: {{"Application": "url", "GitHub": "url", "Company website": "url"}}
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
- ALWAYS PRESERVE links (work_experience.links) from the original CV - do NOT remove or modify them
- If links exist in the CV, extract and keep ALL of them in the links field
- Look carefully for links in formats like "Application: url", "GitHub: url", "Company website: url", etc.
- Links can include project URLs, GitHub repositories, portfolio links, company websites, demo links, etc.
- Store each link with its label (e.g., "Application", "GitHub", "Company website") as the key and the URL as the value
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

    return system_prompt, full_prompt


def get_cover_letter_prompt(cv_data: dict, job_offer: str, cv_language: str) -> str:
    """
    Génère le prompt pour la lettre de motivation
    """
    header = cv_data.get("header", {})
    name = header.get("name", "")
    title = header.get("title", "")
    email = header.get("email", "")
    phone = header.get("phone", "")
    location = header.get("location", "")
    
    work_experience = cv_data.get("work_experience", [])
    technical_skills = cv_data.get("technical_skills", {})
    keywords = cv_data.get("keywords", [])
    
    skills_summary = []
    for category, skills in technical_skills.items():
        skills_summary.extend(skills[:5])
    
    return f"""
You are an expert cover letter writer. Write a professional cover letter in {cv_language} language.

REQUIREMENTS:
- Write in {cv_language} language
- Professional tone, engaging, and tailored to the specific job offer
- 3-4 paragraphs maximum
- First paragraph: Introduction and why you're interested in this position
- Second paragraph: Highlight your most relevant experience and achievements that match the job requirements
- Third paragraph: Emphasize your key skills and how they align with the company's needs
- Fourth paragraph (optional): Closing statement expressing enthusiasm and next steps
- Use keywords from the job offer naturally
- Be specific and concrete, not generic
- Show enthusiasm but remain professional

CANDIDATE INFORMATION:
Name: {name}
Title: {title}
Email: {email}
Phone: {phone}
Location: {location}

KEY SKILLS: {', '.join(skills_summary[:15])}
KEYWORDS FROM JOB: {', '.join(keywords[:15])}

RECENT EXPERIENCE SUMMARY:
{chr(10).join([f"- {exp.get('title', '')} at {exp.get('company', '')}: {exp.get('description', '')[:200]}" for exp in work_experience[:3]])}

JOB OFFER:
{job_offer}

Write ONLY the cover letter content (no subject line, no "Dear Hiring Manager" - start directly with the first paragraph). 
The letter should be well-formatted with proper paragraphs and professional language.
"""
