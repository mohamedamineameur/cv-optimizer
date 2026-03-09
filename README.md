# 📄 ATS Resume Optimizer

Un outil intelligent d'optimisation de CV pour les systèmes ATS (Applicant Tracking Systems) utilisant l'intelligence artificielle pour améliorer la correspondance entre votre CV et les offres d'emploi.

## 🎯 Objectif du Projet

Ce projet permet de :
- **Extraire automatiquement** les informations d'un CV (PDF ou DOCX)
- **Optimiser le CV** pour maximiser le score ATS en utilisant l'IA (GPT-4)
- **Générer un PDF professionnel** avec mise en évidence optionnelle des mots-clés
- **Ajouter des expériences** manuellement avant l'optimisation
- **Supporter plusieurs langues** (Français et Anglais)

## ✨ Fonctionnalités

### 🔍 Extraction et Analyse
- Extraction de texte depuis les fichiers PDF et DOCX
- Analyse intelligente du contenu du CV
- Identification automatique des mots-clés pertinents de l'offre d'emploi

### 🤖 Optimisation par IA
- Utilisation de GPT-4 pour restructurer et optimiser le CV
- Sélection intelligente des mots-clés qui correspondent à la fois au CV et à l'offre
- Réécriture optimisée pour l'ATS tout en préservant la véracité des informations

### 📝 Édition Manuelle
- Ajout d'expériences professionnelles avant l'optimisation
- Interface intuitive pour compléter les informations manquantes

### 📄 Génération PDF
- Génération de PDF professionnel avec ReportLab
- Mise en évidence optionnelle des mots-clés ATS
- Support multilingue (FR/EN) pour les titres de sections

### 🚀 Déploiement
- Création d'exécutable standalone Linux avec PyInstaller
- Application web avec Streamlit

## 🏗️ Architecture du Projet

### Structure des Fichiers

```
pdf/
├── ats_optimizer.py      # Application principale Streamlit + logique métier
├── cv_generator.py       # Générateur de PDF avec ReportLab
├── main.py              # Point d'entrée pour l'exécutable
├── ats_optimizer.spec   # Configuration PyInstaller
├── build_executable.sh  # Script de build automatisé
├── .env                 # Variables d'environnement (API keys)
└── README.md            # Documentation
```

### Architecture Logicielle

```
┌─────────────────────────────────────────┐
│         Interface Streamlit             │
│  (Upload CV, Job Offer, Options)        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Extraction de Texte               │
│  (pdfplumber, python-docx)             │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Optimisation IA (GPT-4)            │
│  (OpenAI API + Prompts structurés)     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Validation Pydantic                │
│  (Schémas de données)                   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Génération PDF                     │
│  (ReportLab + Highlighting)            │
└─────────────────────────────────────────┘
```

## 🛠️ Technologies Utilisées

### Backend & Core
- **Python 3.12+** : Langage principal
- **Streamlit** : Framework web pour l'interface utilisateur
- **OpenAI API (GPT-4)** : Intelligence artificielle pour l'optimisation
- **Pydantic** : Validation et modélisation des données avec types stricts

### Extraction de Données
- **pdfplumber** : Extraction de texte depuis les fichiers PDF
- **python-docx** : Lecture des fichiers Word (.docx)

### Génération PDF
- **ReportLab** : Bibliothèque de génération de PDF professionnels
  - `SimpleDocTemplate` : Structure du document
  - `Paragraph` : Formatage de texte
  - `Table` : Mise en page tabulaire
  - `ListFlowable` : Listes à puces

### Déploiement
- **PyInstaller** : Création d'exécutables standalone
- **python-dotenv** : Gestion des variables d'environnement

### Utilitaires
- **re** (regex) : Recherche et remplacement de texte pour le highlighting
- **json** : Manipulation des données structurées
- **typing** : Annotations de types pour la qualité du code

## 📋 Dépendances

Les dépendances principales sont listées ci-dessous :

