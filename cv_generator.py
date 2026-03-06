import re
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, ListFlowable
from reportlab.lib.units import inch
from reportlab.lib import colors


# =========================
# CONFIG
# =========================

HIGHLIGHT = False


# =========================
# COLORS
# =========================

TEXT_DARK = colors.HexColor("#111111")
TEXT_GRAY = colors.HexColor("#444444")
LINE_GRAY = colors.HexColor("#BBBBBB")
LINK_COLOR = colors.HexColor("#2F5FA7")
HIGHLIGHT_BG = "#FFF59D"
HIGHLIGHT_COLOR = "#000000"


# =========================
# HELPERS
# =========================

def safe(value):
    return value and str(value).strip() != ""


def link(url):
    return f'<link href="{url}" color="{LINK_COLOR}">{url}</link>'


def highlight_text(text, keywords):

    if not HIGHLIGHT or not text:
        return text or ""

    for word in keywords:
        pattern = re.compile(rf"\b({re.escape(word)})\b", re.IGNORECASE)

        text = pattern.sub(
            rf'<span backColor="{HIGHLIGHT_BG}"><b><font color="{HIGHLIGHT_COLOR}">\1</font></b></span>',
            text
        )

    return text


# =========================
# PDF BUILDER
# =========================

def build_cv_pdf(data, output_path="cv.pdf"):

    header = data.get("header", {})
    keywords = data.get("keywords", [])

    story = []

    # =========================
    # STYLES
    # =========================

    name_style = ParagraphStyle(
        "name",
        fontName="Times-Bold",
        fontSize=20,
        textColor=TEXT_DARK,
        spaceAfter=15,
        alignment=1
    )

    title_style = ParagraphStyle(
        "title",
        fontName="Times-Bold",
        fontSize=13,
        textColor=TEXT_GRAY,
        spaceAfter=12,
        alignment=1
    )

    contact_style = ParagraphStyle(
        "contact",
        fontName="Times-Roman",
        fontSize=10,
        leading=14,
        textColor=TEXT_GRAY
    )

    section_style = ParagraphStyle(
        "section",
        fontName="Times-Bold",
        fontSize=12,
        textColor=TEXT_DARK,
        spaceBefore=20,
        spaceAfter=6
    )

    job_title_style = ParagraphStyle(
        "job_title",
        fontName="Times-Bold",
        fontSize=11,
        textColor=TEXT_DARK
    )

    normal = ParagraphStyle(
        "normal",
        fontName="Times-Roman",
        fontSize=10,
        leading=14,
        textColor=TEXT_GRAY
    )

    # =========================
    # HEADER
    # =========================

    if safe(header.get("name")):
        story.append(Paragraph(header["name"], name_style))

    if safe(header.get("title")):
        story.append(Paragraph(header["title"], title_style))

    story.append(
        Table(
            [[""]],
            colWidths=[7.5 * inch],
            style=[("LINEBELOW",(0,0),(-1,-1),1,LINE_GRAY)]
        )
    )

    story.append(Spacer(1,10))

    contact_lines = []

    if safe(header.get("phone")):
        contact_lines.append(f"Phone: {header['phone']}")

    if safe(header.get("location")):
        contact_lines.append(header["location"])

    if safe(header.get("email")):
        contact_lines.append(
            f'Email: <link href="mailto:{header["email"]}" color="{LINK_COLOR}">{header["email"]}</link>'
        )

    if safe(header.get("linkedin")):
        contact_lines.append(f"LinkedIn: {link(header['linkedin'])}")

    if safe(header.get("portfolio")):
        contact_lines.append(f"Portfolio: {link(header['portfolio'])}")

    if safe(header.get("github")):
        contact_lines.append(f"GitHub: {link(header['github'])}")

    if header.get("languages"):
        contact_lines.append(f"Languages: {', '.join(header['languages'])}")

    if contact_lines:
        story.append(Paragraph("<br/>".join(contact_lines), contact_style))


    # =========================
    # SECTION HELPER
    # =========================

    def section(title):

        story.append(Spacer(1,16))
        story.append(Paragraph(title, section_style))

        story.append(
            Table(
                [[""]],
                colWidths=[7.5 * inch],
                style=[("LINEABOVE",(0,0),(-1,-1),1,LINE_GRAY)]
            )
        )

        story.append(Spacer(1,6))


    # =========================
    # WORK EXPERIENCE
    # =========================

    section("WORK EXPERIENCE")

    for job in data.get("work_experience", []):

        if not safe(job.get("title")):
            continue

        title = Paragraph(job["title"], job_title_style)
        date = Paragraph(job.get("date",""), normal)

        story.append(
            Table(
                [[title,date]],
                colWidths=[5.5 * inch,2 * inch],
                style=[("ALIGN",(1,0),(1,0),"RIGHT")]
            )
        )

        if safe(job.get("company")):

            company_text = job["company"]

            if safe(job.get("location")):
                company_text += f", {job['location']}"

            story.append(
                Paragraph(
                    f'<font color="#555555"><i>{company_text}</i></font>',
                    normal
                )
            )

        if safe(job.get("description")):
            story.append(
                Paragraph(
                    highlight_text(job["description"], keywords),
                    normal
                )
            )

        bullets = [
            Paragraph(highlight_text(x, keywords), normal)
            for x in job.get("bullets", [])
            if safe(x)
        ]

        if bullets:
            story.append(
                ListFlowable(
                    bullets,
                    bulletType="bullet",
                    bulletColor=TEXT_GRAY,
                    leftIndent=12
                )
            )

        story.append(Spacer(1,8))


    # =========================
    # EDUCATION
    # =========================

    section("EDUCATION")

    for edu in data.get("education", []):

        if not safe(edu.get("title")):
            continue

        text = f"<b>{edu.get('date','')}</b> — {highlight_text(edu['title'], keywords)}"

        if safe(edu.get("school")):

            text += f"<br/><font color='#555555'>{edu['school']}"

            if safe(edu.get("location")):
                text += f", {edu['location']}"

            text += "</font>"

        story.append(Paragraph(text, normal))
        story.append(Spacer(1,6))


    # =========================
    # SKILLS
    # =========================

    section("TECHNICAL SKILLS")

    skills = data.get("technical_skills", {})

    for category, values in skills.items():

        values = [highlight_text(v, keywords) for v in values if safe(v)]

        if not values:
            continue

        text = f"<b>{category.replace('_',' ').title()}:</b> {', '.join(values)}"

        story.append(Paragraph(text, normal))
        story.append(Spacer(1,4))


    # =========================
    # BUILD PDF
    # =========================

    doc = SimpleDocTemplate(
        output_path,
        pagesize=LETTER,
        leftMargin=30,
        rightMargin=30,
        topMargin=20,
        bottomMargin=20,
    )

    doc.build(story)

    return output_path