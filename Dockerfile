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

# Exposer le port Streamlit (utilise PORT env var ou 8501 par défaut)
ARG PORT=8501
EXPOSE ${PORT}

# Variable d'environnement pour le port
ENV PORT=${PORT}

# Commande par défaut - utilise PORT depuis l'environnement
# Utiliser run.py qui gère automatiquement PORT
CMD ["python", "run.py"]
