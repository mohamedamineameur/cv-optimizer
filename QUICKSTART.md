# 🚀 Guide de Démarrage Rapide

## Installation Express

```bash
# 1. Activer l'environnement virtuel
source venv/bin/activate

# 2. Installer les dépendances (si pas déjà fait)
pip install -r requirements.txt

# 3. Créer le fichier .env
echo "OPENAI_API_KEY=votre_cle_api" > .env

# 4. Lancer l'application
python run.py
```

## Structure du Projet Refactorisé

```
app/
├── config/          → Configuration (settings.py)
├── models/          → Modèles de données (schemas.py)
├── services/        → Services métier
│   ├── cv_extractor.py      # Extraction PDF/DOCX
│   ├── cv_optimizer.py      # Optimisation CV
│   ├── openai_service.py    # API OpenAI
│   ├── pdf_service.py       # Génération PDF
│   └── prompts.py           # Prompts GPT
├── utils/           → Utilitaires
│   ├── logger.py           # Logging
│   └── exceptions.py       # Exceptions
└── frontend/        → Interface Streamlit
    └── main.py             # Application principale
```

## Points Clés de l'Architecture

### ✅ Séparation des Responsabilités
- Chaque service a un rôle unique et bien défini
- Pas de couplage fort entre les modules

### ✅ Configuration Centralisée
- Tout dans `app/config/settings.py`
- Variables d'environnement via `.env`

### ✅ Gestion d'Erreurs
- Exceptions personnalisées
- Logging systématique
- Messages clairs pour l'utilisateur

### ✅ Validation des Données
- Schémas Pydantic pour validation stricte
- Types de données clairs

### ✅ Code Maintenable
- Documentation complète
- Structure modulaire
- Facile à étendre

## Utilisation

1. **Upload CV** : PDF ou DOCX
2. **Coller l'offre d'emploi**
3. **Ajouter des expériences** (optionnel)
4. **Optimiser** : Le système génère un CV optimisé
5. **Générer PDF** : Télécharger le CV et/ou la lettre de motivation

## Docker

```bash
docker-compose up
```

## Support

- `ARCHITECTURE.md` : Documentation détaillée de l'architecture
- `MIGRATION.md` : Guide de migration depuis l'ancien code
- `REFACTORING_SUMMARY.md` : Résumé des changements
