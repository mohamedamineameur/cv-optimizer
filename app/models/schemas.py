"""
Modèles de données Pydantic pour la validation
"""
from typing import Any
from pydantic import BaseModel, Field


class HeaderModel(BaseModel):
    """Modèle pour l'en-tête du CV"""
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
    """Modèle pour une expérience professionnelle"""
    title: str = ""
    company: str = ""
    location: str = ""
    date: str = ""
    description: str = ""
    bullets: list[str] = Field(default_factory=list)
    links: dict[str, str] = Field(default_factory=dict)


class EducationItem(BaseModel):
    """Modèle pour une formation"""
    date: str = ""
    title: str = ""
    school: str = ""
    location: str = ""
    notes: str = ""


class ResumeModel(BaseModel):
    """Modèle complet du CV"""
    keywords: list[str] = Field(default_factory=list)
    header: HeaderModel = Field(default_factory=HeaderModel)
    presentation: str = ""
    work_experience: list[WorkExperienceItem] = Field(default_factory=list)
    education: list[EducationItem] = Field(default_factory=list)
    technical_skills: dict[str, list[str]] = Field(default_factory=dict)


class OptimizeCVRequest(BaseModel):
    """Requête pour optimiser un CV"""
    cv_text: str
    job_offer: str
    language: str = "EN"
    highlight_keywords: bool = False
    additional_experiences: list[dict[str, Any]] = Field(default_factory=list)


class OptimizeCVResponse(BaseModel):
    """Réponse de l'optimisation du CV"""
    success: bool
    resume_data: ResumeModel
    message: str = ""


class GenerateCoverLetterRequest(BaseModel):
    """Requête pour générer une lettre de motivation"""
    resume_data: ResumeModel
    job_offer: str
    language: str = "EN"


class GenerateCoverLetterResponse(BaseModel):
    """Réponse de la génération de lettre de motivation"""
    success: bool
    cover_letter_text: str = ""
    message: str = ""
