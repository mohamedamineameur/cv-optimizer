"""
Service d'extraction de texte depuis les fichiers CV
"""
import docx
import pdfplumber
from typing import BinaryIO
from app.utils import CVParseError, logger


class CVExtractor:
    """Service pour extraire le texte des fichiers CV"""
    
    @staticmethod
    def extract_from_pdf(file: BinaryIO) -> str:
        """
        Extrait le texte d'un fichier PDF
        
        Args:
            file: Fichier PDF en mode binaire
            
        Returns:
            Texte extrait du PDF
            
        Raises:
            CVParseError: Si l'extraction échoue
        """
        try:
            text = ""
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            if not text.strip():
                raise CVParseError("Aucun texte trouvé dans le PDF")
            
            logger.info(f"Extrait {len(text)} caractères du PDF")
            return text.strip()
            
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction PDF: {e}")
            raise CVParseError(f"Impossible d'extraire le texte du PDF: {e}")
    
    @staticmethod
    def extract_from_docx(file: BinaryIO) -> str:
        """
        Extrait le texte d'un fichier DOCX
        
        Args:
            file: Fichier DOCX en mode binaire
            
        Returns:
            Texte extrait du DOCX
            
        Raises:
            CVParseError: Si l'extraction échoue
        """
        try:
            doc = docx.Document(file)
            text = "\n".join(p.text for p in doc.paragraphs if p.text)
            
            if not text.strip():
                raise CVParseError("Aucun texte trouvé dans le DOCX")
            
            logger.info(f"Extrait {len(text)} caractères du DOCX")
            return text.strip()
            
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction DOCX: {e}")
            raise CVParseError(f"Impossible d'extraire le texte du DOCX: {e}")
    
    @staticmethod
    def extract(file, filename: str) -> str:
        """
        Extrait le texte d'un fichier CV (PDF ou DOCX)
        
        Args:
            file: Fichier en mode binaire
            filename: Nom du fichier
            
        Returns:
            Texte extrait
            
        Raises:
            CVParseError: Si le format n'est pas supporté ou si l'extraction échoue
        """
        filename_lower = filename.lower()
        
        if filename_lower.endswith(".pdf"):
            return CVExtractor.extract_from_pdf(file)
        elif filename_lower.endswith(".docx"):
            return CVExtractor.extract_from_docx(file)
        else:
            raise CVParseError(f"Format de fichier non supporté: {filename}")
