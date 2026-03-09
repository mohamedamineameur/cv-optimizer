from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.units import inch
from reportlab.lib import colors


# =========================
# COLORS
# =========================

TEXT_DARK = colors.HexColor("#111111")
TEXT_GRAY = colors.HexColor("#444444")
LINE_GRAY = colors.HexColor("#BBBBBB")


# =========================
# COVER LETTER PDF BUILDER
# =========================

def build_cover_letter_pdf(
    cover_letter_text: str,
    header: dict,
    language: str = "EN",
    output_path: str = "cover_letter.pdf"
):
    """
    Génère un PDF professionnel pour la lettre de motivation.
    """
    
    # Traductions selon la langue
    translations = {
        "EN": {
            "subject": "Subject: Application for",
            "dear": "Dear Hiring Manager,",
            "sincerely": "Sincerely,",
        },
        "FR": {
            "subject": "Objet : Candidature pour",
            "dear": "Madame, Monsieur,",
            "sincerely": "Cordialement,",
        }
    }
    
    texts = translations.get(language, translations["EN"])
    
    story = []
    
    # =========================
    # STYLES
    # =========================
    
    name_style = ParagraphStyle(
        "name",
        fontName="Times-Bold",
        fontSize=12,
        textColor=TEXT_DARK,
        spaceAfter=8,
        alignment=2  # Right align
    )
    
    contact_style = ParagraphStyle(
        "contact",
        fontName="Times-Roman",
        fontSize=9,
        leading=12,
        textColor=TEXT_GRAY,
        alignment=2  # Right align
    )
    
    date_style = ParagraphStyle(
        "date",
        fontName="Times-Roman",
        fontSize=10,
        textColor=TEXT_GRAY,
        spaceAfter=12,
        alignment=2  # Right align
    )
    
    subject_style = ParagraphStyle(
        "subject",
        fontName="Times-Bold",
        fontSize=11,
        textColor=TEXT_DARK,
        spaceAfter=16
    )
    
    greeting_style = ParagraphStyle(
        "greeting",
        fontName="Times-Roman",
        fontSize=10,
        textColor=TEXT_DARK,
        spaceAfter=12
    )
    
    body_style = ParagraphStyle(
        "body",
        fontName="Times-Roman",
        fontSize=10,
        leading=14,
        textColor=TEXT_DARK,
        spaceAfter=12,
        alignment=4  # Justify
    )
    
    closing_style = ParagraphStyle(
        "closing",
        fontName="Times-Roman",
        fontSize=10,
        textColor=TEXT_DARK,
        spaceAfter=8
    )
    
    signature_style = ParagraphStyle(
        "signature",
        fontName="Times-Roman",
        fontSize=10,
        textColor=TEXT_DARK,
        spaceAfter=4
    )
    
    # =========================
    # HEADER (Right aligned)
    # =========================
    
    name = header.get("name", "")
    if name:
        story.append(Paragraph(name, name_style))
    
    contact_lines = []
    if header.get("phone"):
        contact_lines.append(header["phone"])
    if header.get("email"):
        contact_lines.append(header["email"])
    if header.get("location"):
        contact_lines.append(header["location"])
    if header.get("linkedin"):
        contact_lines.append(header["linkedin"])
    
    if contact_lines:
        story.append(Paragraph("<br/>".join(contact_lines), contact_style))
    
    story.append(Spacer(1, 20))
    
    # Date (right aligned)
    from datetime import datetime
    date_text = datetime.now().strftime("%B %d, %Y") if language == "EN" else datetime.now().strftime("%d %B %Y")
    story.append(Paragraph(date_text, date_style))
    
    story.append(Spacer(1, 16))
    
    # =========================
    # SUBJECT LINE
    # =========================
    
    job_title = header.get("title", "")
    if job_title:
        subject_text = f"{texts['subject']} {job_title}"
        story.append(Paragraph(subject_text, subject_style))
    
    story.append(Spacer(1, 12))
    
    # =========================
    # GREETING
    # =========================
    
    story.append(Paragraph(texts["dear"], greeting_style))
    
    story.append(Spacer(1, 8))
    
    # =========================
    # BODY (Cover letter content)
    # =========================
    
    # Diviser le texte en paragraphes
    paragraphs = cover_letter_text.split("\n\n")
    
    for para in paragraphs:
        para = para.strip()
        if para:
            # Remplacer les retours à la ligne simples par des espaces
            para = para.replace("\n", " ")
            story.append(Paragraph(para, body_style))
            story.append(Spacer(1, 8))
    
    story.append(Spacer(1, 16))
    
    # =========================
    # CLOSING
    # =========================
    
    story.append(Paragraph(texts["sincerely"], closing_style))
    story.append(Spacer(1, 24))
    
    if name:
        story.append(Paragraph(name, signature_style))
    
    # =========================
    # BUILD PDF
    # =========================
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=LETTER,
        leftMargin=72,
        rightMargin=72,
        topMargin=72,
        bottomMargin=72,
    )
    
    doc.build(story)
    
    return output_path
