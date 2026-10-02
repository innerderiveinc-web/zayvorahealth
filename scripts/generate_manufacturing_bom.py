#!/usr/bin/env python3
"""
ZAYVORA Health OS™ - Master Pharmaceutical Manufacturing Specifications & BOM Generator
Generates:
1. docs/ZAYVORA_Master_Product_Manufacturing_BOM.pdf (High-grade standalone PDF)
2. docs/ZAYVORA_Master_Product_Manufacturing_BOM.html (High-DPI responsive & print-ready HTML)
"""

import os
import sys
import json
import re

# Ensure workspace root is in sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.knowledge.app.data.products_master import MASTER_PRODUCTS
from services.knowledge.app.data.kits_master import MASTER_KITS

# 10 Retail Products
RETAIL_PRODUCTS = [
    {
        "id": "ZAY-RET-01",
        "name": "ManiVital Pro™",
        "category": "Fertility & Vitality",
        "dosage_form": "Safoof / Granules (150g Jar)",
        "mrp": 1450,
        "dosage": "5g twice daily with lukewarm milk",
        "indications": "Male reproductive vitality, seminal viscosity, oligospermia, fatigue.",
        "key_ingredients": "Withania somnifera (Ashwagandha 5%), Mucuna pruriens (Kaunch 10% L-DOPA), Safed Musli, Salep, Kushta Qalai."
    },
    {
        "id": "ZAY-RET-02",
        "name": "OvaSync™",
        "category": "Women's Health",
        "dosage_form": "Granules (150g Jar)",
        "mrp": 1380,
        "dosage": "5g twice daily with milk / water",
        "indications": "Ovarian reserve support, follicular rhythm balancer, PCOS/PCOD, luteal phase support.",
        "key_ingredients": "Asparagus racemosus (Shatavari 10%), Saraca asoca (Ashoka Chhal), Symplocos racemosa (Lodhra), Aloe vera."
    },
    {
        "id": "ZAY-RET-03",
        "name": "Qurs-e-Taqwiyat-e-Mani™",
        "category": "Fertility & Vitality",
        "dosage_form": "Tablets (60 Tablets bottle)",
        "mrp": 890,
        "dosage": "2 tablets twice daily after meals",
        "indications": "Classical seminal viscosity, reproductive tone, nocturnal emissions, asthenospermia.",
        "key_ingredients": "Salep Orchis, Zafran (Saffron), Kushta Baiza-e-Murgh, Amber compound, Gond Kikar."
    },
    {
        "id": "ZAY-RET-04",
        "name": "MetaboCore Elite™",
        "category": "Metabolic Health",
        "dosage_form": "Veg Capsules (60 Caps)",
        "mrp": 1250,
        "dosage": "1 capsule 20 mins before main meals",
        "indications": "Metabolic syndrome, insulin resistance, HbA1c moderation, atherogenic lipid control.",
        "key_ingredients": "Gymnema sylvestre (25% Gymnemic Acids), Berberis aristata (Daruhald 95% Berberine), Momordica charantia, Fenugreek."
    },
    {
        "id": "ZAY-RET-05",
        "name": "ThyroMet Axis™",
        "category": "Endocrine & Thyroid",
        "dosage_form": "Tablets (60 Tablets bottle)",
        "mrp": 1320,
        "dosage": "1 tablet morning and evening",
        "indications": "Subclinical hypothyroidism, sluggish metabolic rate, cold sensitivity, water retention.",
        "key_ingredients": "Commiphora mukul (Purified Guggulu - Guggulsterones 2.5%), Bauhinia variegata (Kanchnar), Piper longum (Trikatu)."
    },
    {
        "id": "ZAY-RET-06",
        "name": "LiverPrime Core™",
        "category": "Hepato-Biliary",
        "dosage_form": "Herbal Decoction Syrup (200ml Bottle)",
        "mrp": 1150,
        "dosage": "10ml twice daily before meals",
        "indications": "Non-alcoholic fatty liver (NAFLD), sluggish biliary flow, hepatomegaly, toxic burden.",
        "key_ingredients": "Picrorhiza kurroa (Kutki 5% Kutkin), Cichorium intybus (Kasni), Andrographis paniculata (Kalmegh 10% Andrographolide), Bhumyamalaki."
    },
    {
        "id": "ZAY-RET-07",
        "name": "NeuroCalmX™",
        "category": "Neuropsychiatric",
        "dosage_form": "Granules / Majoon (125g Jar)",
        "mrp": 1200,
        "dosage": "5g at bedtime with warm milk",
        "indications": "GABAergic calm, mental resilience, generalized tension, insomnia, mental fatigue.",
        "key_ingredients": "Bacopa monnieri (Brahmi 20% Bacosides), Convolvulus pluricaulis (Shankhpushpi), Lavandula stoechas (Ustukhuddus), Melissa officinalis."
    },
    {
        "id": "ZAY-RET-08",
        "name": "NightOne X™",
        "category": "Sleep Medicine",
        "dosage_form": "Veg Capsules (30 Caps)",
        "mrp": 1320,
        "dosage": "1 capsule 30 minutes before sleep",
        "indications": "Circadian rhythm disruption, fragmented sleep, non-REM deficiency, jet lag recovery.",
        "key_ingredients": "Valeriana wallichii (Tagar 0.8% Valerenic acid), Nardostachys jatamansi (Jatamansi), Withania somnifera, Lactuca sativa."
    },
    {
        "id": "ZAY-RET-09",
        "name": "Sleep Stress Harmonizer™",
        "category": "Sleep & Adrenal",
        "dosage_form": "Infusion Tisane / Powder (100g Pouch)",
        "mrp": 1180,
        "dosage": "1 teaspoon steeped in warm water 45 mins before bed",
        "indications": "Nocturnal cortisol surges, 3 AM wakefulness, hyperarousal, restless leg tension.",
        "key_ingredients": "Matricaria chamomilla, Ocimum sanctum (Tulsi), Rosa damascena (Gul-e-Surkh), Coriandrum sativum, Cardamom."
    },
    {
        "id": "ZAY-RET-10",
        "name": "Men Daily Vitality™",
        "category": "Daily Micronutrient & Tonic",
        "dosage_form": "Multi-Herb Tablets (60 Tablets)",
        "mrp": 950,
        "dosage": "1 tablet daily after breakfast",
        "indications": "General debility, micronutrient replenishment, physical stamina, daily cellular antioxidant defence.",
        "key_ingredients": "Emblica officinalis (Amla standardized Vitamin C), Tribulus terrestris (Gokshura 40%), Panax ginseng, Shilajit purified (Fulvic Acid 50%)."
    }
]