```python
streamlit>=1.55.0        # Interface web
openai>=1.0.0            # API OpenAI
pydantic>=2.0.0          # Validation de données
pdfplumber>=0.11.0       # Extraction PDF
python-docx>=1.1.0       # Lecture Word
reportlab>=4.0.0         # Génération PDF
python-dotenv>=1.0.0     # Variables d'environnement
pyinstaller>=6.0.0       # Création d'exécutable
```

## 🚀 Installation

### Prérequis
- Python 3.12 ou supérieur
- Clé API OpenAI

### Étapes d'Installation

1. **Cloner ou télécharger le projet**
```bash
cd /home/amine/Bureau/python/pdf
```

2. **Créer un environnement virtuel**
```bash
python3 -m venv venv
source venv/bin/activate  # Sur Linux/Mac
```

3. **Installer les dépendances**
```bash
pip install streamlit openai pydantic pdfplumber python-docx reportlab python-dotenv pyinstaller
```

4. **Configurer les variables d'environnement**
Créer un fichier `.env` à la racine du projet :
```env
OPENAI_API_KEY=votre_cle_api_openai
```

## 💻 Utilisation

### Mode Application Web (Streamlit)

```bash
source venv/bin/activate
streamlit run ats_optimizer.py
```

L'application sera accessible sur `http://localhost:8501`

### Mode Exécutable Standalone

1. **Construire l'exécutable**
```bash
./build_executable.sh
```

2. **Exécuter l'exécutable**
```bash
./dist/ats_optimizer
```

## 📖 Guide d'Utilisation

### 1. Préparation
- Sélectionner la langue du CV (FR ou EN)
- Uploader votre CV au format PDF ou DOCX
- Coller le texte de l'offre d'emploi

### 2. Ajout d'Expériences (Optionnel)
- Utiliser la section "Add Work Experience (before optimization)"
- Remplir les champs : Titre, Entreprise, Localisation, Date, Description, Bullet points
- Les expériences seront incluses dans le CV envoyé au modèle

### 3. Optimisation
- Cliquer sur "Optimize CV"
- Le système va :
  1. Extraire le texte du CV
  2. Analyser l'offre d'emploi
  3. Optimiser avec GPT-4
  4. Générer un JSON structuré

### 4. Génération PDF
- Optionnel : Activer "Highlight keywords in PDF" pour surligner les mots-clés
- Cliquer sur "Generate PDF"
- Télécharger le CV optimisé

## 🔧 Détails Techniques

### Extraction de Texte

Le système utilise deux bibliothèques selon le format :

**PDF (pdfplumber)** :
```python
with pdfplumber.open(file) as pdf:
    for page in pdf.pages:
        text += page.extract_text() + "\n"
```

**DOCX (python-docx)** :
```python
doc = docx.Document(file)
return "\n".join(p.text for p in doc.paragraphs if p.text)
```

### Optimisation IA

Le prompt système est structuré pour :
1. Extraire toutes les informations du CV
2. Identifier les mots-clés pertinents (présents dans CV ET offre)
3. Optimiser le wording pour l'ATS
4. Retourner un JSON structuré

**Schéma de données Pydantic** :
```python
class ResumeModel(BaseModel):
    keywords: list[str]
    header: HeaderModel
    work_experience: list[WorkExperienceItem]
    education: list[EducationItem]
    technical_skills: dict[str, list[str]]
```

### Génération PDF

Le générateur PDF utilise ReportLab avec :
- **Styles personnalisés** : Titres, sections, texte normal
- **Mise en page** : Marges, espacements, alignements
- **Highlighting** : Surlignage des mots-clés avec regex
- **Multilingue** : Traductions des sections selon la langue

**Exemple de highlighting** :
```python
def highlight_text(text, keywords, highlight=False):
    for word in keywords:
        pattern = re.compile(rf"\b({re.escape(word)})\b", re.IGNORECASE)
        text = pattern.sub(
            rf'<span backColor="{HIGHLIGHT_BG}"><b>\1</b></span>',
            text
        )
    return text
```

