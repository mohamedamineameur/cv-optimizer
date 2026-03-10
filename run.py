#!/usr/bin/env python3
"""
Point d'entrée principal de l'application
Compatible avec Streamlit Cloud et déploiement local
"""
import os
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    # Chemin vers le frontend
    frontend_path = Path(__file__).parent / "app" / "frontend" / "main.py"
    
    # Arguments de base pour Streamlit
    streamlit_args = [
        sys.executable,
        "-m", "streamlit", "run",
        str(frontend_path),
        "--server.headless", "true",
    ]
    
    # Ne spécifier le port que si on n'est pas sur Streamlit Cloud
    # Streamlit Cloud gère automatiquement les ports via PORT env var
    if not os.getenv("STREAMLIT_CLOUD"):
        # Pour déploiement local, utiliser le port spécifié ou 8501 par défaut
        port = os.getenv("PORT", "8501")
        streamlit_args.extend([
            "--server.port", port,
            "--server.address", "0.0.0.0"
        ])
    
    # Lancer Streamlit
    subprocess.run(streamlit_args)