# Simple PDF Engine Implementation (Standard PDF 1.4 specification)
class PDFWriter:
    def __init__(self, page_width=595.28, page_height=841.89):
        self.width = page_width
        self.height = page_height
        self.pages = []  # list of command strings
        self.current_stream = []
        self.current_y = 800
        self.margin_x = 40
        self.usable_width = self.width - (2 * self.margin_x)
        self.page_num = 0

    def start_page(self):
        if self.current_stream:
            self._finalize_page()
        self.page_num += 1
        self.current_stream = []
        self.current_y = 790
        
        # Add Running Header
        self.draw_rect(self.margin_x, 805, self.usable_width, 1.0, fill_color=(0.18, 0.42, 0.31))
        self.add_text("ZAYVORA HEALTH OS™ — PHARMACEUTICAL MANUFACTURING SPECIFICATIONS & BOM", 
                      self.margin_x, 812, font_size=8, font="F2", color=(0.18, 0.42, 0.31))
        self.add_text("STRICTLY CONFIDENTIAL — AYUSH GMP & ISO 9001:2015", 
                      self.width - self.margin_x - 215, 812, font_size=7.5, font="F1", color=(0.4, 0.4, 0.4))
        
        # Add Running Footer
        self.draw_rect(self.margin_x, 35, self.usable_width, 0.8, fill_color=(0.7, 0.7, 0.7))
        self.add_text(f"Document ID: ZAY-MFG-BOM-2026-V5 | Rev 5.0 | Page {self.page_num}", 
                      self.margin_x, 24, font_size=8, font="F1", color=(0.4, 0.4, 0.4))
        self.add_text("Valid for Commercial Batch Production & QA Release Verification", 
                      self.width - self.margin_x - 225, 24, font_size=8, font="F1", color=(0.4, 0.4, 0.4))

    def _finalize_page(self):
        page_content = "\n".join(self.current_stream)
        self.pages.append(page_content)
        self.current_stream = []

    def check_space(self, needed_pt):
        if self.current_y - needed_pt < 55:
            self.start_page()

    def escape_text(self, text):
        if text is None:
            return ""
        s = str(text)
        s = s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        # Filter to latin-1 safe chars
        clean = []
        for c in s:
            code = ord(c)
            if code < 128:
                clean.append(c)
            elif code in (8211, 8212): # em-dash, en-dash
                clean.append("-")
            elif code in (8216, 8217): # curly quotes
                clean.append("'")
            elif code in (8220, 8221): # curly double quotes
                clean.append('"')
            elif code == 8482: # trademark TM
                clean.append("(TM)")
            elif code == 174: # registered
                clean.append("(R)")
            elif code < 256:
                clean.append(c)
            else:
                clean.append("?")
        return "".join(clean)

    def add_text(self, text, x, y, font_size=10, font="F1", color=(0, 0, 0)):
        escaped = self.escape_text(text)
        r, g, b = color
        self.current_stream.append(
            f"BT\n/{font} {font_size} Tf\n{r:.3f} {g:.3f} {b:.3f} rg\n{x:.2f} {y:.2f} Td\n({escaped}) Tj\nET"
        )

    def draw_rect(self, x, y, w, h, fill_color=None, stroke_color=None, line_width=1.0):
        cmds = []
        if line_width != 1.0:
            cmds.append(f"{line_width:.2f} w")
        if fill_color:
            r, g, b = fill_color
            cmds.append(f"{r:.3f} {g:.3f} {b:.3f} rg")
        if stroke_color:
            r, g, b = stroke_color
            cmds.append(f"{r:.3f} {g:.3f} {b:.3f} RG")
        
        cmds.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re")
        if fill_color and stroke_color:
            cmds.append("B")
        elif fill_color:
            cmds.append("f")
        elif stroke_color:
            cmds.append("S")
        self.current_stream.append("\n".join(cmds))

    def compile(self):
        if self.current_stream:
            self._finalize_page()
            
        num_pages = len(self.pages)
        page_obj_ids = [6 + i * 2 for i in range(num_pages)]
        content_obj_ids = [7 + i * 2 for i in range(num_pages)]

        catalog = "1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        pages_kids = " ".join(f"{pid} 0 R" for pid in page_obj_ids)
        pages = f"2 0 obj\n<< /Type /Pages /Kids [{pages_kids}] /Count {num_pages} >>\nendobj\n"
        f1 = "3 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
        f2 = "4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n"
        f3 = "5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique >>\nendobj\n"

        body_parts = [catalog, pages, f1, f2, f3]

        for i in range(num_pages):
            pid = page_obj_ids[i]
            cid = content_obj_ids[i]
            stream_data = self.pages[i].encode("latin1")
            stream_len = len(stream_data)

            page_str = (
                f"{pid} 0 obj\n"
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.width:.2f} {self.height:.2f}] "
                f"/Contents {cid} 0 R "
                f"/Resources << /Font << /F1 3 0 R /F2 4 0 R /F3 5 0 R >> >> >>\n"
                f"endobj\n"
            )
            content_str = (
                f"{cid} 0 obj\n"
                f"<< /Length {stream_len} >>\n"
                f"stream\n"
            ).encode("latin1") + stream_data + b"\nendstream\nendobj\n"

            body_parts.append(page_str)
            body_parts.append(content_str)

        header = "%PDF-1.4\n".encode("latin1")
        offsets = [0]
        curr_offset = len(header)

        byte_chunks = []
        for part in body_parts:
            b = part if isinstance(part, bytes) else part.encode("latin1")
            offsets.append(curr_offset)
            curr_offset += len(b)
            byte_chunks.append(b)

        total_objs = len(body_parts) + 1
        xref = [f"xref\n0 {total_objs}\n0000000000 65535 f \n"]
        for off in offsets[1:]:
            xref.append(f"{off:010d} 00000 n \n")
        xref_str = "".join(xref).encode("latin1")

        trailer = (
            f"trailer\n<< /Size {total_objs} /Root 1 0 R >>\n"
            f"startxref\n{curr_offset}\n%%EOF\n"
        ).encode("latin1")

        return header + b"".join(byte_chunks) + xref_str + trailer


