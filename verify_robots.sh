#!/bin/bash
# Script de vérification de robots.txt

echo "🔍 Vérification de robots.txt..."

URL="${1:-https://cv-optimizer.codecraftnest.ca/robots.txt}"

echo "URL testée: $URL"
echo ""

# Vérifier le contenu
CONTENT=$(curl -s "$URL" | head -20)

echo "Contenu reçu (20 premières lignes):"
echo "-----------------------------------"
echo "$CONTENT"
echo "-----------------------------------"
echo ""

# Vérifier le Content-Type
CONTENT_TYPE=$(curl -s -I "$URL" | grep -i "content-type" | head -1)
echo "Content-Type: $CONTENT_TYPE"

# Vérifier si c'est du HTML ou du texte
if echo "$CONTENT" | grep -q "<!DOCTYPE\|<html\|<head"; then
    echo "❌ ERREUR: robots.txt contient du HTML au lieu de texte pur!"
    echo ""
    echo "Solution:"
    echo "1. Vérifier que .htaccess ou nginx.conf intercepte /robots.txt"
    echo "2. Vérifier que /static/robots.txt existe et est en texte pur"
    echo "3. Redémarrer le serveur web"
    exit 1
else
    echo "✅ robots.txt est en format texte pur (valide)"
    
    # Vérifier la syntaxe de base
    if echo "$CONTENT" | grep -q "User-agent:"; then
        echo "✅ Contient 'User-agent:' (syntaxe valide)"
    else
        echo "⚠️  Avertissement: 'User-agent:' non trouvé"
    fi
    
    if echo "$CONTENT" | grep -q "Sitemap:"; then
        echo "✅ Contient 'Sitemap:'"
    else
        echo "⚠️  Avertissement: 'Sitemap:' non trouvé"
    fi
fi

echo ""
echo "✅ Vérification terminée"
