#!/usr/bin/env python3
"""
Point d'entrée pour l'exécutable standalone.
Lance l'application Streamlit.
"""
import sys
import os

# Déterminer si on est dans un exécutable PyInstaller
if getattr(sys, 'frozen', False):
    # Si on est dans un exécutable, le répertoire de base est celui de l'exécutable
    BASE_DIR = sys._MEIPASS
    SCRIPT_DIR = os.path.dirname(sys.executable)
else:
    # Sinon, utiliser le répertoire du script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SCRIPT_DIR = BASE_DIR

# Ajouter le répertoire de base au chemin Python
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, SCRIPT_DIR)

# Importer et lancer Streamlit
if __name__ == "__main__":
    import streamlit.web.cli as stcli
    
    # Chemin vers le script Streamlit
    if getattr(sys, 'frozen', False):
        # Dans un exécutable PyInstaller, les fichiers sont dans sys._MEIPASS
        streamlit_script = os.path.join(BASE_DIR, "ats_optimizer.py")
        # Vérifier que le fichier existe
        if not os.path.exists(streamlit_script):
            print(f"ERREUR: Fichier introuvable: {streamlit_script}")
            print(f"BASE_DIR: {BASE_DIR}")
            print(f"Fichiers disponibles: {os.listdir(BASE_DIR)}")
            sys.exit(1)
    else:
        streamlit_script = os.path.join(SCRIPT_DIR, "ats_optimizer.py")
    
    # Arguments pour Streamlit
    sys.argv = [
        "streamlit",
        "run",
        streamlit_script,
        "--server.headless", "true",
        "--server.port", "8501",
        "--server.address", "0.0.0.0",
        "--browser.gatherUsageStats", "false"
    ]
    
    # Lancer Streamlit
    stcli.main()