### Gestion des Langues

Le système supporte le français et l'anglais avec des traductions :

```python
translations = {
    "EN": {
        "work_experience": "WORK EXPERIENCE",
        "education": "EDUCATION",
        "technical_skills": "TECHNICAL SKILLS",
    },
    "FR": {
        "work_experience": "EXPÉRIENCE PROFESSIONNELLE",
        "education": "FORMATION",
        "technical_skills": "COMPÉTENCES TECHNIQUES",
    }
}
```

## 🎨 Fonctionnalités Avancées

### Highlighting des Mots-clés

Les mots-clés ATS peuvent être surlignés en jaune dans le PDF généré pour visualiser rapidement la correspondance avec l'offre.

### Ajout d'Expériences

Permet d'ajouter des expériences professionnelles manuellement avant l'optimisation. Ces expériences sont formatées et intégrées au texte du CV envoyé au modèle.

### Validation de Données

Utilisation de Pydantic pour :
- Valider la structure des données
- S'assurer de la cohérence des types
- Fournir des messages d'erreur clairs

## 📦 Création d'Exécutable

Le projet inclut un système de build pour créer un exécutable standalone :

1. **Configuration PyInstaller** (`ats_optimizer.spec`)
   - Inclut toutes les dépendances
   - Collecte les données nécessaires (Streamlit, ReportLab, etc.)
   - Crée un exécutable one-file

2. **Script de Build** (`build_executable.sh`)
   - Automatise le processus
   - Nettoie les builds précédents
   - Génère l'exécutable dans `dist/`

## 🔒 Sécurité

- Les clés API sont stockées dans `.env` (non versionné)
- Le fichier `.gitignore` exclut les fichiers sensibles
- Validation des entrées utilisateur

## 📝 Structure des Données

### Format JSON du CV

```json
{
  "keywords": ["Python", "PostgreSQL", "AWS"],
  "header": {
    "name": "John Doe",
    "title": "Software Engineer",
    "email": "john@example.com",
    "phone": "+1234567890",
    "location": "Paris, France",
    "linkedin": "https://linkedin.com/in/johndoe",
    "github": "https://github.com/johndoe",
    "languages": ["French", "English"]
  },
  "work_experience": [
    {
      "title": "Senior Developer",
      "company": "Tech Corp",
      "location": "Paris",
      "date": "2020-2023",
      "description": "Led development team",
      "bullets": ["Achievement 1", "Achievement 2"],
      "links": {}
    }
  ],
  "education": [
    {
      "date": "2018",
      "title": "Master in Computer Science",
      "school": "University",
      "location": "Paris",
      "notes": "Magna Cum Laude"
    }
  ],
  "technical_skills": {
    "Languages": ["Python", "JavaScript"],
    "Frameworks": ["React", "Django"]
  }
}
```

## 🐛 Dépannage

### Erreur "OPENAI_API_KEY not found"
- Vérifier que le fichier `.env` existe
- Vérifier que la clé API est correctement définie

### Erreur lors de l'extraction PDF
- Vérifier que le PDF n'est pas protégé par mot de passe
- Essayer de convertir en DOCX si le PDF est scanné

### Erreur lors de la génération PDF
- Vérifier que toutes les données requises sont présentes
- Vérifier les logs pour plus de détails

## 📄 Licence

Ce projet est un outil personnel d'optimisation de CV.

## 👤 Auteur

Développé pour optimiser les CVs et améliorer les chances de passage des systèmes ATS.

## 🔮 Améliorations Futures

- Support de plus de formats de fichiers
- Export en différents formats (LaTeX, HTML)
- Analyse de score ATS en temps réel
- Suggestions d'amélioration automatiques
- Support de plus de langues

---

**Note** : Ce projet utilise l'API OpenAI qui nécessite des crédits. Assurez-vous d'avoir un compte OpenAI actif avec des crédits disponibles.
