#!/bin/bash
# Script pour créer un exécutable Linux standalone

set -e

echo "🔨 Construction de l'exécutable Linux..."

# Activer l'environnement virtuel
source venv/bin/activate

# Vérifier que PyInstaller est installé
if ! command -v pyinstaller &> /dev/null; then
    echo "📦 Installation de PyInstaller..."
    pip install pyinstaller
fi

# Créer le répertoire de build s'il n'existe pas
mkdir -p dist

# Nettoyer les builds précédents
echo "🧹 Nettoyage des builds précédents..."
rm -rf build dist/ats_optimizer

# Construire l'exécutable avec le fichier .spec
echo "⚙️  Construction de l'exécutable..."
pyinstaller ats_optimizer.spec

echo "✅ Exécutable créé dans dist/ats_optimizer"
echo "📝 Pour l'exécuter: ./dist/ats_optimizer"
