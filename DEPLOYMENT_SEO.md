# 🚀 Guide de Déploiement SEO pour cv-optimizer.codecraftnest.ca

## Fichiers SEO Créés

### ✅ Fichiers Statiques
- `static/index.html` - Page d'accueil SEO-optimisée (363 lignes)
- `static/robots.txt` - Configuration pour les crawlers
- `static/sitemap.xml` - Plan du site pour les moteurs de recherche
- `static/faq.html` - Page FAQ pour contenu additionnel
- `static/manifest.json` - Manifest PWA

### ✅ Configuration Serveur
- `.htaccess` - Configuration Apache pour SEO
- `static/.htaccess` - Configuration pour fichiers statiques
- `streamlit_config.toml` - Configuration Streamlit

## Configuration Serveur

### Option 1 : Apache

1. **Copier les fichiers statiques** sur le serveur
2. **Configurer le VirtualHost** :

```apache
<VirtualHost *:80>
    ServerName cv-optimizer.codecraftnest.ca
    Redirect permanent / https://cv-optimizer.codecraftnest.ca/
</VirtualHost>

<VirtualHost *:443>
    ServerName cv-optimizer.codecraftnest.ca
    DocumentRoot /chemin/vers/pdf/static
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /chemin/vers/cert.pem
    SSLCertificateKeyFile /chemin/vers/key.pem
    
    # Servir index.html à la racine
    DirectoryIndex index.html
    
    # Proxy pour Streamlit app
    ProxyPass /app http://localhost:8501/
    ProxyPassReverse /app http://localhost:8501/
    
    # Servir fichiers statiques
    Alias /static /chemin/vers/pdf/static
    <Directory /chemin/vers/pdf/static>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    # Robots et sitemap
    Alias /robots.txt /chemin/vers/pdf/static/robots.txt
    Alias /sitemap.xml /chemin/vers/pdf/static/sitemap.xml
</VirtualHost>
```

### Option 2 : Nginx

```nginx
server {
    listen 80;
    server_name cv-optimizer.codecraftnest.ca;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name cv-optimizer.codecraftnest.ca;
    
    ssl_certificate /chemin/vers/cert.pem;
    ssl_certificate_key /chemin/vers/key.pem;
    
    root /chemin/vers/pdf/static;
    index index.html;
    
    # Page d'accueil
    location = / {
        try_files /index.html =404;
    }
    
    # Fichiers statiques
    location /static/ {
        alias /chemin/vers/pdf/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Robots et sitemap
    location = /robots.txt {
        alias /chemin/vers/pdf/static/robots.txt;
    }
    
    location = /sitemap.xml {
        alias /chemin/vers/pdf/static/sitemap.xml;
    }
    
    # FAQ
    location = /faq {
        try_files /faq.html =404;
    }
    
    # Proxy pour Streamlit
    location /app {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Compression
    gzip on;
    gzip_types text/html text/css application/javascript application/json;
    
    # Cache
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## Actions Post-Déploiement

### 1. Google Search Console
1. Ajouter la propriété : `cv-optimizer.codecraftnest.ca`
2. Vérifier la propriété (DNS ou fichier HTML)
3. Soumettre le sitemap : `https://cv-optimizer.codecraftnest.ca/sitemap.xml`

### 2. Google Analytics
1. Créer une propriété Google Analytics
2. Ajouter le code de suivi dans `index.html`

### 3. Vérifications SEO
- [ ] Tester avec Google PageSpeed Insights
- [ ] Vérifier mobile-friendly avec Google Mobile-Friendly Test
- [ ] Valider les structured data avec Schema.org Validator
- [ ] Vérifier l'indexation : `site:cv-optimizer.codecraftnest.ca`

### 4. Optimisations Additionnelles
- [ ] Créer des images optimisées (og-image.jpg, favicon.ico)
- [ ] Ajouter Google Analytics
- [ ] Créer un blog avec contenu SEO
- [ ] Obtenir des backlinks de qualité
- [ ] Optimiser les temps de chargement

## Métriques à Surveiller

- **Trafic organique** : Nombre de visiteurs depuis Google
- **Mots-clés** : Position dans les résultats de recherche
- **Taux de rebond** : Qualité du trafic
- **Temps sur site** : Engagement des utilisateurs
- **Conversions** : Utilisation de l'application

## Améliorations Continues

1. **Contenu** : Publier régulièrement du contenu SEO
2. **Backlinks** : Obtenir des liens depuis des sites de qualité
3. **Performance** : Optimiser les temps de chargement
4. **Mobile** : S'assurer que tout fonctionne parfaitement sur mobile
5. **Accessibilité** : Respecter les standards WCAG
