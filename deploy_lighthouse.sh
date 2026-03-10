#!/bin/bash
# Script de déploiement des optimisations Lighthouse

set -e

echo "🚀 Déploiement des optimisations Lighthouse..."

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Vérifier que nous sommes à la racine du projet
if [ ! -f "run.py" ]; then
    echo -e "${RED}❌ Erreur: Ce script doit être exécuté depuis la racine du projet${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Vérification de l'environnement..."

# Vérifier les fichiers nécessaires
FILES=(
    ".streamlit/config.toml"
    ".htaccess"
    "nginx.conf"
    "static/robots.txt"
    "static/sitemap.xml"
)

for file in "${FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${YELLOW}⚠${NC}  Fichier manquant: $file"
    else
        echo -e "${GREEN}✓${NC}  $file"
    fi
done

echo ""
echo -e "${YELLOW}📋 Instructions de déploiement:${NC}"
echo ""
echo "1. Pour Apache:"
echo "   - Copier .htaccess à la racine du serveur web"
echo "   - Vérifier que mod_rewrite, mod_headers, mod_deflate, mod_expires sont activés"
echo "   - Redémarrer Apache: sudo systemctl restart apache2"
echo ""
echo "2. Pour Nginx:"
echo "   - Copier nginx.conf dans /etc/nginx/sites-available/"
echo "   - Créer un lien: sudo ln -s /etc/nginx/sites-available/cv-optimizer /etc/nginx/sites-enabled/"
echo "   - Tester: sudo nginx -t"
echo "   - Redémarrer: sudo systemctl restart nginx"
echo ""
echo "3. Vérifier robots.txt:"
echo "   - Visiter: https://cv-optimizer.codecraftnest.ca/robots.txt"
echo "   - Doit afficher du texte pur (pas de HTML)"
echo ""
echo "4. Tester avec Lighthouse:"
echo "   - Ouvrir Chrome DevTools"
echo "   - Onglet Lighthouse"
echo "   - Lancer l'audit"
echo ""
echo -e "${GREEN}✅ Optimisations prêtes pour déploiement!${NC}"
