"""
Service pour les interactions avec l'API OpenAI
"""
from openai import OpenAI
from app.config import settings
from app.utils import OpenAIError, logger


class OpenAIService:
    """Service pour gérer les appels à l'API OpenAI"""
    
    def __init__(self):
        """Initialise le client OpenAI"""
        if not settings.openai_api_key:
            raise OpenAIError("OPENAI_API_KEY non configurée")
        
        self.client = OpenAI(api_key=settings.openai_api_key)
        logger.info("Service OpenAI initialisé")
    
    def optimize_cv(self, cv_text: str, job_offer: str, language: str) -> dict:
        """
        Optimise un CV avec GPT-4
        
        Args:
            cv_text: Texte du CV
            job_offer: Offre d'emploi
            language: Langue (EN ou FR)
            
        Returns:
            Données du CV optimisé en JSON
            
        Raises:
            OpenAIError: Si l'appel API échoue
        """
        try:
            from app.services.prompts import get_cv_optimization_prompt
            
            cv_language = "French" if language == "FR" else "English"
            system_prompt, full_prompt = get_cv_optimization_prompt(
                cv_text, job_offer, cv_language
            )
            
            logger.info(f"Appel OpenAI pour optimisation CV (langue: {language})")
            
            completion = self.client.chat.completions.create(
                model=settings.openai_model,
                temperature=settings.openai_temperature,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_prompt},
                    {"role": "user", "content": full_prompt},  # Envoi double
                ]
            )
            
            content = completion.choices[0].message.content
            
            # Extraire le JSON
            import json
            start = content.find("{")
            end = content.rfind("}") + 1
            
            if start == -1 or end == 0:
                raise OpenAIError("Aucun JSON trouvé dans la réponse")
            
            json_text = content[start:end]
            result = json.loads(json_text)
            
            logger.info("CV optimisé avec succès")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Erreur de parsing JSON: {e}")
            raise OpenAIError(f"Erreur de parsing de la réponse: {e}")
        except Exception as e:
            logger.error(f"Erreur OpenAI: {e}")
            raise OpenAIError(f"Erreur lors de l'optimisation: {e}")
    
    def generate_cover_letter(self, cv_data: dict, job_offer: str, language: str) -> str:
        """
        Génère une lettre de motivation
        
        Args:
            cv_data: Données du CV optimisé
            job_offer: Offre d'emploi
            language: Langue (EN ou FR)
            
        Returns:
            Texte de la lettre de motivation
            
        Raises:
            OpenAIError: Si l'appel API échoue
        """
        try:
            from app.services.prompts import get_cover_letter_prompt
            
            cv_language = "French" if language == "FR" else "English"
            prompt = get_cover_letter_prompt(cv_data, job_offer, cv_language)
            
            logger.info(f"Génération lettre de motivation (langue: {language})")
            
            completion = self.client.chat.completions.create(
                model=settings.openai_model,
                temperature=0.7,
                messages=[
                    {"role": "system", "content": "You are an expert cover letter writer. Write professional, engaging, and tailored cover letters."},
                    {"role": "user", "content": prompt},
                ]
            )
            
            cover_letter_text = completion.choices[0].message.content.strip()
            logger.info("Lettre de motivation générée avec succès")
            
            return cover_letter_text
            
        except Exception as e:
            logger.error(f"Erreur génération lettre: {e}")
            raise OpenAIError(f"Erreur lors de la génération: {e}")
