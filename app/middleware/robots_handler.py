"""
Middleware pour servir robots.txt correctement
"""
from pathlib import Path
from streamlit.runtime.scriptrunner import get_script_run_ctx
import streamlit as st


def serve_robots_txt():
    """
    Servir robots.txt depuis le dossier static
    """
    static_dir = Path(__file__).parent.parent.parent / "static"
    robots_path = static_dir / "robots.txt"
    
    if robots_path.exists():
        return robots_path.read_text()
    
    # Fallback robots.txt minimal
    return "User-agent: *\nAllow: /\n"


def setup_robots_route():
    """
    Configurer la route robots.txt pour Streamlit
    Note: Streamlit ne supporte pas nativement les routes personnalisées,
    donc cette fonction doit être utilisée avec un reverse proxy (Nginx/Apache)
    ou un middleware personnalisé.
    """
    # Cette fonction est principalement pour documentation
    # L'implémentation réelle se fait via .htaccess ou nginx.conf
    pass
