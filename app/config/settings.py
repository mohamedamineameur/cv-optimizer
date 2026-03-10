"""
Configuration centralisée de l'application
"""
import os
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass  # .env optionnel


class Settings:
    """Configuration de l'application"""
    
    def __init__(self):
        # OpenAI
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
        self.openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1")
        self.openai_temperature: float = float(os.getenv("OPENAI_TEMPERATURE", "0.0"))
        
        # Application
        self.app_name: str = os.getenv("APP_NAME", "ATS Resume Optimizer")
        self.app_version: str = os.getenv("APP_VERSION", "1.0.0")
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"
        
        # Paths
        self.base_dir: Path = Path(__file__).parent.parent.parent
        self.output_dir: Path = self.base_dir / "output"
        self.temp_dir: Path = self.base_dir / "temp"
        
        # PDF Generation
        self.pdf_highlight_enabled: bool = os.getenv("PDF_HIGHLIGHT_ENABLED", "false").lower() == "true"
        self.pdf_highlight_color: str = os.getenv("PDF_HIGHLIGHT_COLOR", "#FFF59D")
        
        # Logging
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.log_file: Optional[str] = os.getenv("LOG_FILE")
        
        # Créer les dossiers nécessaires
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)


# Instance globale des settings
settings = Settings()
