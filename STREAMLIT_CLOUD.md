# 🚀 Configuration Streamlit Cloud

## Problème Résolu

Le port 8501 était spécifié explicitement dans le code, ce qui causait des conflits avec Streamlit Cloud qui gère automatiquement les ports.

## Modifications Apportées

### 1. `run.py`
- ✅ Suppression du port codé en dur
- ✅ Détection automatique de Streamlit Cloud
- ✅ Utilisation de la variable d'environnement `PORT` si disponible
- ✅ Compatible avec déploiement local et Streamlit Cloud

### 2. `.streamlit/config.toml`
- ✅ Port commenté (géré automatiquement)
- ✅ Server address commenté (géré automatiquement)
- ✅ Configuration compatible avec Streamlit Cloud

### 3. `streamlit_config.toml`
- ✅ Même traitement que `.streamlit/config.toml`

## Configuration Streamlit Cloud

Streamlit Cloud détecte automatiquement :
- Le fichier `run.py` comme point d'entrée
- Le module principal depuis `app/frontend/main.py`
- Les dépendances depuis `requirements.txt`

## Variables d'Environnement

Pour Streamlit Cloud, configurez dans les paramètres de l'app :

1. **OPENAI_API_KEY** (requis)
   - Votre clé API OpenAI
   - Configuré dans Settings → Secrets

2. **STREAMLIT_CLOUD** (optionnel)
   - Défini automatiquement par Streamlit Cloud
   - Utilisé pour détecter l'environnement

## Déploiement Local

Pour un déploiement local, vous pouvez :

1. **Utiliser les valeurs par défaut** :
   ```bash
   python run.py
   # Utilisera le port 8501 par défaut
   ```

2. **Spécifier un port personnalisé** :
   ```bash
   PORT=8080 python run.py
   ```

3. **Décommenter dans `.streamlit/config.toml`** :
   ```toml
   [server]
   port = 8501
   address = "0.0.0.0"
   ```

## Vérification

Après déploiement sur Streamlit Cloud :

1. ✅ L'application devrait démarrer sans erreur de port
2. ✅ L'application devrait être accessible via l'URL Streamlit Cloud
3. ✅ Les logs ne devraient plus montrer "Port 8501 is not available"

## Structure Requise pour Streamlit Cloud

```
cv-optimizer/
├── run.py                    # Point d'entrée (requis)
├── requirements.txt          # Dépendances (requis)
├── .streamlit/
│   └── config.toml          # Configuration (optionnel)
├── app/
│   └── frontend/
│       └── main.py          # Application Streamlit
└── ...
```

## Notes Importantes

- Streamlit Cloud gère automatiquement HTTPS
- Les fichiers statiques doivent être dans le repo ou servis via un CDN
- Les secrets sont gérés via l'interface Streamlit Cloud
- Le port est géré automatiquement - ne pas le spécifier dans le code

## Dépannage

### Port toujours en conflit
- Vérifier qu'aucun port n'est spécifié dans le code
- Vérifier que `.streamlit/config.toml` n'a pas de port défini
- Redéployer l'application

### Application ne démarre pas
- Vérifier les logs dans Streamlit Cloud
- Vérifier que `run.py` existe et est exécutable
- Vérifier que `app/frontend/main.py` existe

### Variables d'environnement non chargées
- Vérifier la configuration dans Settings → Secrets
- Vérifier que les noms des variables sont corrects
- Redéployer après modification des secrets

---

**L'application est maintenant compatible avec Streamlit Cloud! ✅**