def build_pdf_dossier():
    pdf = PDFWriter()

    # ================= PAGE 1: TITLE & COVER =================
    pdf.start_page()
    
    # Top Decorative Banner
    pdf.draw_rect(pdf.margin_x, 700, pdf.usable_width, 85, fill_color=(0.11, 0.26, 0.20))
    pdf.add_text("ZAYVORA HEALTH OS™", pdf.margin_x + 15, 755, font_size=20, font="F2", color=(1.0, 1.0, 1.0))
    pdf.add_text("CENTRAL PHARMACEUTICAL MANUFACTURING DOSSIER", pdf.margin_x + 15, 735, font_size=12, font="F2", color=(0.95, 0.77, 0.40))
    pdf.add_text("Master Bill of Materials (BOM), Formulations & Quality Control Standard Operating Procedures", 
                 pdf.margin_x + 15, 715, font_size=9, font="F1", color=(0.85, 0.90, 0.88))
    
    pdf.current_y = 675
    
    # Metadata Box
    pdf.draw_rect(pdf.margin_x, pdf.current_y - 85, pdf.usable_width, 85, fill_color=(0.97, 0.98, 0.97), stroke_color=(0.80, 0.85, 0.82))
    pdf.add_text("DOCUMENT METADATA & COMPLIANCE SIGN-OFF", pdf.margin_x + 10, pdf.current_y - 18, font_size=10, font="F2", color=(0.11, 0.26, 0.20))
    
    meta_items = [
        ("Document Ref:", "ZAY-MFG-BOM-2026-V5", "Classification:", "Proprietary Commercial Formulation"),
        ("Regulatory Track:", "AYUSH Schedule T (GMP) / FSSAI 2022", "Batch Production:", "Commercial Pilot & Scale-Up Ready"),
        ("Clinical Author:", "Dr. Irfan Ashraf / Clinical Knowledge Desk", "Effective Date:", "September 2026 | Version 5.0 Enterprise"),
        ("Testing Authority:", "HPLC Active Marker Assays (USP/UPI)", "Pharmacopoeia:", "Unani Pharmacopoeia of India (UPI Vol 1-6)")
    ]
    
    y_meta = pdf.current_y - 34
    for col1_l, col1_v, col2_l, col2_v in meta_items:
        pdf.add_text(col1_l, pdf.margin_x + 10, y_meta, font_size=8, font="F2", color=(0.3, 0.3, 0.3))
        pdf.add_text(col1_v, pdf.margin_x + 95, y_meta, font_size=8, font="F1", color=(0.1, 0.1, 0.1))
        pdf.add_text(col2_l, pdf.margin_x + 270, y_meta, font_size=8, font="F2", color=(0.3, 0.3, 0.3))
        pdf.add_text(col2_v, pdf.margin_x + 360, y_meta, font_size=8, font="F1", color=(0.1, 0.1, 0.1))
        y_meta -= 12

    pdf.current_y -= 105

    # Executive Overview
    pdf.add_text("1. EXECUTIVE SUMMARY & MANUFACTURING DIRECTIVE", pdf.margin_x, pdf.current_y, font_size=11, font="F2", color=(0.18, 0.42, 0.31))
    pdf.draw_rect(pdf.margin_x, pdf.current_y - 4, pdf.usable_width, 1.0, fill_color=(0.18, 0.42, 0.31))
    pdf.current_y -= 18

    exec_lines = [
        "This master engineering document provides the exact pharmaceutical Bill of Materials (BOM), HPLC phytochemical",
        "standardizations, organ-axis classifications, and Schedule E(1) detoxification (Mudabbar) protocols for commercial",
        "batch production within the ZAYVORA Health OS manufacturing continuum. All formulations are verified against",
        "the Unani Pharmacopoeia of India (UPI), Ayurvedic Pharmacopoeia of India (API), and AYUSH GMP norms.",
        "",
        "Key Manufacturing Directives:",
        "1. Standardization Thresholds: All botanical extracts must meet HPLC assayed active marker concentrations (e.g., Withanolides 5%,",
        "   Gymnemic acids 25%, AKBA 30%, Reserpine 1.0%). Crude unstandardized powders are rejected at QA quarantine.",
        "2. Schedule E(1) Gates: Ingredients such as Kuchla (Strychnos nux-vomica) and Suranjan (Colchicum autumnale) require authenticated",
        "   SOP Mudabbar certificates prior to release from Raw Material Stores.",
        "3. Kushta / Calcined Mineral Processing: Products containing Kushta (Tin calx, Egg Shell calx, Coral calx) are manufactured in dedicated",
        "   micro-pulverization clean rooms under AYUSH Proprietary licensing."
    ]
    for line in exec_lines:
        if line.startswith("Key") or line.startswith("1. S") or line.startswith("2. S") or line.startswith("3. K"):
            pdf.add_text(line, pdf.margin_x, pdf.current_y, font_size=8.5, font="F2", color=(0.15, 0.15, 0.15))
        else:
            pdf.add_text(line, pdf.margin_x, pdf.current_y, font_size=8.5, font="F1", color=(0.25, 0.25, 0.25))
        pdf.current_y -= 12

    pdf.current_y -= 10
    
    # Portfolio Structure Table
    pdf.add_text("2. PRODUCT PORTFOLIO STRUCTURE SUMMARY", pdf.margin_x, pdf.current_y, font_size=11, font="F2", color=(0.18, 0.42, 0.31))
    pdf.draw_rect(pdf.margin_x, pdf.current_y - 4, pdf.usable_width, 1.0, fill_color=(0.18, 0.42, 0.31))
    pdf.current_y -= 22

    # Portfolio table header
    pdf.draw_rect(pdf.margin_x, pdf.current_y - 14, pdf.usable_width, 16, fill_color=(0.18, 0.42, 0.31))
    pdf.add_text("CATALOG TIER", pdf.margin_x + 8, pdf.current_y - 10, font_size=8, font="F2", color=(1, 1, 1))
    pdf.add_text("UNITS", pdf.margin_x + 130, pdf.current_y - 10, font_size=8, font="F2", color=(1, 1, 1))
    pdf.add_text("ORGAN AXES / SCOPE", pdf.margin_x + 180, pdf.current_y - 10, font_size=8, font="F2", color=(1, 1, 1))
    pdf.add_text("REGULATORY JURISDICTION", pdf.margin_x + 360, pdf.current_y - 10, font_size=8, font="F2", color=(1, 1, 1))
    pdf.current_y -= 14

    port_rows = [
        ("Master Clinical Formulations", "32 SKUs", "15 Organ Axes (Cardiac, Neuro, Endo, etc.)", "AYUSH Classical / AYUSH Proprietary"),
        ("Clinical Protocol Kits", "21 Kits", "Multi-Product Synergistic Regimens (K-01 to K-21)", "Prescription OPD Treatment Packs"),
        ("Retail Storefront Products", "10 Products", "Direct Consumer Wellness & Adaptogens", "OTC Nutraceutical / Classical"),
    ]
    for tier, count, scope, reg in port_rows:
        pdf.draw_rect(pdf.margin_x, pdf.current_y - 14, pdf.usable_width, 16, fill_color=(0.95, 0.96, 0.95), stroke_color=(0.85, 0.88, 0.86))
        pdf.add_text(tier, pdf.margin_x + 8, pdf.current_y - 10, font_size=8, font="F2", color=(0.1, 0.1, 0.1))
        pdf.add_text(count, pdf.margin_x + 130, pdf.current_y - 10, font_size=8, font="F1", color=(0.1, 0.1, 0.1))
        pdf.add_text(scope, pdf.margin_x + 180, pdf.current_y - 10, font_size=8, font="F1", color=(0.1, 0.1, 0.1))
        pdf.add_text(reg, pdf.margin_x + 360, pdf.current_y - 10, font_size=8, font="F1", color=(0.1, 0.1, 0.1))
        pdf.current_y -= 16

    # ================= MASTER CLINICAL PRODUCTS (ZAY-001 to ZAY-032) =================
    pdf.start_page()
    pdf.add_text("3. MASTER CLINICAL PRODUCTS: COMPLETE BILL OF MATERIALS (BOM)", pdf.margin_x, pdf.current_y, font_size=12, font="F2", color=(0.11, 0.26, 0.20))
    pdf.draw_rect(pdf.margin_x, pdf.current_y - 4, pdf.usable_width, 1.2, fill_color=(0.11, 0.26, 0.20))
    pdf.current_y -= 16

    # Sort products by SKU
    skus = sorted(MASTER_PRODUCTS.keys(), key=lambda s: int(s.split("-")[-1]))
    
    for sku in skus:
        p = MASTER_PRODUCTS[sku]
        comp = p.get("composition", [])
        num_ingredients = len(comp)
        
        # Estimate height needed for this product block
        # Header (22) + Meta Grid (30) + Table Header (14) + Rows (14 * num_ingredients) + Footer (16) + Spacing (15)
        needed_height = 22 + 30 + 14 + (num_ingredients * 14) + 16 + 18
        pdf.check_space(needed_height)

        # Product Header Banner
        is_rx = p.get("is_prescription_required", False)
        rx_label = "PRESCRIPTION ONLY (SCHEDULE E-1 / POTENT)" if is_rx else "AYUSH OTC / DISPENSARY"
        rx_color = (0.75, 0.15, 0.15) if is_rx else (0.18, 0.42, 0.31)
        
        pdf.draw_rect(pdf.margin_x, pdf.current_y - 18, pdf.usable_width, 20, fill_color=(0.90, 0.94, 0.92), stroke_color=(0.70, 0.80, 0.75))
        pdf.add_text(f"{sku}: {p.get('name', '')}", pdf.margin_x + 8, pdf.current_y - 13, font_size=10.5, font="F2", color=(0.11, 0.26, 0.20))
        pdf.add_text(f"Classical: {p.get('unani_name', '')}", pdf.margin_x + 190, pdf.current_y - 13, font_size=9, font="F3", color=(0.25, 0.25, 0.25))
        pdf.add_text(rx_label, pdf.width - pdf.margin_x - 170, pdf.current_y - 13, font_size=7.5, font="F2", color=rx_color)
        pdf.current_y -= 22

        # Technical Metadata Sub-Box
        pdf.draw_rect(pdf.margin_x, pdf.current_y - 24, pdf.usable_width, 24, fill_color=(0.98, 0.98, 0.98), stroke_color=(0.88, 0.88, 0.88))
        pdf.add_text(f"Organ Axis: {p.get('organ_axis', '')}", pdf.margin_x + 6, pdf.current_y - 10, font_size=7.5, font="F2", color=(0.3, 0.3, 0.3))
        pdf.add_text(f"Dosage Form: {p.get('formulation_type', '')}", pdf.margin_x + 130, pdf.current_y - 10, font_size=7.5, font="F1", color=(0.2, 0.2, 0.2))
        pdf.add_text(f"Regulatory: {p.get('regulatory_track', '')}", pdf.margin_x + 250, pdf.current_y - 10, font_size=7.5, font="F1", color=(0.2, 0.2, 0.2))
        pdf.add_text(f"MRP: INR {p.get('mrp_inr', 0)}", pdf.width - pdf.margin_x - 70, pdf.current_y - 10, font_size=7.5, font="F2", color=(0.11, 0.26, 0.20))
        
        pdf.add_text(f"Indication: {p.get('primary_indication', '')[:100]}...", pdf.margin_x + 6, pdf.current_y - 20, font_size=7, font="F3", color=(0.4, 0.4, 0.4))
        pdf.current_y -= 28

        # Ingredients Table Header
        pdf.draw_rect(pdf.margin_x, pdf.current_y - 13, pdf.usable_width, 14, fill_color=(0.18, 0.42, 0.31))
        pdf.add_text("#", pdf.margin_x + 6, pdf.current_y - 10, font_size=7.5, font="F2", color=(1, 1, 1))
        pdf.add_text("BOTANICAL / CLASSICAL INGREDIENT", pdf.margin_x + 24, pdf.current_y - 10, font_size=7.5, font="F2", color=(1, 1, 1))
        pdf.add_text("AMOUNT (MG)", pdf.margin_x + 245, pdf.current_y - 10, font_size=7.5, font="F2", color=(1, 1, 1))
        pdf.add_text("HPLC STANDARDIZATION / SPECIFICATION", pdf.margin_x + 325, pdf.current_y - 10, font_size=7.5, font="F2", color=(1, 1, 1))
        pdf.current_y -= 13

        total_mg = 0
        for idx, ing in enumerate(comp, 1):
            bg = (0.96, 0.97, 0.96) if idx % 2 == 0 else (1.0, 1.0, 1.0)
            amt = ing.get("amount_mg", 0)
            total_mg += amt
            pdf.draw_rect(pdf.margin_x, pdf.current_y - 13, pdf.usable_width, 13, fill_color=bg, stroke_color=(0.90, 0.90, 0.90))
            pdf.add_text(str(idx), pdf.margin_x + 6, pdf.current_y - 9.5, font_size=7, font="F1", color=(0.3, 0.3, 0.3))
            pdf.add_text(ing.get("ingredient", "")[:48], pdf.margin_x + 24, pdf.current_y - 9.5, font_size=7.5, font="F1", color=(0.1, 0.1, 0.1))
            pdf.add_text(f"{amt} mg", pdf.margin_x + 250, pdf.current_y - 9.5, font_size=7.5, font="F2", color=(0.18, 0.42, 0.31))
            pdf.add_text(ing.get("standardization", "")[:40], pdf.margin_x + 325, pdf.current_y - 9.5, font_size=7, font="F3", color=(0.35, 0.35, 0.35))
            pdf.current_y -= 13

        # Product Summary Line
        dosage_note = f"Dose: {p.get('dosage', '')[:70]} | Total Actives per Unit: {total_mg} mg"
        pdf.draw_rect(pdf.margin_x, pdf.current_y - 12, pdf.usable_width, 12, fill_color=(0.92, 0.94, 0.93))
        pdf.add_text(dosage_note, pdf.margin_x + 6, pdf.current_y - 9, font_size=7, font="F2", color=(0.2, 0.3, 0.25))
        pdf.current_y -= 18

    # ================= 21 CLINICAL PROTOCOL KITS =================
    pdf.start_page()
    pdf.add_text("4. MASTER CLINICAL PROTOCOL KITS (K-01 TO K-21)", pdf.margin_x, pdf.current_y, font_size=12, font="F2", color=(0.11, 0.26, 0.20))
    pdf.draw_rect(pdf.margin_x, pdf.current_y - 4, pdf.usable_width, 1.2, fill_color=(0.11, 0.26, 0.20))
    pdf.current_y -= 16

    kit_keys = sorted(MASTER_KITS.keys(), key=lambda k: int(k.split("-")[-1]))
    
    # Kit table header
    pdf.draw_rect(pdf.margin_x, pdf.current_y - 14, pdf.usable_width, 16, fill_color=(0.18, 0.42, 0.31))
    pdf.add_text("KIT ID", pdf.margin_x + 6, pdf.current_y - 10, font_size=8, font="F2", color=(1, 1, 1))
    pdf.add_text("CLINICAL PROTOCOL NAME", pdf.margin_x + 50, pdf.current_y - 10, font_size=8, font="F2", color=(1, 1, 1))
    pdf.add_text("COMPONENT FORMULATIONS (SKU & ROLE)", pdf.margin_x + 200, pdf.current_y - 10, font_size=8, font="F2", color=(1, 1, 1))
    pdf.current_y -= 16

    for kid in kit_keys:
        kit = MASTER_KITS[kid]
        prods = kit.get("products", [])
        
        # Height: 16 pt base + (12 * len(prods))
        needed = 16 + (len(prods) * 12) + 4
        pdf.check_space(needed)

        pdf.draw_rect(pdf.margin_x, pdf.current_y - needed, pdf.usable_width, needed, fill_color=(0.97, 0.98, 0.97), stroke_color=(0.85, 0.88, 0.86))
        pdf.add_text(kid, pdf.margin_x + 6, pdf.current_y - 12, font_size=8.5, font="F2", color=(0.11, 0.26, 0.20))
        pdf.add_text(kit.get("name", ""), pdf.margin_x + 50, pdf.current_y - 12, font_size=8.5, font="F2", color=(0.15, 0.15, 0.15))
        
        y_prod = pdf.current_y - 12
        for pr in prods:
            p_text = f"• {pr.get('sku')}: {pr.get('name')} — {pr.get('role')}"
            pdf.add_text(p_text[:75], pdf.margin_x + 200, y_prod, font_size=7, font="F1", color=(0.25, 0.25, 0.25))
            y_prod -= 12

        pdf.current_y -= (needed + 4)

    # ================= 10 RETAIL PRODUCTS =================
    pdf.start_page()
    pdf.add_text("5. DIRECT-TO-CONSUMER RETAIL / OTC PRODUCTS (10 FORMULATIONS)", pdf.margin_x, pdf.current_y, font_size=12, font="F2", color=(0.11, 0.26, 0.20))
    pdf.draw_rect(pdf.margin_x, pdf.current_y - 4, pdf.usable_width, 1.2, fill_color=(0.11, 0.26, 0.20))
    pdf.current_y -= 16

    # Retail Table Header
    pdf.draw_rect(pdf.margin_x, pdf.current_y - 14, pdf.usable_width, 16, fill_color=(0.18, 0.42, 0.31))
    pdf.add_text("ID", pdf.margin_x + 6, pdf.current_y - 10, font_size=8, font="F2", color=(1, 1, 1))
    pdf.add_text("PRODUCT NAME & FORM", pdf.margin_x + 65, pdf.current_y - 10, font_size=8, font="F2", color=(1, 1, 1))
    pdf.add_text("PRIMARY INGREDIENTS & SPECIFICATION", pdf.margin_x + 210, pdf.current_y - 10, font_size=8, font="F2", color=(1, 1, 1))
    pdf.add_text("MRP", pdf.width - pdf.margin_x - 40, pdf.current_y - 10, font_size=8, font="F2", color=(1, 1, 1))
    pdf.current_y -= 16

    for ret in RETAIL_PRODUCTS:
        needed = 32
        pdf.check_space(needed)

        pdf.draw_rect(pdf.margin_x, pdf.current_y - needed, pdf.usable_width, needed, fill_color=(0.98, 0.98, 0.98), stroke_color=(0.88, 0.88, 0.88))
        pdf.add_text(ret["id"], pdf.margin_x + 6, pdf.current_y - 12, font_size=7.5, font="F2", color=(0.11, 0.26, 0.20))
        pdf.add_text(ret["name"], pdf.margin_x + 65, pdf.current_y - 12, font_size=8, font="F2", color=(0.1, 0.1, 0.1))
        pdf.add_text(ret["dosage_form"], pdf.margin_x + 65, pdf.current_y - 22, font_size=6.5, font="F3", color=(0.4, 0.4, 0.4))
        
        pdf.add_text(ret["key_ingredients"][:65], pdf.margin_x + 210, pdf.current_y - 12, font_size=7, font="F1", color=(0.2, 0.2, 0.2))
        pdf.add_text(f"Dose: {ret['dosage'][:60]}", pdf.margin_x + 210, pdf.current_y - 22, font_size=6.5, font="F3", color=(0.35, 0.35, 0.35))
        
        pdf.add_text(f"₹{ret['mrp']}", pdf.width - pdf.margin_x - 40, pdf.current_y - 14, font_size=8, font="F2", color=(0.18, 0.42, 0.31))
        pdf.current_y -= (needed + 4)

    # ================= MANUFACTURING & QA SPECIFICATIONS =================
    pdf.start_page()
    pdf.add_text("6. QUALITY ASSURANCE, PACKAGING & RELEASE CONTROLS", pdf.margin_x, pdf.current_y, font_size=12, font="F2", color=(0.11, 0.26, 0.20))
    pdf.draw_rect(pdf.margin_x, pdf.current_y - 4, pdf.usable_width, 1.2, fill_color=(0.11, 0.26, 0.20))
    pdf.current_y -= 18

    qa_sections = [
        ("A. Schedule T (AYUSH Good Manufacturing Practice) Parameters:", [
            "• Raw Material Testing: Macro & microscopic botanical authentication, TLC/HPTLC fingerprinting against UPI/API standards.",
            "• Heavy Metal Limits: Lead (< 10 ppm), Cadmium (< 0.3 ppm), Arsenic (< 3.0 ppm), Mercury (< 1.0 ppm) per ICP-MS.",
            "• Microbial Safety: Total Aerobic Count (< 10^5 CFU/g), Yeast/Mould (< 10^3 CFU/g), E. coli (Absent), Salmonella (Absent).",
            "• Pesticide Residues & Aflatoxins: Total Aflatoxins B1+B2+G1+G2 (< 10 ppb) per AOAC fluorometric assay."
        ]),
        ("B. Schedule E(1) Mudabbar (Detoxification) Protocol:", [
            "• Kuchla (Strychnos nux-vomica): 7-day immersion in cow's milk with daily replacement, boiling, endocarp de-sheathing,",
            "  and light roasting in Cow Ghee (Roghan-e-Zard) to achieve Strychnine alkaloid moderation.",
            "• Suranjan (Colchicum autumnale): Steeping in Roghan-e-Badam (sweet almond oil) followed by decoction rinsing to moderate Colchicine.",
            "• Kushtajat (Calx): Quadruple calcination cycle in airtight earthen crucibles (Boodha) monitored by X-Ray Diffraction (XRD)."
        ]),
        ("C. Primary Packaging & Shelf-Life Specifications:", [
            "• Safoof / Powders: Food-grade amber HDPE jars with heat-induction foil seals and food-grade silica desiccant bags.",
            "• Capsules / Tablets: Cold-form Alu-Alu blister packaging with light-blocking barrier film.",
            "• Syrups & Decoctions: Amber PET pharmaceutical bottles with tamper-evident pilfer-proof (ROPP) caps.",
            "• Shelf-Life: 36 months from Date of Manufacturing under ambient controlled temperature (20-25 deg C, RH < 60%)."
        ])
    ]

    for sec_title, bullets in qa_sections:
        pdf.add_text(sec_title, pdf.margin_x, pdf.current_y, font_size=9.5, font="F2", color=(0.11, 0.26, 0.20))
        pdf.current_y -= 14
        for b in bullets:
            pdf.add_text(b, pdf.margin_x + 8, pdf.current_y, font_size=8, font="F1", color=(0.2, 0.2, 0.2))
            pdf.current_y -= 12
        pdf.current_y -= 6

    # Sign-off box
    pdf.draw_rect(pdf.margin_x, pdf.current_y - 60, pdf.usable_width, 60, fill_color=(0.95, 0.97, 0.96), stroke_color=(0.80, 0.85, 0.82))
    pdf.add_text("MANUFACTURING APPROVAL & AUTHORIZATION SIGN-OFF", pdf.margin_x + 10, pdf.current_y - 16, font_size=8.5, font="F2", color=(0.11, 0.26, 0.20))
    pdf.add_text("Head of Manufacturing & Technical Operations: ___________________________", pdf.margin_x + 10, pdf.current_y - 32, font_size=8, font="F1", color=(0.3, 0.3, 0.3))
    pdf.add_text("Chief Quality Assurance Officer (QA/QC): ___________________________", pdf.margin_x + 10, pdf.current_y - 48, font_size=8, font="F1", color=(0.3, 0.3, 0.3))
    pdf.add_text("Date: ____ / ____ / 2026", pdf.width - pdf.margin_x - 120, pdf.current_y - 48, font_size=8, font="F2", color=(0.3, 0.3, 0.3))

    return pdf.compile()


