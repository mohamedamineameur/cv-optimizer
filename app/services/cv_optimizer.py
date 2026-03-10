"""
Service principal d'optimisation de CV
"""
from typing import Any
from app.models import ResumeModel
from app.services.openai_service import OpenAIService
from app.utils import logger


class CVOptimizer:
    """Service principal pour l'optimisation de CV"""
    
    def __init__(self):
        """Initialise le service"""
        self.openai_service = OpenAIService()
        logger.info("Service CVOptimizer initialisé")
    
    def optimize(
        self,
        cv_text: str,
        job_offer: str,
        language: str,
        additional_experiences: list[dict[str, Any]] = None
    ) -> ResumeModel:
        """
        Optimise un CV
        
        Args:
            cv_text: Texte du CV
            job_offer: Offre d'emploi
            language: Langue (EN ou FR)
            additional_experiences: Expériences supplémentaires à ajouter
            
        Returns:
            CV optimisé sous forme de ResumeModel
        """
        # Ajouter les expériences supplémentaires au texte
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
        
        # Optimiser avec OpenAI
        optimized_data = self.openai_service.optimize_cv(cv_text, job_offer, language)
        
        # Valider et retourner
        return ResumeModel.model_validate(optimized_data)
