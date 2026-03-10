#!/usr/bin/env python3
"""
Point d'entrée principal de l'application
Compatible avec Streamlit Cloud et déploiement local
Le port est toujours géré via la variable d'environnement PORT
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
    
    # Utiliser TOUJOURS la variable d'environnement PORT
    # Streamlit Cloud définit automatiquement PORT
    # Pour déploiement local, définir PORT dans l'environnement ou .env
    port = os.getenv("PORT")
    
    if port:
        # Si PORT est défini, l'utiliser
        streamlit_args.extend([
            "--server.port", port,
        ])
    # Si PORT n'est pas défini, Streamlit utilisera son port par défaut
    
    # Address seulement pour déploiement local (pas Streamlit Cloud)
    if not os.getenv("STREAMLIT_CLOUD"):
        streamlit_args.extend([
            "--server.address", "0.0.0.0"
        ])
    
    # Lancer Streamlit
    subprocess.run(streamlit_args)
