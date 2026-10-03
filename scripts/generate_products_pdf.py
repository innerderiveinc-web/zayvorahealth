import sys
import os
sys.path.insert(0, 'services/knowledge/app/data')
from products_master import MASTER_PRODUCTS

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#165B44"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(40, 810, "ZAYVORA Health OS™ — Official Clinical Formulary (32 Master Products)")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#5F707E"))
            self.drawRightString(555, 810, "Chief Clinician: Dr. Irfan Ashraf (BUMS, AMU)")
            self.setStrokeColor(colors.HexColor("#DCD5C4"))
            self.setLineWidth(0.6)
            self.line(40, 804, 555, 804)

        # Footer
        self.setStrokeColor(colors.HexColor("#DCD5C4"))
        self.setLineWidth(0.6)
        self.line(40, 42, 555, 42)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#5F707E"))
        self.drawString(40, 30, "CONFIDENTIAL & STATUTORY COMPLIANT • AYUSH GMP & 21 CFR PART 11")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(555, 30, page_text)
        self.restoreState()


def build_formulary_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#165B44")
    charcoal_dark = colors.HexColor("#1B242A")
    body_color = colors.HexColor("#2D3748")
    muted_color = colors.HexColor("#5F707E")
    gold_accent = colors.HexColor("#96601B")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=muted_color,
        spaceAfter=12
    )

    section_heading = ParagraphStyle(
        'SecHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.white,
        spaceAfter=0
    )

    prod_header_style = ParagraphStyle(
        'ProdHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=primary_color,
    )

    prod_sub_style = ParagraphStyle(
        'ProdSub',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=12,
        textColor=gold_accent,
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=charcoal_dark,
    )

    body_regular = ParagraphStyle(
        'BodyRegular',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=body_color,
    )

    table_header = ParagraphStyle(
        'TableHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=primary_color,
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=charcoal_dark,
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=charcoal_dark,
    )

    story = []

    # Cover Header Banner
    story.append(Paragraph("ZAYVORA Health OS™ — Clinical Formulary", title_style))
    story.append(Paragraph(
        "<b>32 Master Standardized Botanical & Classical Unani Formulations</b><br/>"
        "Official Ingredients, Therapeutic Dosages, High-Performance Analytical Markers & Clinical Indications<br/>"
        "<b>Chief Clinician & IP Steward:</b> Hakeem Dr. Irfan Ashraf (BUMS, AKTC AMU, 2002–2007; NCISM Reg: BUMS/AMU/2007)",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=0, spaceAfter=12))

    # Executive Summary Box
    exec_text = (
        "<b>Integrative Prescribing Architecture:</b> This compendium details the 32 proprietary and modernized "
        "master formulations developed under the ZAYVORA Clinical Framework. Within the ZAYVORA Health OS Clinical Cockpit, "
        "clinicians can co-prescribe these 32 GMP-certified botanical formulations alongside classical single drugs (Mufradat), "
        "traditional pharmacopoeial compounds (Qarabadeen like Majun, Khamira, Arq, and Sharbat), as well as extemporaneous "
        "bedside compounds (Self-Nuskha Track). Every formulation features quantitative active ingredient dosing and HPLC assay markers."
    )
    exec_table = Table([[Paragraph(exec_text, body_regular)]], colWidths=[520])
    exec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F4F0E6")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#DCD5C4")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(exec_table)
    story.append(Spacer(1, 14))

    # Group Products by Section
    sections = [
        ("SECTION A: CHRONIC DISEASE CLUSTER (NCDs)", ["ZAY-001", "ZAY-002", "ZAY-003", "ZAY-004", "ZAY-005", "ZAY-006", "ZAY-007", "ZAY-008"]),
        ("SECTION B: SPECIALTY & SYSTEMIC BRAND FORMULATIONS", ["ZAY-009", "ZAY-010", "ZAY-011", "ZAY-012", "ZAY-013", "ZAY-014", "ZAY-015", "ZAY-016", "ZAY-017", "ZAY-018", "ZAY-019", "ZAY-020", "ZAY-021", "ZAY-022"]),
        ("SECTION C: POSHIDA AMRAZ & CONTROLLED Rx SPECIALTIES", ["ZAY-023", "ZAY-024", "ZAY-025", "ZAY-026", "ZAY-027", "ZAY-028", "ZAY-029", "ZAY-030", "ZAY-031", "ZAY-032"]),
    ]

    for sec_title, sku_list in sections:
        # Section Header Banner
        sec_bar = Table([[Paragraph(f"<b>{sec_title}</b>", section_heading)]], colWidths=[520])
        sec_bar.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), primary_color),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(sec_bar)
        story.append(Spacer(1, 8))

        for sku in sku_list:
            p = MASTER_PRODUCTS.get(sku)
            if not p:
                continue

            card_elements = []

            # 1. Product Title Bar
            header_row = [
                Paragraph(f"<b>{p['sku']}: {p['name']}</b>", prod_header_style),
                Paragraph(f"<b>{p.get('unani_name', '')}</b>", prod_sub_style)
            ]
            t_head = Table([header_row], colWidths=[280, 240])
            t_head.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
            ]))
            card_elements.append(t_head)

            # 2. Key Metadata Pill Grid
            reg_badge = p.get('regulatory_track', '').replace('_', ' ')
            meta_data = [
                [
                    Paragraph(f"<b>Form:</b> {p.get('formulation_type', '')}", body_regular),
                    Paragraph(f"<b>Axis:</b> {p.get('organ_axis', '')}", body_regular),
                    Paragraph(f"<b>Track:</b> {reg_badge}", body_regular),
                    Paragraph(f"<b>Rx Required:</b> {'Yes' if p.get('is_prescription_required') else 'No'}", body_regular)
                ]
            ]
            t_meta = Table(meta_data, colWidths=[140, 130, 150, 100])
            t_meta.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FAF8F5")),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2D9CC")),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ]))
            card_elements.append(t_meta)
            card_elements.append(Spacer(1, 4))

            # 3. Indication & Posology
            ind_text = f"<b>Clinical Indications:</b> {p.get('primary_indication', '')}<br/><b>Standard Posology:</b> {p.get('dosage', '')}"
            card_elements.append(Paragraph(ind_text, body_regular))
            card_elements.append(Spacer(1, 4))

            # 4. Ingredients Table (Item, Latin/Common Name, Amount mg, Standardization)
            ing_rows = [
                [
                    Paragraph("<b>#</b>", table_header),
                    Paragraph("<b>Active Ingredient (Botanical Binomial / Unani)</b>", table_header),
                    Paragraph("<b>Amount / Dose</b>", table_header),
                    Paragraph("<b>Analytical Marker / Standardization</b>", table_header),
                ]
            ]
            for idx, ing in enumerate(p.get('composition', []), 1):
                amt_str = f"{ing.get('amount_mg')} mg" if ing.get('amount_mg') else "-"
                ing_rows.append([
                    Paragraph(str(idx), table_cell_bold),
                    Paragraph(ing.get('ingredient', ''), table_cell),
                    Paragraph(amt_str, table_cell_bold),
                    Paragraph(ing.get('standardization', '-'), table_cell),
                ])

            t_ing = Table(ing_rows, colWidths=[20, 240, 100, 160])
            t_ing.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E6F4EA")),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
                ('TOPPADDING', (0, 0), (-1, -1), 2.5),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#DCD5C4")),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            card_elements.append(t_ing)

            # 5. Contraindications & Safety
            if p.get('contraindications'):
                ci_str = " • ".join(p.get('contraindications', []))
                card_elements.append(Spacer(1, 3))
                card_elements.append(Paragraph(f"<b>Safety & Contraindications:</b> <font color='#A83232'>{ci_str}</font>", body_regular))

            card_elements.append(Spacer(1, 10))
            card_elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#DCD5C4"), spaceBefore=2, spaceAfter=8))

            story.append(KeepTogether(card_elements))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    out_path = "docs/ZAYVORA_32_Master_Products_Formulary.pdf"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    build_formulary_pdf(out_path)
