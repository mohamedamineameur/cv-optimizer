FROM python:3.12-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Créer les dossiers nécessaires
RUN mkdir -p output temp

# Exposer le port Streamlit
EXPOSE 8501

# Commande par défaut
CMD ["python", "-m", "streamlit", "run", "app/frontend/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