def build_html_dossier():
    """Generates an executive, high-DPI printable HTML dossier with CSS print styles."""
    html_lines = []
    html_lines.append("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ZAYVORA Health OS™ - Master Manufacturing BOM & Formulations Dossier</title>
  <style>
    :root {
      --primary: #1B4332;
      --primary-dark: #0D2818;
      --primary-light: #2D6A4F;
      --accent: #D4AF37;
      --accent-warm: #E76F51;
      --bg: #FAFAF7;
      --card-bg: #FFFFFF;
      --text: #1F2937;
      --text-muted: #4B5563;
      --border: #E5E7EB;
    }
    * { box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      margin: 0;
      padding: 24px;
    }
    .container {
      max-width: 1200px;
      margin: 0 auto;
      background: #FFFFFF;
      padding: 40px;
      border-radius: 8px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    .print-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #ECFDF5;
      border: 1px solid #A7F3D0;
      padding: 12px 20px;
      border-radius: 6px;
      margin-bottom: 24px;
    }
    .btn-print {
      background: var(--primary-light);
      color: white;
      border: none;
      padding: 8px 18px;
      font-weight: 600;
      border-radius: 6px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }
    .btn-print:hover { background: var(--primary); }
    .header-banner {
      background: linear-gradient(135deg, var(--primary-dark), var(--primary));
      color: white;
      padding: 32px;
      border-radius: 8px;
      margin-bottom: 24px;
    }
    .header-banner h1 { margin: 0 0 6px 0; font-size: 26px; letter-spacing: -0.5px; }
    .header-banner .subtitle { color: #A7F3D0; font-size: 15px; margin: 0 0 12px 0; font-weight: 500; }
    .header-banner .doc-info { font-size: 12px; color: #D1FAE5; display: flex; gap: 20px; flex-wrap: wrap; }
    .section-title {
      font-size: 18px;
      font-weight: 700;
      color: var(--primary-dark);
      border-bottom: 2px solid var(--primary-light);
      padding-bottom: 6px;
      margin-top: 36px;
      margin-bottom: 16px;
    }
    .meta-box {
      background: #F9FAFB;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 16px 20px;
      margin-bottom: 24px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 12px;
      font-size: 13px;
    }
    .meta-item strong { color: var(--primary-dark); display: block; font-size: 11px; text-transform: uppercase; }
    .product-card {
      border: 1px solid var(--border);
      border-radius: 8px;
      margin-bottom: 24px;
      overflow: hidden;
      page-break-inside: avoid;
    }
    .product-header {
      background: #F0FDF4;
      border-bottom: 1px solid #DCFCE7;
      padding: 14px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }
    .product-sku {
      font-weight: 800;
      color: var(--primary);
      font-size: 16px;
      margin-right: 8px;
    }
    .product-title {
      font-size: 16px;
      font-weight: 700;
      color: #111827;
    }
    .product-unani {
      font-style: italic;
      color: #4B5563;
      font-size: 13px;
      margin-left: 8px;
    }
    .badge {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 600;
    }
    .badge-rx { background: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5; }
    .badge-otc { background: #D1FAE5; color: #065F46; border: 1px solid #6EE7B7; }
    .badge-reg { background: #E0E7FF; color: #3730A3; border: 1px solid #C7D2FE; }
    .product-meta-row {
      padding: 10px 20px;
      background: #F9FAFB;
      border-bottom: 1px solid var(--border);
      font-size: 12px;
      display: flex;
      gap: 20px;
      flex-wrap: wrap;
    }
    table.bom-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12.5px;
    }
    table.bom-table th {
      background: #F3F4F6;
      color: #374151;
      text-align: left;
      padding: 8px 14px;
      font-weight: 600;
      border-bottom: 1px solid var(--border);
    }
    table.bom-table td {
      padding: 8px 14px;
      border-bottom: 1px solid #F3F4F6;
    }
    table.bom-table tr:nth-child(even) { background: #FAFAFA; }
    .product-footer {
      padding: 10px 20px;
      background: #F8FAFC;
      border-top: 1px solid var(--border);
      font-size: 12px;
      color: #334155;
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
    }
    @media print {
      body { background: white; padding: 0; }
      .container { max-width: 100%; padding: 0; box-shadow: none; }
      .print-bar { display: none; }
      .product-card { page-break-inside: avoid; }
      @page { size: A4; margin: 12mm; }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="print-bar">
      <div>
        <strong>ZAYVORA Health OS™ Pharmaceutical Manufacturing Dossier</strong>
        <span style="color:#059669; margin-left: 10px;">• Ready for Commercial Export / PDF Print</span>
      </div>
      <button class="btn-print" onclick="window.print()">
        <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M2.5 8a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/><path d="M5 1a2 2 0 0 0-2 2v2H2a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h1v1a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-1h1a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-1V3a2 2 0 0 0-2-2H5zM4 3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2H4V3zm1 5a2 2 0 0 0-2 2v1H2a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v-1a2 2 0 0 0-2-2H5zm7 2v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1z"/></svg>
        Print / Save to PDF
      </button>
    </div>

    <div class="header-banner">
      <h1>ZAYVORA HEALTH OS™ — PHARMACEUTICAL MASTER BOM</h1>
      <div class="subtitle">Complete Standardized Formulations, HPLC Extract Assays & Manufacturing Specifications</div>
      <div class="doc-info">
        <span><strong>Document ID:</strong> ZAY-MFG-BOM-2026-V5</span>
        <span><strong>Version:</strong> 5.0 Enterprise</span>
        <span><strong>Compliance:</strong> AYUSH Schedule T (GMP) / FSSAI 2022</span>
        <span><strong>Coverage:</strong> 32 Master Clinical + 21 Protocol Kits + 10 Retail</span>
      </div>
    </div>

    <div class="meta-box">
      <div class="meta-item">
        <strong>Manufacturer / Sponsor</strong>
        ZAYVORA Health OS Technologies & Herbal Formulations Desk
      </div>
      <div class="meta-item">
        <strong>Pharmacopoeial Reference</strong>
        Unani Pharmacopoeia of India (UPI) & Ayurvedic Pharmacopoeia (API)
      </div>
      <div class="meta-item">
        <strong>Quality Control Assurance</strong>
        HPLC Phytochemical Marker Assay + Heavy Metal ICP-MS Clearance
      </div>
      <div class="meta-item">
        <strong>Schedule E(1) Governance</strong>
        Verified Mudabbar (Detoxification) Process Standard Operating Procedures
      </div>
    </div>

    <div class="section-title">1. Master Clinical Formulations (ZAY-001 through ZAY-032)</div>
""")

    skus = sorted(MASTER_PRODUCTS.keys(), key=lambda s: int(s.split("-")[-1]))
    for sku in skus:
        p = MASTER_PRODUCTS[sku]
        comp = p.get("composition", [])
        is_rx = p.get("is_prescription_required", False)
        rx_badge = '<span class="badge badge-rx">Rx Schedule E-1 / Doctor Signature</span>' if is_rx else '<span class="badge badge-otc">Dispensary Standard</span>'
        reg_badge = f'<span class="badge badge-reg">{p.get("regulatory_track", "")}</span>'
        
        total_mg = sum(ing.get("amount_mg", 0) for ing in comp)

        html_lines.append(f"""
    <div class="product-card">
      <div class="product-header">
        <div>
          <span class="product-sku">{sku}</span>
          <span class="product-title">{p.get('name', '')}</span>
          <span class="product-unani">({p.get('unani_name', '')})</span>
        </div>
        <div>
          {rx_badge}
          {reg_badge}
        </div>
      </div>
      <div class="product-meta-row">
        <span><strong>Organ Axis:</strong> {p.get('organ_axis', '')}</span>
        <span><strong>Dosage Form:</strong> {p.get('formulation_type', '')}</span>
        <span><strong>MRP:</strong> ₹{p.get('mrp_inr', 0)}</span>
        <span><strong>Primary Indication:</strong> {p.get('primary_indication', '')}</span>
      </div>
      <table class="bom-table">
        <thead>
          <tr>
            <th style="width: 40px;">#</th>
            <th>Botanical / Classical Component</th>
            <th style="width: 120px;">Amount (mg)</th>
            <th style="width: 100px;">% of Formula</th>
            <th>Standardization / Active Marker Specification</th>
          </tr>
        </thead>
        <tbody>
""")
        for idx, ing in enumerate(comp, 1):
            amt = ing.get("amount_mg", 0)
            pct = (amt / total_mg * 100) if total_mg > 0 else 0
            html_lines.append(f"""
          <tr>
            <td>{idx}</td>
            <td><strong>{ing.get('ingredient', '')}</strong></td>
            <td style="color: #047857; font-weight: 600;">{amt} mg</td>
            <td>{pct:.1f}%</td>
            <td><code>{ing.get('standardization', '')}</code></td>
          </tr>
""")
        html_lines.append(f"""
        </tbody>
      </table>
      <div class="product-footer">
        <div><strong>Dosage & Route:</strong> {p.get('dosage', '')}</div>
        <div><strong>Total Actives per Dose:</strong> {total_mg} mg</div>
      </div>
    </div>
""")

    # Section 2: Clinical Protocol Kits
    html_lines.append("""
    <div class="section-title">2. Clinical Protocol Kits (21 Treatment Packs)</div>
    <table class="bom-table" style="background: white; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; margin-bottom: 24px;">
      <thead>
        <tr>
          <th style="width: 80px;">Kit ID</th>
          <th style="width: 260px;">Protocol Name</th>
          <th>Component Formulations & Clinical Rationale</th>
        </tr>
      </thead>
      <tbody>
""")
    kit_keys = sorted(MASTER_KITS.keys(), key=lambda k: int(k.split("-")[-1]))
    for kid in kit_keys:
        k = MASTER_KITS[kid]
        prods_html = "".join([f"<li style='margin-bottom: 4px;'><strong>{pr.get('sku')} ({pr.get('name')}):</strong> {pr.get('role')}</li>" for pr in k.get("products", [])])
        html_lines.append(f"""
        <tr>
          <td><strong style="color: var(--primary);">{kid}</strong></td>
          <td><strong>{k.get('name', '')}</strong></td>
          <td><ul style="margin: 0; padding-left: 18px; font-size: 12px;">{prods_html}</ul></td>
        </tr>
""")
    html_lines.append("""
      </tbody>
    </table>
""")

    # Section 3: Retail OTC Products
    html_lines.append("""
    <div class="section-title">3. Consumer Retail / Storefront Products (10 Formulations)</div>
    <table class="bom-table" style="background: white; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; margin-bottom: 24px;">
      <thead>
        <tr>
          <th style="width: 90px;">SKU ID</th>
          <th style="width: 180px;">Product Name & Form</th>
          <th>Primary Key Ingredients</th>
          <th style="width: 220px;">Dosage & Indication</th>
          <th style="width: 80px;">MRP</th>
        </tr>
      </thead>
      <tbody>
""")
    for ret in RETAIL_PRODUCTS:
        html_lines.append(f"""
        <tr>
          <td><strong style="color: var(--primary);">{ret['id']}</strong></td>
          <td><strong>{ret['name']}</strong><br><small style="color:#6B7280;">{ret['dosage_form']}</small></td>
          <td style="font-size: 12px;">{ret['key_ingredients']}</td>
          <td style="font-size: 12px;"><strong>Dose:</strong> {ret['dosage']}<br><strong>Indication:</strong> {ret['indications']}</td>
          <td><strong style="color:#047857;">₹{ret['mrp']}</strong></td>
        </tr>
""")
    html_lines.append("""
      </tbody>
    </table>

    <div class="section-title">4. GMP Quality Assurance & Schedule E(1) Mudabbar SOPs</div>
    <div style="background: #F9FAFB; border: 1px solid var(--border); border-radius: 8px; padding: 20px; font-size: 13px; line-height: 1.6;">
      <h4 style="margin: 0 0 8px 0; color: var(--primary);">Schedule T (AYUSH GMP) Release Controls</h4>
      <p style="margin: 0 0 12px 0;">All finished batches must undergo release testing before leaving the quarantine hold: Assay testing by HPLC, Moisture content (Loss on Drying &lt; 8.0%), Disintegration time for tablets (&lt; 30 minutes), and Aerobic Microbial Plate Count (&lt; 10^5 CFU/g).</p>
      
      <h4 style="margin: 0 0 8px 0; color: var(--primary);">Mudabbar (Purification) Certification for Schedule E(1) Herbs</h4>
      <p style="margin: 0 0 12px 0;">Kuchla (Strychnos nux-vomica) and Suranjan (Colchicum autumnale) are subject to mandatory multi-stage purification protocols. Raw batches must be accompanied by an authenticated Mudabbar batch certificate showing alkaloid moderation prior to formulation into finished products.</p>
      
      <h4 style="margin: 0 0 8px 0; color: var(--primary);">Packaging & Shelf-Life Protocol</h4>
      <p style="margin: 0;">Finished products must be packaged into food-grade, induction-sealed HDPE containers or Alu-Alu cold form blisters with nitrogen purging where appropriate. Labeled shelf-life: 36 months under controlled ambient room temperature (20-25°C, RH &lt; 60%).</p>
    </div>

    <div style="margin-top: 40px; padding: 20px; border-top: 2px dashed #D1D5DB; display: flex; justify-content: space-between; font-size: 12px; color: #6B7280;">
      <div>Authorized Signatory (Manufacturing QA): ___________________________</div>
      <div>Technical Director (Formulations): ___________________________</div>
      <div>Date: ____ / ____ / 2026</div>
    </div>
  </div>
</body>
</html>
""")
    return "".join(html_lines)


def main():
    print("=" * 70)
    print("ZAYVORA Health OS™ - Pharmaceutical Manufacturing BOM Generator")
    print("=" * 70)

    # Target paths
    docs_dir = os.path.join(BASE_DIR, "docs")
    os.makedirs(docs_dir, exist_ok=True)

    pdf_path = os.path.join(docs_dir, "ZAYVORA_Master_Product_Manufacturing_BOM.pdf")
    html_path = os.path.join(docs_dir, "ZAYVORA_Master_Product_Manufacturing_BOM.html")

    # 1. Generate PDF
    print("[1/2] Generating standalone Adobe PDF document...")
    pdf_bytes = build_pdf_dossier()
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)
    pdf_size_kb = len(pdf_bytes) / 1024
    print(f" -> Generated: {pdf_path} ({pdf_size_kb:.1f} KB)")

    # 2. Generate HTML
    print("[2/2] Generating responsive high-DPI printable HTML dossier...")
    html_content = build_html_dossier()
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    html_size_kb = len(html_content.encode("utf-8")) / 1024
    print(f" -> Generated: {html_path} ({html_size_kb:.1f} KB)")

    print("\n✓ SUCCESS: Both Manufacturing Dossier formats generated successfully!")
    print(f"• PDF File:  {pdf_path}")
    print(f"• HTML File: {html_path}")


if __name__ == "__main__":
    main()
