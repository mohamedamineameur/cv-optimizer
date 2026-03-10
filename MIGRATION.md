# Guide de Migration vers la Nouvelle Architecture

## Changements Principaux

Le projet a été complètement refactorisé avec une architecture professionnelle full stack.

## Nouvelle Structure

### Avant
```
pdf/
├── ats_optimizer.py  (tout mélangé)
├── cv_generator.py
└── cover_letter_generator.py
```

### Après
```
pdf/
├── app/
│   ├── config/       # Configuration
│   ├── models/       # Modèles de données
│   ├── services/    # Services métier
│   ├── utils/       # Utilitaires
│   └── frontend/    # Interface utilisateur
├── cv_generator.py  # (conservé pour compatibilité)
└── cover_letter_generator.py  # (conservé pour compatibilité)
```

## Comment Utiliser

### Option 1 : Utiliser la nouvelle architecture (recommandé)

```bash
# Lancer l'application
python run.py

# Ou directement avec Streamlit
streamlit run app/frontend/main.py
```

### Option 2 : Utiliser l'ancien fichier (toujours fonctionnel)

```bash
streamlit run ats_optimizer.py
```

## Avantages de la Nouvelle Architecture

1. **Séparation des responsabilités** : Chaque module a un rôle clair
2. **Maintenabilité** : Code plus facile à comprendre et modifier
3. **Testabilité** : Services isolés, faciles à tester
4. **Scalabilité** : Facile d'ajouter de nouvelles fonctionnalités
5. **Configuration centralisée** : Tout dans `app/config/settings.py`
6. **Gestion d'erreurs** : Exceptions personnalisées et logging
7. **Documentation** : Code mieux documenté

## Migration Progressive

Les anciens fichiers (`ats_optimizer.py`, `cv_generator.py`, etc.) sont toujours fonctionnels.
Vous pouvez migrer progressivement vers la nouvelle architecture.

## Configuration

Créez un fichier `.env` à la racine :

```env
OPENAI_API_KEY=votre_cle_api
OPENAI_MODEL=gpt-4.1
LOG_LEVEL=INFO
```

## Docker

Pour utiliser Docker :

```bash
docker-compose up
```

L'application sera accessible sur `http://localhost:8501`
