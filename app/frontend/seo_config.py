"""
Configuration SEO pour Streamlit
"""
import streamlit as st


def set_seo_meta_tags():
    """
    Configure les meta tags SEO pour Streamlit
    Note: Streamlit a des limitations pour les meta tags,
    mais on peut utiliser st.set_page_config et des composants HTML
    """
    st.set_page_config(
        page_title="CV Optimizer ATS - Optimisez Votre CV pour les Systèmes ATS avec l'IA",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://codecraftnest.ca',
            'Report a bug': None,
            'About': "CV Optimizer ATS - Optimisez votre CV avec l'intelligence artificielle"
        }
    )
    
    # Ajouter des meta tags via HTML
    st.markdown("""
    <head>
        <meta name="description" content="Optimisez votre CV pour les systèmes ATS (Applicant Tracking Systems) avec l'intelligence artificielle. Générez un CV professionnel optimisé et une lettre de motivation personnalisée.">
        <meta name="keywords" content="CV optimisé, ATS, optimisation CV, CV professionnel, lettre de motivation, intelligence artificielle, GPT-4, recherche d'emploi">
        <meta name="author" content="CodeCraftNest">
        <meta property="og:title" content="CV Optimizer ATS - Optimisez Votre CV avec l'IA">
        <meta property="og:description" content="Optimisez votre CV pour les systèmes ATS avec l'intelligence artificielle.">
        <meta property="og:url" content="https://cv-optimizer.codecraftnest.ca">
        <meta property="og:type" content="website">
        <link rel="canonical" href="https://cv-optimizer.codecraftnest.ca/app">
    </head>
    """, unsafe_allow_html=True)
