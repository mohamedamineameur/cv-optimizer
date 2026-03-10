"""
Interface Streamlit refactorisée
"""
import streamlit as st
from pathlib import Path
import sys

# Ajouter le chemin parent pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.config import settings
from app.models import ResumeModel
from app.services import CVExtractor, CVOptimizer, PDFService, OpenAIService
from app.utils import logger, CVParseError, OpenAIError, PDFGenerationError
from app.frontend.components import setup_seo


def main():
    """Point d'entrée principal de l'application"""
    
    # Configuration SEO et page
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
    
    # Configuration SEO complète (injection JavaScript + meta tags)
    setup_seo()
    
    # Styles pour performance
    st.markdown("""
    <style>
        /* Réduire CLS - afficher le contenu progressivement */
        [data-testid="stApp"] {
            min-height: 100vh;
        }
        /* Font display swap pour éviter FOIT */
        @font-face {
            font-display: swap;
        }
        /* Optimisation pour réduire les layout shifts */
        .stApp > header {
            visibility: visible;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Utiliser h1 pour le titre principal (SEO)
    st.markdown(f"# 📄 {settings.app_name}", unsafe_allow_html=True)
    st.caption(f"Version {settings.app_version}")
    
    # Sidebar pour les options
    with st.sidebar:
        st.header("⚙️ Options")
        language = st.selectbox(
            "CV language",
            ["EN", "FR"],
            label_visibility="visible",
            help="Select the language for your CV"
        )
        highlight_keywords = st.checkbox(
            "Highlight keywords in PDF",
            value=False,
            help="Highlight matching keywords in the generated PDF"
        )
        generate_cover_letter = st.checkbox(
            "Generate cover letter",
            value=False,
            help="Generate a personalized cover letter"
        )
        show_json = st.checkbox(
            "Show JSON",
            value=False,
            help="Display the generated JSON data"
        )
    
    # Formulaire principal
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📤 Upload CV")
        uploaded_cv = st.file_uploader(
            "Upload your CV",
            type=["pdf", "docx"],
            help="Supported formats: PDF, DOCX",
            label_visibility="visible",
            key="cv_uploader"
        )
    
    with col2:
        st.subheader("💼 Job Offer")
        job_offer = st.text_area(
            "Paste job offer",
            height=200,
            help="Copy and paste the complete job offer text",
            label_visibility="visible",
            key="job_offer_textarea",
            placeholder="Paste the complete job offer text here..."
        )
    
    # Section pour ajouter des expériences
    st.divider()
    st.subheader("➕ Add Work Experience (before optimization)")
    
    additional_experiences = st.session_state.get('additional_experiences', [])
    
    with st.expander("Add new work experience to include in CV", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            new_title = st.text_input(
                "Job Title",
                key="pre_exp_title",
                label_visibility="visible",
                help="Enter the job title"
            )
            new_company = st.text_input(
                "Company",
                key="pre_exp_company",
                label_visibility="visible",
                help="Enter the company name"
            )
            new_location = st.text_input(
                "Location",
                key="pre_exp_location",
                label_visibility="visible",
                help="Enter the job location"
            )
            new_date = st.text_input(
                "Date (e.g., Jan 2020 - Dec 2022)",
                key="pre_exp_date",
                label_visibility="visible",
                help="Enter the employment period"
            )
        
        with col2:
            new_description = st.text_area(
                "Description",
                height=100,
                key="pre_exp_desc",
                label_visibility="visible",
                help="Enter a brief description"
            )
            new_bullets_text = st.text_area(
                "Bullet points (one per line)",
                height=100,
                key="pre_exp_bullets",
                help="Enter one bullet point per line",
                label_visibility="visible"
            )
        
        if st.button("Add Experience", key="add_pre_exp", type="primary"):
            if new_title and new_company:
                new_experience = {
                    "title": new_title,
                    "company": new_company,
                    "location": new_location,
                    "date": new_date,
                    "description": new_description,
                    "bullets": [b.strip() for b in new_bullets_text.split("\n") if b.strip()],
                }
                
                if 'additional_experiences' not in st.session_state:
                    st.session_state['additional_experiences'] = []
                st.session_state['additional_experiences'].append(new_experience)
                st.success(f"Experience '{new_title}' at '{new_company}' added!")
                st.rerun()
            else:
                st.error("Please fill at least Title and Company")
    
    # Afficher les expériences ajoutées
    if additional_experiences:
        st.write(f"**{len(additional_experiences)} experience(s) added:**")
        for i, exp in enumerate(additional_experiences):
            with st.expander(f"{exp.get('title', 'N/A')} at {exp.get('company', 'N/A')} - {exp.get('date', '')}"):
                st.write(f"**Company:** {exp.get('company', '')}")
                st.write(f"**Location:** {exp.get('location', '')}")
                st.write(f"**Date:** {exp.get('date', '')}")
                st.write(f"**Description:** {exp.get('description', '')}")
                if exp.get('bullets'):
                    st.write("**Bullet points:**")
                    for bullet in exp.get('bullets', []):
                        st.write(f"- {bullet}")
                
                if st.button(f"Remove", key=f"remove_exp_{i}"):
                    st.session_state['additional_experiences'].pop(i)
                    st.rerun()
    
    st.divider()
    
    # Bouton d'optimisation avec aria-label pour accessibilité
    if st.button(
        "🚀 Optimize CV",
        type="primary",
        use_container_width=True,
        key="optimize_button",
        help="Click to optimize your CV with AI"
    ):
        # Validation
        if not uploaded_cv:
            st.error("❌ Please upload a CV file")
            st.stop()
        
        if not job_offer.strip():
            st.error("❌ Please paste the job offer")
            st.stop()
        
        try:
            # Extraction
            with st.spinner("📄 Parsing CV..."):
                extractor = CVExtractor()
                cv_text = extractor.extract(uploaded_cv, uploaded_cv.name)
            
            if not cv_text:
                st.error("❌ Could not extract text from CV")
                st.stop()
            
            st.success("✅ CV parsed successfully")
            
            # Optimisation
            with st.spinner("🤖 Optimizing CV with AI..."):
                optimizer = CVOptimizer()
                additional_exps = st.session_state.get('additional_experiences', [])
                resume_data = optimizer.optimize(
                    cv_text,
                    job_offer,
                    language,
                    additional_exps
                )
                
                st.session_state['cv_data'] = resume_data.model_dump()
                st.session_state['cv_language'] = language
                st.session_state['job_offer'] = job_offer
            
            st.success("✅ CV optimized successfully!")
            
        except CVParseError as e:
            st.error(f"❌ Error parsing CV: {e}")
            logger.error(f"CVParseError: {e}")
        except OpenAIError as e:
            st.error(f"❌ Error with AI optimization: {e}")
            logger.error(f"OpenAIError: {e}")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
            logger.error(f"Unexpected error: {e}", exc_info=True)
    
    # Affichage des résultats
    if 'cv_data' in st.session_state:
        resume_data = st.session_state['cv_data']
        
        if show_json:
            st.divider()
            st.subheader("📋 Generated JSON")
            st.json(resume_data)
        
        # Génération PDF
        st.divider()
        st.subheader("📄 Generate PDF")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Generate CV PDF", type="primary", use_container_width=True):
                try:
                    with st.spinner("Generating CV PDF..."):
                        pdf_service = PDFService()
                        cv_language = st.session_state.get('cv_language', 'EN')
                        pdf_path = pdf_service.generate_cv_pdf(
                            resume_data,
                            language=cv_language,
                            highlight=highlight_keywords
                        )
                    
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download optimized CV",
                            data=f.read(),
                            file_name="optimized_cv.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    
                    st.success("✅ CV PDF generated!")
                    
                except PDFGenerationError as e:
                    st.error(f"❌ Error generating PDF: {e}")
                    logger.error(f"PDFGenerationError: {e}")
        
        with col2:
            if generate_cover_letter:
                if st.button("📝 Generate Cover Letter", type="primary", use_container_width=True):
                    try:
                        with st.spinner("Generating cover letter..."):
                            openai_service = OpenAIService()
                            cv_language = st.session_state.get('cv_language', 'EN')
                            job_offer_text = st.session_state.get('job_offer', job_offer)
                            
                            cover_letter_text = openai_service.generate_cover_letter(
                                resume_data,
                                job_offer_text,
                                cv_language
                            )
                            
                            pdf_service = PDFService()
                            cover_letter_path = pdf_service.generate_cover_letter_pdf(
                                cover_letter_text,
                                resume_data.get("header", {}),
                                language=cv_language
                            )
                        
                        with open(cover_letter_path, "rb") as f:
                            st.download_button(
                                label="⬇️ Download cover letter",
                                data=f.read(),
                                file_name="cover_letter.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        
                        st.success("✅ Cover letter generated!")
                        
                    except OpenAIError as e:
                        st.error(f"❌ Error generating cover letter: {e}")
                        logger.error(f"OpenAIError: {e}")
                    except PDFGenerationError as e:
                        st.error(f"❌ Error generating PDF: {e}")
                        logger.error(f"PDFGenerationError: {e}")


if __name__ == "__main__":
    main()
