# Architecture du Projet

## Structure du Projet

```
pdf/
├── app/
│   ├── __init__.py
│   ├── config/              # Configuration centralisée
│   │   ├── __init__.py
│   │   └── settings.py      # Settings de l'application
│   ├── models/              # Modèles de données
│   │   ├── __init__.py
│   │   └── schemas.py       # Schémas Pydantic
│   ├── services/            # Services métier
│   │   ├── __init__.py
│   │   ├── cv_extractor.py  # Extraction de texte CV
│   │   ├── cv_optimizer.py  # Service principal d'optimisation
│   │   ├── openai_service.py # Service OpenAI
│   │   ├── pdf_service.py   # Génération PDF
│   │   └── prompts.py       # Gestion des prompts
│   ├── utils/               # Utilitaires
│   │   ├── __init__.py
│   │   ├── logger.py        # Configuration logging
│   │   └── exceptions.py    # Exceptions personnalisées
│   └── frontend/            # Interface utilisateur
│       └── main.py          # Application Streamlit
├── cv_generator.py          # Générateur PDF CV (legacy, à migrer)
├── cover_letter_generator.py # Générateur PDF lettre (legacy, à migrer)
├── requirements.txt         # Dépendances Python
├── Dockerfile              # Configuration Docker
├── docker-compose.yml      # Docker Compose
├── run.py                 # Point d'entrée principal
└── README.md              # Documentation

```

## Architecture en Couches

### 1. Configuration (`app/config/`)
- **Settings centralisés** : Toutes les configurations via variables d'environnement
- **Gestion des chemins** : Dossiers output/temp automatiquement créés
- **Validation** : Vérification des configurations requises

### 2. Modèles (`app/models/`)
- **Schémas Pydantic** : Validation stricte des données
- **Types de données** : Modèles pour CV, requêtes, réponses
- **Sérialisation** : Conversion automatique JSON ↔ Objets Python

### 3. Services (`app/services/`)
- **CVExtractor** : Extraction de texte depuis PDF/DOCX
- **CVOptimizer** : Orchestration de l'optimisation
- **OpenAIService** : Interactions avec l'API OpenAI
- **PDFService** : Génération de PDFs
- **Prompts** : Gestion centralisée des prompts

### 4. Utilitaires (`app/utils/`)
- **Logger** : Système de logging configurable
- **Exceptions** : Exceptions personnalisées avec gestion d'erreurs

### 5. Frontend (`app/frontend/`)
- **Streamlit** : Interface utilisateur moderne
- **Gestion d'état** : Session state pour persistance
- **UX améliorée** : Meilleure organisation et feedback utilisateur

## Flux de Données

```
User Input (CV + Job Offer)
    ↓
Frontend (Streamlit)
    ↓
CVExtractor → CV Text
    ↓
CVOptimizer
    ↓
OpenAIService → Optimized Data
    ↓
ResumeModel (Validation)
    ↓
PDFService → PDF Files
    ↓
User Download
```

## Principes de Design

### Separation of Concerns
- Chaque service a une responsabilité unique
- Pas de couplage fort entre les modules
- Interfaces claires entre les couches

### Dependency Injection
- Services injectés plutôt que créés directement
- Facilite les tests et la maintenance

### Error Handling
- Exceptions personnalisées par type d'erreur
- Logging systématique des erreurs
- Messages d'erreur clairs pour l'utilisateur

### Configuration Management
- Toutes les configs via variables d'environnement
- Fichier .env pour développement local
- Support Docker avec docker-compose

## Améliorations Futures

1. **API REST** : Ajouter FastAPI pour séparer complètement backend/frontend
2. **Base de données** : Stocker les CVs optimisés (optionnel)
3. **Cache** : Mettre en cache les résultats OpenAI
4. **Tests** : Ajouter tests unitaires et d'intégration
5. **CI/CD** : Pipeline de déploiement automatisé
6. **Monitoring** : Métriques et observabilité
