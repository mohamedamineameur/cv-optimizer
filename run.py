#!/usr/bin/env python3
"""
Point d'entrée principal de l'application
"""
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    # Chemin vers le frontend
    frontend_path = Path(__file__).parent / "app" / "frontend" / "main.py"
    
    # Lancer Streamlit
    subprocess.run([
        sys.executable,
        "-m", "streamlit", "run",
        str(frontend_path),
        "--server.headless", "true",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])
