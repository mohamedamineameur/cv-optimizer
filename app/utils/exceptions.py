"""
Exceptions personnalisées pour l'application
"""


class ATSError(Exception):
    """Exception de base pour l'application"""
    pass


class CVParseError(ATSError):
    """Erreur lors du parsing du CV"""
    pass


class OpenAIError(ATSError):
    """Erreur avec l'API OpenAI"""
    pass


class PDFGenerationError(ATSError):
    """Erreur lors de la génération du PDF"""
    pass


class ValidationError(ATSError):
    """Erreur de validation des données"""
    pass
