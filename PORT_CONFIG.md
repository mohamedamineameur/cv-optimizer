# 🔧 Configuration du Port - Variable d'Environnement PORT

## ✅ Modifications Appliquées

Tous les fichiers ont été modifiés pour utiliser **uniquement** la variable d'environnement `PORT` au lieu d'un port codé en dur.

## 📁 Fichiers Modifiés

### 1. `run.py` ✅
- Utilise `os.getenv("PORT")` 
- Si PORT n'est pas défini, Streamlit utilise son port par défaut
- Compatible avec Streamlit Cloud qui définit automatiquement PORT

### 2. `main.py` ✅
- Utilise `os.getenv("PORT", "8501")` pour l'exécutable standalone
- Valeur par défaut 8501 pour compatibilité locale

### 3. `.streamlit/config.toml` ✅
- Port commenté (géré automatiquement)

### 4. `streamlit_config.toml` ✅
- Port commenté (géré automatiquement)

### 5. `Dockerfile` ✅
- Utilise `ARG PORT=8501` avec valeur par défaut
- `ENV PORT=${PORT}` pour passer au runtime
- CMD utilise `${PORT}` depuis l'environnement

### 6. `docker-compose.yml` ✅
- Utilise `${PORT:-8501}` pour le mapping des ports
- Passe PORT comme variable d'environnement au conteneur

### 7. `nginx.conf` ✅
- Utilise `${PORT:-8501}` pour le proxy upstream
- Note: Nginx nécessite une configuration supplémentaire pour les variables d'environnement

## 🚀 Utilisation

### Streamlit Cloud
**Aucune action requise** - Streamlit Cloud définit automatiquement `PORT`

### Déploiement Local

**Option 1: Variable d'environnement**
```bash
export PORT=8501
python run.py
```

**Option 2: Fichier .env**
```bash
# Dans .env
PORT=8501
```

**Option 3: Ligne de commande**
```bash
PORT=8501 python run.py
```

### Docker

**Option 1: Variable d'environnement**
```bash
export PORT=8080
docker-compose up
```

**Option 2: Fichier .env**
```bash
# Dans .env
PORT=8080
docker-compose up
```

**Option 3: Build avec ARG**
```bash
docker build --build-arg PORT=8080 -t cv-optimizer .
docker run -e PORT=8080 -p 8080:8080 cv-optimizer
```

## 🔍 Vérification

Pour vérifier que le port est bien utilisé depuis l'environnement:

```bash
# Vérifier la variable PORT
echo $PORT

# Tester avec un port différent
PORT=9999 python run.py
# L'application devrait démarrer sur le port 9999
```

## ⚠️ Notes Importantes

1. **Streamlit Cloud**: PORT est défini automatiquement - ne pas le définir manuellement
2. **Docker**: Le port dans docker-compose.yml doit correspondre au PORT défini
3. **Nginx**: Pour utiliser une variable d'environnement dans nginx.conf, il faut utiliser `envsubst` ou définir le port dans la configuration

## 🐛 Dépannage

### Port toujours 8501
- Vérifier que PORT est bien défini: `echo $PORT`
- Vérifier le fichier .env
- Redémarrer le terminal/session

### Docker ne respecte pas PORT
- Vérifier que PORT est passé dans docker-compose.yml
- Vérifier les logs: `docker-compose logs`
- Rebuild: `docker-compose build --no-cache`

### Streamlit Cloud - Port en conflit
- Ne pas définir PORT manuellement dans Streamlit Cloud
- Streamlit Cloud gère automatiquement les ports
- Vérifier que `.streamlit/config.toml` n'a pas de port défini

---

**Tous les fichiers utilisent maintenant la variable d'environnement PORT! ✅**
