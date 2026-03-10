"""
Service de génération de PDF
"""
from pathlib import Path
from app.config import settings
from app.utils import PDFGenerationError, logger


class PDFService:
    """Service pour générer les PDFs"""
    
    @staticmethod
    def generate_cv_pdf(resume_data: dict, language: str = "EN", highlight: bool = False) -> Path:
        """
        Génère un PDF de CV
        
        Args:
            resume_data: Données du CV
            language: Langue (EN ou FR)
            highlight: Activer le highlighting des mots-clés
            
        Returns:
            Chemin du fichier PDF généré
        """
        try:
            from cv_generator import build_cv_pdf
            
            output_path = settings.output_dir / "cv.pdf"
            pdf_path = build_cv_pdf(
                resume_data,
                output_path=str(output_path),
                highlight=highlight,
                language=language
            )
            
            logger.info(f"CV PDF généré: {pdf_path}")
            return Path(pdf_path)
            
        except Exception as e:
            logger.error(f"Erreur génération CV PDF: {e}")
            raise PDFGenerationError(f"Erreur lors de la génération du CV: {e}")
    
    @staticmethod
    def generate_cover_letter_pdf(
        cover_letter_text: str,
        header: dict,
        language: str = "EN"
    ) -> Path:
        """
        Génère un PDF de lettre de motivation
        
        Args:
            cover_letter_text: Texte de la lettre
            header: En-tête avec informations du candidat
            language: Langue (EN ou FR)
            
        Returns:
            Chemin du fichier PDF généré
        """
        try:
            from cover_letter_generator import build_cover_letter_pdf
            
            output_path = settings.output_dir / "cover_letter.pdf"
            pdf_path = build_cover_letter_pdf(
                cover_letter_text,
                header,
                language=language,
                output_path=str(output_path)
            )
            
            logger.info(f"Lettre de motivation PDF générée: {pdf_path}")
            return Path(pdf_path)
            
        except Exception as e:
            logger.error(f"Erreur génération lettre PDF: {e}")
            raise PDFGenerationError(f"Erreur lors de la génération de la lettre: {e}")
