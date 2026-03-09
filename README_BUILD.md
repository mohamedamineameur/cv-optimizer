# Construction de l'exécutable Linux standalone

Ce guide explique comment créer un exécutable Linux autonome qui ne dépend plus de ce serveur.

## Prérequis

1. Python 3.12+ installé
2. Environnement virtuel activé avec toutes les dépendances

## Étapes de construction

### 1. Installer PyInstaller

```bash
source venv/bin/activate
pip install pyinstaller
```

### 2. Construire l'exécutable

Utilisez le script fourni :

```bash
./build_executable.sh
```

Ou manuellement :

```bash
pyinstaller ats_optimizer.spec
```

### 3. L'exécutable sera créé dans `dist/ats_optimizer`

Pour l'exécuter :

```bash
./dist/ats_optimizer
```

L'application Streamlit sera accessible sur `http://localhost:8501`

## Notes importantes

- L'exécutable inclut toutes les dépendances Python nécessaires
- Il nécessite toujours un fichier `.env` avec `OPENAI_API_KEY` dans le même répertoire
- L'exécutable est spécifique à l'architecture Linux (x86_64)
- Pour d'autres architectures, reconstruire sur la machine cible

## Structure des fichiers

- `main.py` : Point d'entrée de l'exécutable
- `ats_optimizer.spec` : Configuration PyInstaller
- `build_executable.sh` : Script de build automatisé
- `dist/ats_optimizer` : Exécutable final (créé après build)

## Distribution

Pour distribuer l'application :

1. Copier l'exécutable `dist/ats_optimizer`
2. Créer un fichier `.env` avec la clé API (ou demander à l'utilisateur de le créer)
3. L'exécutable peut être copié sur n'importe quelle machine Linux compatible
