"""
Composants Streamlit personnalisés pour SEO
"""
import streamlit as st
import streamlit.components.v1 as components


def inject_meta_tags():
    """
    Injecter les meta tags SEO dans le head de la page Streamlit
    Utilise components.html pour injecter directement dans le DOM
    """
    meta_tags_html = """
    <script>
    (function() {
        // Créer ou mettre à jour la meta description
        let metaDesc = document.querySelector('meta[name="description"]');
        if (!metaDesc) {
            metaDesc = document.createElement('meta');
            metaDesc.setAttribute('name', 'description');
            document.head.appendChild(metaDesc);
        }
        metaDesc.setAttribute('content', 'Optimisez votre CV pour les systèmes ATS (Applicant Tracking Systems) avec l\'intelligence artificielle. Générez un CV professionnel optimisé et une lettre de motivation personnalisée en quelques minutes.');
        
        // Meta keywords
        let metaKeywords = document.querySelector('meta[name="keywords"]');
        if (!metaKeywords) {
            metaKeywords = document.createElement('meta');
            metaKeywords.setAttribute('name', 'keywords');
            document.head.appendChild(metaKeywords);
        }
        metaKeywords.setAttribute('content', 'CV optimisé, ATS, optimisation CV, CV professionnel, lettre de motivation, intelligence artificielle, GPT-4, recherche d\'emploi, CV français, CV anglais');
        
        // Meta author
        let metaAuthor = document.querySelector('meta[name="author"]');
        if (!metaAuthor) {
            metaAuthor = document.createElement('meta');
            metaAuthor.setAttribute('name', 'author');
            document.head.appendChild(metaAuthor);
        }
        metaAuthor.setAttribute('content', 'CodeCraftNest');
        
        // Open Graph tags
        const ogTags = [
            {property: 'og:title', content: 'CV Optimizer ATS - Optimisez Votre CV avec l\'IA'},
            {property: 'og:description', content: 'Optimisez votre CV pour les systèmes ATS avec l\'intelligence artificielle. Générez un CV professionnel optimisé.'},
            {property: 'og:url', content: 'https://cv-optimizer.codecraftnest.ca/app'},
            {property: 'og:type', content: 'website'},
            {property: 'og:image', content: 'https://cv-optimizer.codecraftnest.ca/static/og-image.jpg'}
        ];
        
        ogTags.forEach(tag => {
            let meta = document.querySelector(`meta[property="${tag.property}"]`);
            if (!meta) {
                meta = document.createElement('meta');
                meta.setAttribute('property', tag.property);
                document.head.appendChild(meta);
            }
            meta.setAttribute('content', tag.content);
        });
        
        // Twitter Card tags
        const twitterTags = [
            {property: 'twitter:card', content: 'summary_large_image'},
            {property: 'twitter:title', content: 'CV Optimizer ATS'},
            {property: 'twitter:description', content: 'Optimisez votre CV pour les systèmes ATS avec l\'IA'},
            {property: 'twitter:image', content: 'https://cv-optimizer.codecraftnest.ca/static/og-image.jpg'}
        ];
        
        twitterTags.forEach(tag => {
            let meta = document.querySelector(`meta[property="${tag.property}"]`);
            if (!meta) {
                meta = document.createElement('meta');
                meta.setAttribute('property', tag.property);
                document.head.appendChild(meta);
            }
            meta.setAttribute('content', tag.content);
        });
        
        // Canonical URL
        let canonical = document.querySelector('link[rel="canonical"]');
        if (!canonical) {
            canonical = document.createElement('link');
            canonical.setAttribute('rel', 'canonical');
            document.head.appendChild(canonical);
        }
        canonical.setAttribute('href', 'https://cv-optimizer.codecraftnest.ca/app');
    })();
    </script>
    """
    
    components.html(meta_tags_html, height=0)


def setup_seo():
    """
    Configuration SEO complète pour la page
    """
    # Injecter les meta tags via JavaScript
    inject_meta_tags()
    
    # Aussi utiliser st.markdown pour les meta tags de base
    st.markdown("""
    <meta name="description" content="Optimisez votre CV pour les systèmes ATS (Applicant Tracking Systems) avec l'intelligence artificielle. Générez un CV professionnel optimisé et une lettre de motivation personnalisée en quelques minutes.">
    <meta name="keywords" content="CV optimisé, ATS, optimisation CV, CV professionnel, lettre de motivation, intelligence artificielle, GPT-4, recherche d'emploi, CV français, CV anglais">
    <meta name="author" content="CodeCraftNest">
    <meta name="robots" content="index, follow">
    """, unsafe_allow_html=True)
