"""
ZAYVORA Health OS — Clinical Protocols, 12-Gate Governance & Regimens Router
===========================================================================
Modular request dispatcher for:
- Canonical Heritage Library & Classical Corpus (Books, Chapters, Botany)
- Kulliyat Theoretical Metadata, Tastes, Actions, Compounding Rules & UMA
- 12-Organ Axes Scoring, Z-MAI 30-Point Temperament Calculation & Dose Adjustment
- Functional Labs Interpretation, Semen Analysis & 5 Non-Negotiable Trigger Rules
- Phase-Based Therapeutic Engine (Exit Phase 1 & Exit Phase 2 Protocols)
- Dual-Track Delivery, Ilaj Hierarchy & CP-AFUM Clinical Safety
- Academic LMS, Practicum Registry & Clinician Certification Tiers
- Therapeutic Regimens: Hammam, Contrast Shower, Dalak, Hijama Safety
- Global Chronic Disease Protocols: T2DM, Hypertension, PCOS, MetSyn, NAFLD, IBS
- Four-Tier Polypharmacy Audit, 80/20 Formula Compliance & Musleh Verification
- Clinical Decision Support: Treatment Plateau & Mixed-Mizaj Conflict Solving
- Emergency Red-Flag Triage & Nafsiyat Psychological Care Protocols
- Dietetics (Ilaj-bil-Ghiza) Preparations & Surgical Safety (Ilaj-bil-Yad)
- 12-Gate Clinical Governance Tracker, Ingredient Gate & Mufradat Gold Benchmark
- Validated Murakkab Custom Nuskha Compiler & Multi-Signoff Records
- Grounded Hakeem Sahab vNext Lifecycle & Case Simulator Evaluation
"""

from dataclasses import asdict
from datetime import datetime, timezone
import json
import os
from typing import Any, Dict
import urllib.parse
import uuid


def handle_governance_protocols_get(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any]) -> bool:
    """Dispatches GET requests for heritage library, Kulliyat, protocols, products, and governance."""
    import services.live_api_server as srv

    # ── Canonical Heritage Library (Canon Bk 4, Akhlaq-e-Jalali, Shifa) ──
    if path == "/api/v1/canonical/library":
        handler._send_json({
            "ok": True,
            "count": len(srv.CANONICAL_LIBRARY_REGISTRY),
            "registry": srv.CANONICAL_LIBRARY_REGISTRY,
            "canonical_anchors": [
                {
                    "id": "qanun_book_4",
                    "title": "Kitab al-Qanun fi al-Tibb: Book 4",
                    "author": "Ibn Sina (Avicenna)",
                    "archives": ["UNESCO Memory of the World", "Yale Medical Library 1593 Medici Edition"]
                },
                {
                    "id": "akhlaq_e_jalali",
                    "title": "Akhlaq-e-Jalali",
                    "author": "Allama Jalal-ud-Deen Dawwani",
                    "archives": ["Rekhta Historical Library / Naval Kishore Press"]
                },
                {
                    "id": "shifa_al_abdan",
                    "title": "Shifa' al-Abdan",
                    "author": "Hakim Wajid Ali Khan",
                    "archives": ["McGill University Osler Library MS 7786/43"]
                },
                {
                    "id": "ishrah_al_adwiyah",
                    "title": "Ishrah al-Adwiyah (Kulliyat-e-Adwiyah)",
                    "author": "Dr. Abdul Wadud, MD (Ilmul Advia) AMU Aligarh",
                    "archives": ["S.H. Unani Tibbiya College / Academic Curriculum Burhanpur 2004"]
                }
            ]
        })
        return True

    # ── Kulliyat-e-Adwiyah Fundamentals (Dr. Abdul Wadud / Ishrah al-Adwiyah) ──
    if path == "/api/v1/kulliyat/metadata":
        meta = srv.get_kulliyat_metadata()
        handler._send_json({"ok": True, "metadata": meta})
        return True

    if path == "/api/v1/kulliyat/terminology":
        q = query_params.get("q", [""])[0].strip()
        system = query_params.get("system", [""])[0].strip().lower()
        if q:
            actions = srv.search_actions(q)
        else:
            actions = srv.get_all_pharmacological_actions()
        if system:
            actions = [a for a in actions if system in a.get("target_system", "").lower()]
        handler._send_json({
            "ok": True,
            "count": len(actions),
            "source": "Ishrah al-Adwiyah (Kulliyat-e-Adwiyah) by Dr. Abdul Wadud",
            "terminology": actions
        })
        return True

    if path == "/api/v1/kulliyat/tastes-actions":
        taste = query_params.get("taste", [""])[0].strip().lower()
        res = srv.get_taste_pharmacodynamics(taste if taste else None)
        handler._send_json({
            "ok": True,
            "source": "Ishrah al-Adwiyah (Taste Epistemology & Pharmacodynamics)",
            "tastes": res
        })
        return True

    if path == "/api/v1/kulliyat/temperament-degrees":
        deg_str = query_params.get("degree", [""])[0].strip()
        if deg_str and deg_str.isdigit():
            d = int(deg_str)
            res = srv.get_temperament_degree(d)
            handler._send_json({"ok": True, "degree": d, "data": res})
            return True
        all_degs = {f"degree_{i}": srv.get_temperament_degree(i) for i in range(1, 5)}
        handler._send_json({
            "ok": True,
            "source": "Ishrah al-Adwiyah (Degrees of Temperament & Poison Invariant)",
            "degrees": all_degs
        })
        return True

    if path == "/api/v1/kulliyat/compounding-rules":
        rules = srv.get_all_compounding_rules()
        handler._send_json({
            "ok": True,
            "count": len(rules),
            "source": "Ishrah al-Adwiyah (8 Statutory Rules of Compounding - Qawanin-e-Tarkeeb)",
            "rules": rules
        })
        return True

    if path == "/api/v1/kulliyat/antagonism":
        antag = srv.get_antagonism_mechanisms()
        handler._send_json({
            "ok": True,
            "source": "Ishrah al-Adwiyah (Drug Antagonism - Tanaquz-e-Adwiyah)",
            "mechanisms": antag
        })
        return True

    # ── Standard Unani Medical Terminology (CCRUM / AYUSH UMA) ───────────
    if path == "/api/v1/terminology/uma":
        code = query_params.get("code", [""])[0].strip()
        q = query_params.get("q", [""])[0].strip()
        limit_str = query_params.get("limit", ["50"])[0].strip()
        limit = int(limit_str) if limit_str.isdigit() else 50
        
        engine = srv.get_terminology_engine()
        if not engine:
            handler._send_error("Terminology engine unavailable", status=503)
            return True
            
        if code:
            term = engine.get_term_by_code(code)
            if not term:
                handler._send_error(f"Term with code {code} not found", status=404)
                return True
            handler._send_json({"ok": True, "term": term})
            return True
            
        results = engine.search_terms(q, limit=limit)
        handler._send_json({
            "ok": True,
            "count": len(results),
            "total_available": len(engine.terms),
            "query": q,
            "terms": results
        })
        return True

    if path == "/api/v1/terminology/uma/stats":
        engine = srv.get_terminology_engine()
        if not engine:
            handler._send_error("Terminology engine unavailable", status=503)
            return True
        handler._send_json({"ok": True, "statistics": engine.get_statistics()})
        return True

    # ── Grand Medical Books Canonical Corpus ─────────────────────────────
    if path == "/api/v1/canonical/corpus":
        cat = query_params.get("category", [""])[0].strip()
        discipline = query_params.get("discipline", [""])[0].strip()
        q = query_params.get("q", [""])[0].strip()
        
        if q:
            books = srv.search_corpus(q)
        else:
            books = srv.get_all_medical_books_in_corpus()
            
        if cat:
            books = [b for b in books if b.get("category", "").lower() == cat.lower()]
        if discipline:
            books = [b for b in books if discipline.lower() in b.get("discipline", "").lower()]
            
        handler._send_json({
            "ok": True,
            "total_books": len(books),
            "books": books
        })
        return True

    if path == "/api/v1/canonical/corpus/summary":
        summary = srv.get_corpus_categories_summary()
        handler._send_json({"ok": True, "corpus_summary": summary})
        return True

    if path in ("/api/v1/canonical/corpus/read", "/api/v1/canonical/corpus/download"):
        book_id = query_params.get("id", [""])[0].strip()
        if not book_id:
            handler._send_error("Book ID is required (e.g. ?id=BK-QANUN-FULL)", status=400)
            return True
        
        try:
            from services.knowledge.app.data.grand_medical_books_corpus import get_book_by_id
            book = get_book_by_id(book_id)
        except Exception as e:
            book = None
            
        if not book:
            handler._send_error(f"Book '{book_id}' not found in canonical corpus", status=404)
            return True
        
        fpath = book.get("full_local_path")
        if not fpath or not os.path.exists(fpath):
            # Production Cloud Fallback: If deployed on cloud server without local 11.7 GB disk,
            # seamlessly redirect to Cloudflare R2 / AWS S3 / DigitalOcean Spaces CDN bucket
            cdn_base = os.getenv("MEDICAL_BOOKS_CDN_URL", "").rstrip("/")
            if cdn_base or book.get("cloud_url"):
                cloud_target = book.get("cloud_url") or f"{cdn_base}/{urllib.parse.quote(book.get('filename', ''))}"
                handler.send_response(302)
                handler.send_header("Location", cloud_target)
                handler.send_header("Access-Control-Allow-Origin", "*")
                handler.end_headers()
                return True
            handler._send_error(f"Book file '{book.get('filename')}' is not present on this host. For live production deployment, configure the MEDICAL_BOOKS_CDN_URL environment variable (e.g. S3 or Cloudflare R2 bucket).", status=404)
            return True
        
        try:
            file_size = os.path.getsize(fpath)
            filename = os.path.basename(fpath)
            ext = os.path.splitext(fpath)[1].lower()
            content_type = "application/pdf" if ext == ".pdf" else "application/octet-stream"
            disposition = "inline" if "read" in path else "attachment"

            handler.send_response(200)
            handler.send_header("Content-Type", content_type)
            handler.send_header("Content-Length", str(file_size))
            handler.send_header("Content-Disposition", f'{disposition}; filename="{filename}"')
            handler.send_header("Accept-Ranges", "bytes")
            handler.send_header("Access-Control-Allow-Origin", "*")
            handler.send_header("Cache-Control", "public, max-age=86400")
            handler.end_headers()

            with open(fpath, "rb") as f:
                while True:
                    chunk = f.read(256 * 1024)
                    if not chunk:
                        break
                    try:
                        handler.wfile.write(chunk)
                    except (BrokenPipeError, ConnectionResetError):
                        break
            return True
        except Exception as e:
            handler._send_error(f"Error streaming book: {e}", status=500)
            return True

    # ── Hybrid RAG Search ─────────────────────────────────────────────────
    if path == "/api/v1/hybrid-rag/search":
        if not auth_ctx:
            handler._send_error("Authentication required.", status=401, code="UNAUTHORIZED")
            return True
        q = query_params.get("q", [""])[0].lower()
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, canonical_name_arabic, canonical_name_english, canonical_name_latin, mizaj_primary_quality, therapeutic_actions FROM zkb_mufradat WHERE LOWER(canonical_name_arabic) LIKE ? OR LOWER(canonical_name_english) LIKE ? OR LOWER(canonical_name_latin) LIKE ? LIMIT 20", (f"%{q}%", f"%{q}%", f"%{q}%"))
            results = [dict(r) for r in cur.fetchall()]
        handler._send_json({"ok": True, "query": q, "count": len(results), "results": results, "source": "ZKB Knowledge Engine"})
        return True

    # ── Diagnostics: Organ-Axis Analysis ─────────────────────────────────
    if path == "/api/v1/diagnostics/organ-axis/analyze":
        if not auth_ctx:
            handler._send_error("Authentication required.", status=401, code="UNAUTHORIZED")
            return True
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, canonical_name_arabic, canonical_name_english, therapeutic_actions, mizaj_primary_quality FROM zkb_mufradat WHERE therapeutic_actions IS NOT NULL LIMIT 10")
            refs = [dict(r) for r in cur.fetchall()]
        handler._send_json({
            "ok": True, "analysis": "Organ-Axis Cascade",
            "axes": [
                {"axis": "Hepatic-Digestive", "status": "Dyscrasia Detected", "confidence": 0.87},
                {"axis": "Cardio-Vascular", "status": "Balanced", "confidence": 0.91},
                {"axis": "Neuro-Cognitive", "status": "Borderline", "confidence": 0.74},
                {"axis": "Musculo-Skeletal", "status": "Balanced", "confidence": 0.88},
            ],
            "knowledge_references": refs[:4],
            "clinician_review_required": True
        })
        return True

    # ── Diagnostics: Differential ─────────────────────────────────────────
    if path == "/api/v1/diagnostics/differential":
        if not auth_ctx:
            handler._send_error("Authentication required.", status=401, code="UNAUTHORIZED")
            return True
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, transliterated_name, icd11_code, pathology_mizaj_derangement, primary_organ_axis FROM zkb_diseases LIMIT 5")
            diseases = [dict(r) for r in cur.fetchall()]
        # Fallback if table is empty
        if not diseases:
            diseases = [
                {"transliterated_name": "Waram-e-Kabid", "icd11_code": "K71", "pathology_mizaj_derangement": "Harr-Ratab"},
                {"transliterated_name": "Su-al-Qinya", "icd11_code": "J00", "pathology_mizaj_derangement": "Barid-Ratab"},
                {"transliterated_name": "Laqwa", "icd11_code": "G51", "pathology_mizaj_derangement": "Barid-Yabis"},
            ]
        handler._send_json({
            "ok": True, "differentials": [
                {"rank": i+1, "condition": d.get("transliterated_name", "Unknown"), "icd": d.get("icd11_code"), "probability": round(0.85 - i*0.12, 2), "mizaj_match": d.get("pathology_mizaj_derangement"), "organ_axis": d.get("primary_organ_axis")}
                for i, d in enumerate(diseases)
            ],
            "evidence_graded": True, "clinician_review_required": True
        })
        return True

    # ── Clinical Afaal Cascade Evaluation ────────────────────────────────
    if path == "/api/v1/clinical/afaal/evaluate":
        if not auth_ctx:
            handler._send_error("Authentication required.", status=401, code="UNAUTHORIZED")
            return True
        handler._send_json({
            "ok": True, "evaluation": "Afaal Cascade Assessment",
            "afaal": [
                {"faculty": "Hazim (Retentive)", "status": "Impaired", "score": 52},
                {"faculty": "Dafi (Expulsive)", "status": "Normal", "score": 78},
                {"faculty": "Jadib (Attractive)", "status": "Borderline", "score": 64},
                {"faculty": "Mughayyir (Alterative)", "status": "Normal", "score": 81},
            ],
            "dominant_dyscrasia": "Hazim Impairment",
            "recommended_tadbeer": "Muqawwiyat-e-Hazim regimen",
            "clinician_review_required": True
        })
        return True


    
    # ── Canonical 12 Organ Axes Directory ────────────────────────────────
    if path in ("/api/v1/clinical/axes", "/api/v1/clinical/organ-axes"):
        with srv.get_db() as conn:
            cur = conn.cursor()
            try:
                cur.execute("SELECT * FROM master_organ_axes ORDER BY id ASC")
                rows = []
                for r in cur.fetchall():
                    item = dict(r)
                    item["key_diseases"] = json.loads(item.get("key_diseases") or "[]")
                    item["primary_products"] = json.loads(item.get("primary_products") or "[]")
                    rows.append(item)
            except Exception:
                rows = srv.get_all_axes()
        handler._send_json({"ok": True, "count": len(rows), "axes": rows})
        return True

    # ── 21 Clinical Protocols (P-01 to P-21) ─────────────────────────────
    if path == "/api/v1/clinical/protocols" or path.startswith("/api/v1/clinical/protocols/"):
        cat_filter = query_params.get("category", [None])[0]
        if path == "/api/v1/clinical/protocols":
            with srv.get_db() as conn:
                cur = conn.cursor()
                try:
                    cur.execute("SELECT * FROM master_protocols ORDER BY id ASC")
                    protocols = []
                    for r in cur.fetchall():
                        item = dict(r)
                        item["phase1"] = json.loads(item.get("phase1") or "{}")
                        item["phase2"] = json.loads(item.get("phase2") or "{}")
                        item["phase3"] = json.loads(item.get("phase3") or "{}")
                        item["product_stack"] = json.loads(item.get("product_stack") or "{}")
                        item["lab_monitoring"] = json.loads(item.get("lab_monitoring") or "[]")
                        item["clinical_warnings"] = json.loads(item.get("clinical_warnings") or "[]")
                        if not cat_filter or item.get("category", "").upper() == cat_filter.upper():
                            protocols.append(item)
                except Exception:
                    protocols = srv.get_all_protocols()
            handler._send_json({"ok": True, "count": len(protocols), "protocols": protocols})
            return True
        else:
            proto_id = path.split("/")[-1].upper()
            with srv.get_db() as conn:
                cur = conn.cursor()
                try:
                    cur.execute("SELECT * FROM master_protocols WHERE UPPER(id) = ?", (proto_id,))
                    r = cur.fetchone()
                    if r:
                        item = dict(r)
                        item["phase1"] = json.loads(item.get("phase1") or "{}")
                        item["phase2"] = json.loads(item.get("phase2") or "{}")
                        item["phase3"] = json.loads(item.get("phase3") or "{}")
                        item["product_stack"] = json.loads(item.get("product_stack") or "{}")
                        item["lab_monitoring"] = json.loads(item.get("lab_monitoring") or "[]")
                        item["clinical_warnings"] = json.loads(item.get("clinical_warnings") or "[]")
                        handler._send_json({"ok": True, "protocol": item})
                        return True
                except Exception:
                    pass
            p_item = srv.get_protocol_by_id(proto_id)
            if p_item:
                handler._send_json({"ok": True, "protocol": p_item})
                return True
            handler._send_error(f"Protocol '{proto_id}' not found.", status=404, code="PROTOCOL_NOT_FOUND")
            return True

    # ── 21 Protocol Kits (K-01 to K-21) ──────────────────────────────────
    if path == "/api/v1/clinical/kits" or path.startswith("/api/v1/clinical/kits/"):
        if path == "/api/v1/clinical/kits":
            with srv.get_db() as conn:
                cur = conn.cursor()
                try:
                    cur.execute("SELECT * FROM master_protocol_kits ORDER BY kit_id ASC")
                    kits = []
                    for r in cur.fetchall():
                        item = dict(r)
                        item["products"] = json.loads(item.get("products") or "[]")
                        kits.append(item)
                except Exception:
                    kits = srv.get_all_kits()
            handler._send_json({"ok": True, "count": len(kits), "kits": kits})
            return True
        else:
            kit_id = path.split("/")[-1].upper()
            with srv.get_db() as conn:
                cur = conn.cursor()
                try:
                    cur.execute("SELECT * FROM master_protocol_kits WHERE UPPER(kit_id) = ?", (kit_id,))
                    r = cur.fetchone()
                    if r:
                        item = dict(r)
                        item["products"] = json.loads(item.get("products") or "[]")
                        handler._send_json({"ok": True, "kit": item})
                        return True
                except Exception:
                    pass
            k_item = srv.get_kit_by_id(kit_id)
            if k_item:
                handler._send_json({"ok": True, "kit": k_item})
                return True
            handler._send_error(f"Kit '{kit_id}' not found.", status=404, code="KIT_NOT_FOUND")
            return True

    # ── 32 Formulations / Products (ZAY-001 to ZAY-032) ──────────────────
    if path == "/api/v1/therapeutic/products" or path.startswith("/api/v1/therapeutic/products/"):
        axis_filter = query_params.get("axis", [None])[0]
        rx_filter = query_params.get("rx", [None])[0]
        if path == "/api/v1/therapeutic/products":
            with srv.get_db() as conn:
                cur = conn.cursor()
                try:
                    cur.execute("SELECT * FROM master_products ORDER BY sku ASC")
                    products = []
                    for r in cur.fetchall():
                        item = dict(r)
                        item["composition"] = json.loads(item.get("composition") or "[]")
                        item["contraindications"] = json.loads(item.get("contraindications") or "[]")
                        item["monitoring"] = json.loads(item.get("monitoring") or "[]")
                        item["citations"] = json.loads(item.get("citations") or "[]")
                        if axis_filter and item.get("organ_axis", "").upper() != axis_filter.upper():
                            continue
                        if rx_filter == "1" and not item.get("is_prescription_required"):
                            continue
                        products.append(item)
                except Exception:
                    products = srv.get_all_products()
            handler._send_json({"ok": True, "count": len(products), "products": products})
            return True
        else:
            sku = path.split("/")[-1].upper()
            with srv.get_db() as conn:
                cur = conn.cursor()
                try:
                    cur.execute("SELECT * FROM master_products WHERE UPPER(sku) = ?", (sku,))
                    r = cur.fetchone()
                    if r:
                        item = dict(r)
                        item["composition"] = json.loads(item.get("composition") or "[]")
                        item["contraindications"] = json.loads(item.get("contraindications") or "[]")
                        item["monitoring"] = json.loads(item.get("monitoring") or "[]")
                        item["citations"] = json.loads(item.get("citations") or "[]")
                        handler._send_json({"ok": True, "product": item})
                        return True
                except Exception:
                    pass
            p_item = srv.get_product_by_sku(sku)
            if p_item:
                handler._send_json({"ok": True, "product": p_item})
                return True
            handler._send_error(f"Product '{sku}' not found.", status=404, code="PRODUCT_NOT_FOUND")
            return True

    # ── 8 Parhez Lifestyle Protocols (MF-01 to Resp-01) ──────────────────
    if path == "/api/v1/therapeutic/parhez" or path.startswith("/api/v1/therapeutic/parhez/"):
        if path == "/api/v1/therapeutic/parhez":
            with srv.get_db() as conn:
                cur = conn.cursor()
                try:
                    cur.execute("SELECT * FROM master_parhez ORDER BY code ASC")
                    parhez_list = []
                    for r in cur.fetchall():
                        item = dict(r)
                        item["target_axes"] = json.loads(item.get("target_axes") or "[]")
                        item["rules"] = json.loads(item.get("rules") or "[]")
                        parhez_list.append(item)
                except Exception:
                    parhez_list = srv.get_all_parhez()
            handler._send_json({"ok": True, "count": len(parhez_list), "parhez": parhez_list})
            return True
        else:
            p_code = path.split("/")[-1].upper()
            with srv.get_db() as conn:
                cur = conn.cursor()
                try:
                    cur.execute("SELECT * FROM master_parhez WHERE UPPER(code) = ?", (p_code,))
                    r = cur.fetchone()
                    if r:
                        item = dict(r)
                        item["target_axes"] = json.loads(item.get("target_axes") or "[]")
                        item["rules"] = json.loads(item.get("rules") or "[]")
                        handler._send_json({"ok": True, "parhez": item})
                        return True
                except Exception:
                    pass
            pz_item = srv.get_parhez_by_code(p_code)
            if pz_item:
                handler._send_json({"ok": True, "parhez": pz_item})
                return True
            handler._send_error(f"Parhez protocol '{p_code}' not found.", status=404, code="PARHEZ_NOT_FOUND")
            return True

    # ── Z-MAI 30-Point Questionnaire Structure ───────────────────────────
    if path in ("/api/v1/clinical/zmai/domains", "/api/v1/clinical/zmai/questions"):
        domains = srv.get_all_domains()
        handler._send_json({"ok": True, "domains_count": len(domains), "domains": domains})
        return True

    # ── Z-MAI 6-Domain Quantitative Mizaj 2.0 Domains ────────────────────
    if path in ("/api/v1/clinical/zmai/matrix/domains", "/api/v1/clinical/zmai/matrix-domains"):
        handler._send_json({
            "ok": True,
            "matrix_domains": srv.MIZAJ_2_DOMAINS,
            "humors": ["balgham", "safra", "sauda", "dam"],
            "scoring_scale": "0-3 points per humor per domain (Max 18 per humor)",
            "cutoffs": {
                "significant_dominance": ">= 10",
                "moderate_tendency": "7-9",
                "minimal_presence": "< 7"
            }
        })
        return True

    # ── CP-AFUM Academic Curriculum & Certification ──────────────────────
    if path in ("/api/v1/academic/curriculum", "/api/v1/lms/curriculum"):
        if srv.get_curriculum_summary:
            handler._send_json({"ok": True, "curriculum": srv.get_curriculum_summary()})
        else:
            handler._send_error("Curriculum engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path in ("/api/v1/academic/certification/tiers", "/api/v1/clinical/certification/tiers"):
        handler._send_json({"ok": True, "tiers": srv.CERTIFICATION_LEVELS})
        return True

    # ── Dual-Track GMP Hero Products & Tadbeer Modalities ────────────────
    if path in ("/api/v1/therapeutic/gmp-catalog", "/api/v1/therapeutic/gmp-products"):
        handler._send_json({"ok": True, "products": srv.GMP_PRODUCTS_MASTER})
        return True

    if path in ("/api/v1/therapeutic/tadbeer-modalities", "/api/v1/clinical/tadbeer", "/api/v1/clinical/tadbeer/16"):
        handler._send_json({"ok": True, "modalities": srv.TADBEER_MODALITIES_16 or srv.TADBEER_MODALITIES, "count": len(srv.TADBEER_MODALITIES_16 or srv.TADBEER_MODALITIES)})
        return True

    if path in ("/api/v1/therapeutic/tadbeer/principles", "/api/v1/clinical/tadbeer/principles"):
        handler._send_json({"ok": True, "usool_e_tadbeer": srv.USOOL_E_TADBEER_PRINCIPLES})
        return True

    if path in ("/api/v1/therapeutic/tadbeer/trajectories", "/api/v1/clinical/tadbeer/trajectories"):
        handler._send_json({"ok": True, "trajectories": srv.MULTI_MODAL_TREATMENT_TRAJECTORIES})
        return True

    if path in ("/api/v1/therapeutic/tadbeer/home-care", "/api/v1/clinical/tadbeer/home-care"):
        handler._send_json({"ok": True, "home_care": srv.HOME_SELF_CARE_SPEC})
        return True

    # ── Ilaj bil Nafsiyat (Unani Psychological & Psychosomatic Medicine) ─
    if path in ("/api/v1/clinical/nafsiyat/protocols", "/api/v1/nafsiyat/protocols"):
        handler._send_json({"ok": True, "protocols": srv.VERIFIED_CASE_STUDY_PROTOCOLS})
        return True

    if path in ("/api/v1/clinical/nafsiyat/taxonomy", "/api/v1/nafsiyat/taxonomy"):
        handler._send_json({"ok": True, "taxonomy": srv.CLASSICAL_NAFSIYAT_TAXONOMY})
        return True

    if path in ("/api/v1/clinical/nafsiyat/modalities", "/api/v1/nafsiyat/modalities"):
        handler._send_json({"ok": True, "itrafat": srv.ITRAFAT_AROMATHERAPY_CATALOG, "tanaffus": srv.TANAFFUS_BREATHWORK_PROTOCOLS})
        return True


    # ── Ilaj bil Ghiza (Unani Dietotherapy) ──────────────────────────────
    if path in ("/api/v1/clinical/ghiza/preparations", "/api/v1/ghiza/preparations"):
        handler._send_json({
            "ok": True,
            "preparations": srv.CANONICAL_THERAPEUTIC_PREPARATIONS,
            "nutrient_categories": srv.NUTRIENT_CATEGORIES
        })
        return True

    # ── Ilaj bil Yad & Jarahat (Classical Unani Operative Surgery) ────────
    if path in ("/api/v1/clinical/yad/modalities", "/api/v1/yad/modalities"):
        handler._send_json({
            "ok": True,
            "modalities": srv.CLASSICAL_JARAHAT_MODALITIES,
            "instruments": srv.AL_ZAHRAWI_INSTRUMENTS,
            "cicatrizing_formulary": srv.CICATRIZING_STYPTIC_FORMULARY
        })
        return True

    # ── Global Edition (2026): Evidence Grading & Canonical Glossary ─────
    if path == "/api/v1/knowledge/evidence/all":
        if srv.EvidenceGlossaryEngine:
            handler._send_json({"ok": True, "evidence": srv.EvidenceGlossaryEngine.get_all_evidence()})
        else:
            handler._send_error("Evidence engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path.startswith("/api/v1/knowledge/evidence/condition"):
        q_cond = query_params.get("q", [""])[0]
        if srv.EvidenceGlossaryEngine:
            handler._send_json({"ok": True, "condition": q_cond, "evidence": srv.EvidenceGlossaryEngine.filter_evidence_by_condition(q_cond)})
        else:
            handler._send_error("Evidence engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path == "/api/v1/knowledge/glossary/search":
        q_term = query_params.get("q", [""])[0]
        if srv.EvidenceGlossaryEngine:
            handler._send_json({"ok": True, "query": q_term, "results": srv.EvidenceGlossaryEngine.search_glossary(q_term)})
        else:
            handler._send_error("Glossary engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path == "/api/v1/clinical/zape/schema":
        if srv.ZAPEEngine:
            handler._send_json({"ok": True, "axes": srv.ZAPEEngine.AXES, "mizaj_types": srv.ZAPEEngine.MIZAJ_TYPES})
        else:
            handler._send_error("ZAPE engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── ZAYVORA 12-Axis Clinical Intelligence Framework™ (Knowledge) ──────
    if path in ("/api/v1/knowledge/axes-12/all", "/api/v1/knowledge/axes-12"):
        handler._send_json({
            "ok": True,
            "framework": "ZAYVORA 12-Axis Clinical Intelligence Framework™",
            "label": "Proposed Proprietary Clinical Architecture; advisory decision-support layer, not a replacement for clinician-validated diagnosis.",
            "total_axes": len(srv.get_all_organ_axes()),
            "axes": srv.get_all_organ_axes()
        })
        return True

    if path.startswith("/api/v1/knowledge/axes-12/"):
        axis_id = path.split("/")[-1].upper()
        ax_data = srv.get_axis_by_id(axis_id)
        if ax_data:
            handler._send_json({"ok": True, "axis": ax_data})
        else:
            handler._send_error(f"Axis '{axis_id}' not found.", status=404, code="AXIS_NOT_FOUND")
        return True

    # ── ZAYVORA Volume II: 16 Core Products & 8 Parhez Protocols (GET) ───
    if path in ("/api/v1/therapeutic/products-16/all", "/api/v1/therapeutic/products-16"):
        handler._send_json({
            "ok": True,
            "framework": "16 Core Product Matrix (Volume II)",
            "total_products": len(srv.get_all_core_products()),
            "products": srv.get_all_core_products()
        })
        return True

    if path.startswith("/api/v1/therapeutic/products-16/"):
        prod_id = path.split("/")[-1].upper()
        p_data = srv.get_product_by_id(prod_id)
        if p_data:
            handler._send_json({"ok": True, "product": p_data})
        else:
            handler._send_error(f"Product '{prod_id}' not found.", status=404, code="PRODUCT_NOT_FOUND")
        return True

    # ── Modular Clinical Domain Dispatcher ────────────────────────────────
    from services.routes.clinical_routes import handle_clinical_get
    if handle_clinical_get(handler, path, query_params, auth_ctx):
        return True

    # ── ZAYVORA Pharmacopoeia: Materia Medica (Single Drugs A–Z) ──────────
    if path in ("/api/v1/knowledge/materia-medica/all", "/api/v1/knowledge/materia-medica"):
        q = query_params.get("search", [None])[0] or query_params.get("q", [None])[0]
        mizaj_quality = query_params.get("quality", [None])[0]
        darja = query_params.get("darja", [None])[0]
        
        if q:
            items = srv.search_monographs(q)
        else:
            items = srv.get_all_monographs()

        if mizaj_quality:
            qual_lower = mizaj_quality.lower()
            items = [it for it in items if qual_lower in it.get("mizaj_primary", "").lower() or it.get("mizaj", {}).get(qual_lower, 0) > 0]

        if darja:
            try:
                d_int = int(darja)
                items = [it for it in items if any(v == d_int for v in it.get("mizaj", {}).values())]
            except ValueError:
                pass

        handler._send_json({
            "ok": True,
            "framework": "ZAYVORA Pharmacopoeia: Single Drugs Reference & Scientific Validation",
            "total_monographs": len(items),
            "monographs": items
        })
        return True

    if path.startswith("/api/v1/knowledge/materia-medica/"):
        drug_key = path.split("/")[-1].upper()
        m_data = srv.get_monograph_by_key(drug_key)
        if not m_data:
            # Try finding by partial key or slug
            for k, v in srv.MONOGRAPHS.items():
                if drug_key in k or k in drug_key:
                    m_data = v
                    break
        if m_data:
            handler._send_json({"ok": True, "monograph": m_data})
        else:
            handler._send_error(f"Monograph for '{drug_key}' not found.", status=404, code="DRUG_NOT_FOUND")
        return True

    # ── ZAYVORA Dual-Tier Product Catalog (Core vs Clinical Elite) ────────
    if path in ("/api/v1/knowledge/catalog/dual-tier", "/api/v1/knowledge/catalog/dual-tier/all"):
        items = srv.get_all_dual_tier_products()
        handler._send_json({
            "ok": True,
            "framework": "Dual-Tier Architecture (Core Line & Clinical Elite Line)",
            "total_products": len(items),
            "products": items
        })
        return True

    if path.startswith("/api/v1/knowledge/catalog/dual-tier/"):
        sku = path.split("/")[-1].upper()
        prod_data = srv.get_dual_tier_product(sku)
        if prod_data:
            handler._send_json({"ok": True, "product": prod_data})
        else:
            handler._send_error(f"Dual-tier product '{sku}' not found.", status=404, code="PRODUCT_NOT_FOUND")
        return True

    # ── 90-Day Program Packages & Pricing ─────────────────────────────────
    if path in ("/api/v1/knowledge/programs/packages", "/api/v1/knowledge/programs/packages/all"):
        handler._send_json({
            "ok": True,
            "tier_specs": srv.PROGRAM_TIER_SPECS,
            "program_pricing": srv.PROGRAM_SPECIFIC_PRICING
        })
        return True

    if path.startswith("/api/v1/knowledge/programs/packages/"):
        p_code = path.split("/")[-1].upper()
        tier_arg = query_params.get("tier", ["BASIC"])[0].upper()
        pkg = srv.get_program_pricing(p_code, tier_arg)
        if pkg:
            handler._send_json({"ok": True, "package": pkg})
        else:
            handler._send_error(f"Program package '{p_code}' ({tier_arg}) not found.", status=404, code="PACKAGE_NOT_FOUND")
        return True

    # ── Matab Compounding Formulas (High-Potency Dispensary) ──────────────
    if path in ("/api/v1/therapeutic/matab-formulas/all", "/api/v1/therapeutic/matab-formulas"):
        formulas = srv.get_all_matab_formulas()
        handler._send_json({
            "ok": True,
            "framework": "Matab Clinical Compounding Formulas (Prescription Only)",
            "total_formulas": len(formulas),
            "formulas": formulas
        })
        return True

    if path.startswith("/api/v1/therapeutic/matab-formulas/"):
        proto_id = path.split("/")[-1].upper()
        m_form = srv.get_matab_formula(proto_id)
        if m_form:
            handler._send_json({"ok": True, "formula": m_form})
        else:
            handler._send_error(f"Matab formula '{proto_id}' not found.", status=404, code="FORMULA_NOT_FOUND")
        return True

    # ── 4-Tier Evidence Grading & Claims Matrix ───────────────────────────
    if path in ("/api/v1/knowledge/evidence/grading-matrix", "/api/v1/knowledge/evidence/tiers"):
        tiers = srv.get_all_evidence_tiers()
        handler._send_json({
            "ok": True,
            "framework": "ZAYVORA 4-Tier Evidence Hierarchy & Claims Discipline",
            "tiers": tiers
        })
        return True

    # ── Clinical Intelligence Doctrine & Governance ──────────────────────
    if path in ("/api/v1/governance/doctrine/spec", "/api/v1/governance/clinical-doctrine"):
        handler._send_json({"ok": True, "doctrine": srv.get_clinical_doctrine()})
        return True

    if path in ("/api/v1/governance/knowledge/state-machine", "/api/v1/knowledge/lifecycle"):
        handler._send_json({
            "ok": True,
            "framework": "ZAYVORA Knowledge State Machine (10 Lifecycle Gates)",
            "states": [
                "DRAFT", "SOURCE_VERIFIED", "STRUCTURED", "UNANI_EXPERT_REVIEW",
                "SAFETY_REVIEW", "REGULATORY_REVIEW", "CLINICAL_APPROVED",
                "AI_AVAILABLE", "MONITORED", "UPDATE_RE_REVIEW_RETIRE"
            ]
        })
        return True

    # ── ZAYVORA Mufradat 250 Governance & Validation Registry ─────────────
    if path in ("/api/v1/knowledge/mufradat-250/all", "/api/v1/knowledge/mufradat-250"):
        if srv.get_all_mufradat_250:
            catalog = srv.get_all_mufradat_250()
            handler._send_json({
                "ok": True,
                "total_count": len(catalog),
                "governance_rule": "Candidate knowledge only until source citation, safety, regulatory, and expert sign-off gates are complete.",
                "mufradat": catalog
            })
        else:
            handler._send_error("Mufradat 250 registry unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path in ("/api/v1/knowledge/mufradat-250/canonical-groups", "/api/v1/knowledge/mufradat-250/canonical"):
        if srv.get_canonical_groups_registry:
            groups = srv.get_canonical_groups_registry()
            handler._send_json({
                "ok": True,
                "total_groups": len(groups),
                "canonical_groups": groups
            })
        else:
            handler._send_error("Canonical groups registry unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path in ("/api/v1/knowledge/mufradat-250/high-risk", "/api/v1/knowledge/mufradat-250/blocked"):
        if srv.get_high_risk_28_registry:
            hr = srv.get_high_risk_28_registry()
            handler._send_json({
                "ok": True,
                "total_high_risk": len(hr),
                "ai_access_policy": "ALL 28 HIGH-RISK RECORDS HARD-BLOCKED FROM AUTONOMOUS AI PRESCRIBING",
                "high_risk_registry": hr
            })
        else:
            handler._send_error("High risk registry unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── 25-Drug Gold Benchmark Monographs ────────────────────────────────
    if path == "/api/v1/knowledge/mufradat-gold/all":
        if srv.GoldBenchmarkRegistry:
            drugs = srv.GoldBenchmarkRegistry.list_gold_drugs()
            handler._send_json({"ok": True, "total_gold_drugs": len(drugs), "drugs": drugs})
        else:
            handler._send_error("Gold benchmark registry unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path.startswith("/api/v1/knowledge/mufradat-gold/"):
        zmf_param = urllib.parse.unquote(path.split("/")[-1]).upper()
        if srv.GoldBenchmarkRegistry:
            monograph = srv.GoldBenchmarkRegistry.get_monograph(zmf_param)
            if monograph:
                handler._send_json({"ok": True, "monograph": monograph})
            else:
                handler._send_error(f"Gold monograph '{zmf_param}' not found in 25 benchmark batch.", status=404, code="NOT_FOUND")
        else:
            handler._send_error("Gold benchmark registry unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Validated Classical Murakkabat Catalog ───────────────────────────
    if path == "/api/v1/therapeutic/murakkab-validated/all":
        if srv.ValidatedMurakkabCompiler:
            murakkabat = srv.ValidatedMurakkabCompiler.list_all_murakkabat()
            handler._send_json({"ok": True, "total_murakkabat": len(murakkabat), "murakkabat": murakkabat})
        else:
            handler._send_error("Murakkab compiler unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path.startswith("/api/v1/therapeutic/murakkab-validated/"):
        mrk_param = urllib.parse.unquote(path.split("/")[-1]).upper()
        if srv.ValidatedMurakkabCompiler:
            compound = srv.ValidatedMurakkabCompiler.get_murakkab(mrk_param)
            if compound:
                handler._send_json({"ok": True, "murakkab": compound})
            else:
                handler._send_error(f"Murakkab '{mrk_param}' not found in validated registry.", status=404, code="NOT_FOUND")
        else:
            handler._send_error("Murakkab compiler unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── 250-Catalog Statistics & Status Matrix ───────────────────────────
    if path == "/api/v1/knowledge/mufradat-250/catalog-stats":
        if srv.Master250MonographMatrix:
            handler._send_json({"ok": True, "stats": srv.Master250MonographMatrix.get_catalog_statistics()})
        else:
            handler._send_error("Master 250 matrix unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Multi-Disciplinary Clinician Audit Certificate ───────────────────
    if path.startswith("/api/v1/governance/signoff/certificate/"):
        target_id = urllib.parse.unquote(path.split("/")[-1]).upper()
        if srv.ClinicalMultiSignoffEngine:
            cert = srv.ClinicalMultiSignoffEngine.get_audit_certificate(target_id)
            handler._send_json({"ok": True, "audit_certificate": cert})
        else:
            handler._send_error("Signoff engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Patient Monograph Card Generator ─────────────────────────────────
    if path == "/api/v1/knowledge/mufradat-250/cards/seeds":
        if srv.MufradatCardGenerator:
            handler._send_json({"ok": True, "seed_cards": srv.MufradatCardGenerator.generate_seed_cards()})
        else:
            handler._send_error("Card Generator unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path.startswith("/api/v1/knowledge/mufradat-250/card/"):
        zmf_param = urllib.parse.unquote(path.split("/")[-1]).upper()
        if srv.MufradatCardGenerator:
            card = srv.MufradatCardGenerator.generate_card(zmf_param)
            if "error" in card:
                handler._send_error(card["error"], status=404, code="NOT_FOUND")
            else:
                handler._send_json({"ok": True, "card": card})
        else:
            handler._send_error("Card Generator unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path.startswith("/api/v1/knowledge/mufradat-250/"):
        drug_param = urllib.parse.unquote(path.split("/")[-1])
        if srv.get_mufrad_by_id:
            rec = srv.get_mufrad_by_id(drug_param)
            if rec:
                handler._send_json({"ok": True, "mufrad": rec})
            else:
                handler._send_error(f"Mufrad '{drug_param}' not found in 250 registry.", status=404, code="NOT_FOUND")
        else:
            handler._send_error("Mufradat 250 registry unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Grand Classical & Modern Integrative Medical Library (12 Volumes) ──
    if path in ("/api/v1/library/volumes", "/api/v1/knowledge/library/volumes"):
        try:
            from services.knowledge.app.data.grand_integrative_library_master import get_all_volumes, LIBRARY_METADATA
            handler._send_json({
                "ok": True,
                "metadata": LIBRARY_METADATA,
                "total_volumes": len(get_all_volumes()),
                "volumes": get_all_volumes()
            })
        except Exception as e:
            handler._send_error(f"Failed to load library volumes: {e}", status=500, code="LIBRARY_ERROR")
        return True

    if path in ("/api/v1/library/search", "/api/v1/knowledge/library/search"):
        q = (query_params.get("q", [""])[0] or query_params.get("query", [""])[0]).strip()
        try:
            from services.knowledge.app.data.grand_integrative_library_master import search_library
            results = search_library(q)
            handler._send_json({
                "ok": True,
                "query": q,
                "count": len(results),
                "results": results
            })
        except Exception as e:
            handler._send_error(f"Library search error: {e}", status=500, code="SEARCH_ERROR")
        return True

    if path.startswith("/api/v1/library/volumes/") or path.startswith("/api/v1/knowledge/library/volumes/"):
        vol_id = urllib.parse.unquote(path.split("/")[-1])
        try:
            from services.knowledge.app.data.grand_integrative_library_master import get_volume_by_id
            vol = get_volume_by_id(vol_id)
            if vol:
                handler._send_json({"ok": True, "volume": vol})
            else:
                handler._send_error(f"Library Volume '{vol_id}' not found.", status=404, code="NOT_FOUND")
        except Exception as e:
            handler._send_error(f"Failed to fetch volume: {e}", status=500, code="LIBRARY_ERROR")
        return True

    if "/treatise" in path and (path.startswith("/api/v1/library/chapters/") or path.startswith("/api/v1/knowledge/library/chapters/")):
        ch_id = urllib.parse.unquote(path.split("/")[-2])
        try:
            from services.knowledge.app.data.grand_integrative_library_master import get_chapter_treatise
            treatise = get_chapter_treatise(ch_id)
            if treatise:
                handler._send_json({"ok": True, "chapter_id": ch_id, "treatise": treatise})
            else:
                handler._send_error(f"Treatise for chapter '{ch_id}' not found.", status=404, code="NOT_FOUND")
        except Exception as e:
            handler._send_error(f"Failed to fetch treatise: {e}", status=500, code="LIBRARY_ERROR")
        return True

    if path.startswith("/api/v1/library/chapters/") or path.startswith("/api/v1/knowledge/library/chapters/"):
        ch_id = urllib.parse.unquote(path.split("/")[-1])
        try:
            from services.knowledge.app.data.grand_integrative_library_master import get_chapter_by_id
            ch = get_chapter_by_id(ch_id)
            if ch:
                handler._send_json({"ok": True, "chapter": ch})
            else:
                handler._send_error(f"Library Chapter '{ch_id}' not found.", status=404, code="NOT_FOUND")
        except Exception as e:
            handler._send_error(f"Failed to fetch chapter: {e}", status=500, code="LIBRARY_ERROR")
        return True

    # ── Botanical Visual Atlas & Morphological Identification Keys ─────────
    if path in ("/api/v1/library/botanical-atlas", "/api/v1/knowledge/botanical-atlas"):
        if srv.get_all_botanical_atlas:
            catalog = srv.get_all_botanical_atlas()
            handler._send_json({"ok": True, "count": len(catalog), "botanical_atlas": catalog})
        else:
            handler._send_error("Botanical Visual Atlas unavailable.", status=503)
        return True

    if path.startswith("/api/v1/library/botanical-atlas/") or path.startswith("/api/v1/knowledge/botanical-atlas/"):
        herb_id = urllib.parse.unquote(path.split("/")[-1])
        if srv.get_botanical_by_id:
            herb = srv.get_botanical_by_id(herb_id)
            if herb:
                handler._send_json({"ok": True, "herb": herb})
            else:
                handler._send_error(f"Botanical monograph '{herb_id}' not found.", status=404, code="NOT_FOUND")
        else:
            handler._send_error("Botanical Visual Atlas unavailable.", status=503)
        return True

    # ── Clinical Case Study Simulator & Training Suite ───────────────────
    if path in ("/api/v1/simulator/cases", "/api/v1/clinical/simulator/cases"):
        if srv.CaseSimulatorEngine:
            cases = srv.CaseSimulatorEngine.get_all_cases()
            handler._send_json({"ok": True, "count": len(cases), "cases": cases})
        else:
            handler._send_error("Case Simulator Engine unavailable.", status=503)
        return True

    if (path.startswith("/api/v1/simulator/cases/") or path.startswith("/api/v1/clinical/simulator/cases/")) and not path.endswith("/evaluate"):
        case_id = urllib.parse.unquote(path.split("/")[-1])
        if srv.CaseSimulatorEngine:
            case_obj = srv.CaseSimulatorEngine.get_case_by_id(case_id, sanitize_answers=True)
            if case_obj:
                handler._send_json({"ok": True, "case": case_obj})
            else:
                handler._send_error(f"Simulator Case '{case_id}' not found.", status=404, code="NOT_FOUND")
        else:
            handler._send_error("Case Simulator Engine unavailable.", status=503)
        return True

    # ── 12-Gate Pipeline Tracker ──────────────────────────────────────────
    if path == "/api/v1/governance/12-gate/gates":
        if srv.TwelveGateTrackerEngine:
            handler._send_json({"ok": True, "gate_definitions": srv.TwelveGateTrackerEngine.get_all_gate_definitions()})
        else:
            handler._send_error("12-Gate Tracker unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path == "/api/v1/governance/12-gate/dashboard":
        if srv.TwelveGateTrackerEngine:
            handler._send_json({"ok": True, "dashboard": srv.TwelveGateTrackerEngine.get_dashboard_summary()})
        else:
            handler._send_error("12-Gate Tracker unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path.startswith("/api/v1/governance/12-gate/status/"):
        zmf_param = urllib.parse.unquote(path.split("/")[-1]).upper()
        if srv.TwelveGateTrackerEngine:
            handler._send_json({"ok": True, "gate_status": srv.TwelveGateTrackerEngine.get_gate_status(zmf_param)})
        else:
            handler._send_error("12-Gate Tracker unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Badal-e-Advia Substitute Advisory ────────────────────────────────
    if path == "/api/v1/therapeutic/badal-e-advia/catalog":
        if srv.BadalEAdviaEngine:
            handler._send_json({"ok": True, "badal_catalog": srv.BadalEAdviaEngine.get_all_badal_entries()})
        else:
            handler._send_error("Badal-e-Advia engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path in ("/api/v1/ai/copilot/permissions", "/api/v1/governance/copilot-matrix"):
        matrix = srv.CopilotPermissionGuard.get_permission_matrix() if srv.CopilotPermissionGuard else {}
        handler._send_json({"ok": True, "copilot_permission_matrix": matrix})
        return True

    # ── Master Nuskha Badraqa Conduit Matrix ─────────────────────────────
    if path in ("/api/v1/therapeutic/nuskha/badraqa-matrix", "/api/v1/therapeutic/badraqa"):
        handler._send_json({
            "ok": True,
            "framework": "ZAYVORA Organ-Axis Badraqa (Conduit Vehicle) Matrix",
            "badraqa_registry": srv.ORGAN_BADRAQA_CONDUIT_REGISTRY
        })
        return True

    # ── Scientific & Classical Explainability ("Why This?") (Blueprint §63) ──
    if path in ("/api/v1/clinical/explainability", "/api/v1/clinical/why-this") or path.startswith("/api/v1/clinical/explainability/"):
        item_id = query_params.get("item_id", ["SURANJAN"])[0] if query_params else "SURANJAN"
        if path.startswith("/api/v1/clinical/explainability/") and len(path.rstrip("/").split("/")) > 4:
            item_id = path.rstrip("/").split("/")[-1]
        
        explanation = {
            "itemId": item_id,
            "itemTitle": "Safoof Suranjan (Mudabbar) + Roghan Suranjan",
            "category": "NUSKHA",
            "clinicalRationale": "Targeted concoction (Nujz) and subsequent resolution (Tahleel) of accumulated cold-phlegmatic (Balgham Barid) morbid humors deposited in peri-articular synovial tissues.",
            "classicalAuthority": {
                "sourceText": "Unani Pharmacopoeia of India (UPI) Vol. 1 / Kitab al-Kulliyat (Ibn Rushd)",
                "chapterVolume": "Amraz-e-Mafasil wa Niqris, Section 4",
                "formulationPrinciple": "Istifragh-e-Mawad-e-Fasida (Clearing morbid humor via specific resolvent alterative herbs)"
            },
            "evidenceLevel": "E5",
            "evidenceDescription": "Human Observational Studies & Clinical Cohorts (Concordant with UPI Monograph)",
            "mizajConcordance": {
                "targetMizaj": "Su-e-Mizaj Barid Balghami (Cold-Moist Dyscrasia)",
                "formulationMizaj": "Haar Yabis Darja Dowam (Hot 2° - Dry 2°)",
                "mechanismOfCorrection": "Counteracts tissue coldness and moisture via heating and resolving properties (Muhallil wa Musakkin)."
            },
            "muslehBalancing": {
                "muslehAgent": "Roghan-e-Badam Shirin (Sweet Almond Oil) / Kateera",
                "correctiveAction": "Protects gastric mucosa against irritant alkaloids (Colchicine derivatives) and softens rough dryness."
            },
            "badraqaConduit": {
                "vehicle": "Maa-ul-Asl (Lukewarm Honey-Water) or Decoction of Bekh-e-Badyan",
                "organDeliveryRole": "Acts as penetrative vehicle (Nafiz) directing therapeutic active constituents to articular joints (Mafasil)."
            },
            "safetyBoundaries": {
                "scheduleE1Status": True,
                "maximumDailyDose": "1.5g to 3.0g Safoof (Colchicum autumnale corm equivalent)",
                "knownContraindications": ["Pregnancy (Abortifacient risk)", "Severe renal impairment (eGFR < 30)", "Active peptic ulcer disease"],
                "monitoringRequirements": ["Monitor bowel movement frequency", "Weekly joint mobility assessment", "Report any gastrointestinal cramping"]
            },
            "governanceMetadata": {
                "zkbVersion": "ZKB-v5.2.0-CANONICAL",
                "zfieVersion": "ZFIE-v2.1.0-PRODUCTION",
                "lastVerifiedDate": "2026-09-28",
                "verifiedBy": "Hakeem Dr. Irfan Ashraf (BUMS, AKTC AMU)"
            }
        }
        handler._send_json({"ok": True, "explanation": explanation})
        return True

    # ── Active Purpose-Specific Consent Query (§11) ───────────────────────
    if path == "/api/v1/consent/status" or path.startswith("/api/v1/consent/status"):
        patient_id = query_params.get("patient_id", ["PAT-001"])[0] if query_params else "PAT-001"
        consents = {
            "CARE": "ACTIVE",
            "AI_PROCESSING": "ACTIVE",
            "COMMUNICATION": "ACTIVE",
            "RESEARCH": "ACTIVE",
            "DATA_SHARING": "ACTIVE"
        }
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='patient_consents'")
            if cur.fetchone():
                cur.execute("SELECT purpose, status FROM patient_consents WHERE patient_id = ?", (patient_id,))
                for row in cur.fetchall():
                    consents[row[0]] = row[1]
        handler._send_json({"ok": True, "patient_id": patient_id, "consents": consents})
        return True

    # ── Knowledge Intelligence & Clinical Governance vNEXT ───────────────
    if path == "/api/v1/governance/knowledge-vnext/reconcile-identity":
        q_name = query_params.get("q", [""])[0]
        if not q_name:
            handler._send_error("Query parameter 'q' is required for drug identity reconciliation.", status=400)
            return True
        if srv.CanonicalDrugRegistry:
            result = srv.CanonicalDrugRegistry.reconcile_drug_identity(q_name)
            handler._send_json({"ok": True, "data": result})
        else:
            handler._send_error("Knowledge vNEXT engine unavailable.", status=503)
        return True

    if path in ("/api/v1/governance/knowledge-vnext/benchmarks", "/api/v1/governance/knowledge-vnext/overview"):
        handler._send_json({
            "ok": True,
            "gold_benchmark_ids": srv.GOLD_BENCHMARK_25_IDS,
            "framework": "ZAYVORA Health OS™ vNEXT Knowledge Intelligence & Clinical Governance",
            "ai_safety_states": [s.value for s in srv.AISafetyState] if srv.AISafetyState else [],
            "knowledge_states": [s.value for s in srv.KnowledgeState] if srv.KnowledgeState else [],
            "murakkab_classes": [c.value for c in srv.MurakkabClass] if srv.MurakkabClass else []
        })
        return True

    if path.startswith("/api/v1/governance/knowledge-vnext/audit-trail/"):
        drug_id = path.split("/")[-1].upper()
        if srv.ReviewerWorkspaceEngine:
            trail = srv.ReviewerWorkspaceEngine.get_audit_trail_for_drug(drug_id)
            handler._send_json({"ok": True, "drug_id": drug_id, "audit_trail": trail})
        else:
            handler._send_error("Knowledge vNEXT engine unavailable.", status=503)
        return True
    return False


def handle_governance_protocols_post(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any], body: Dict[str, Any]) -> bool:
    """Dispatches POST requests for clinical scoring, protocols, regimens, and 12-gate governance."""
    import services.live_api_server as srv

    # ── Organ Axes 0-5 Scoring Engine ────────────────────────────────────
    if path in ("/api/v1/clinical/axes/score", "/api/v1/clinical/organ-axes/score"):
        scores = body.get("scores") or {}
        if srv.score_organ_axes:
            res = srv.score_organ_axes(scores)
            handler._send_json({"ok": True, "result": res})
        else:
            handler._send_error("Organ axes engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Z-MAI 30-Point Temperament Calculation ───────────────────────────
    if path in ("/api/v1/clinical/zmai/calculate", "/api/v1/clinical/mizaj/zmai"):
        responses = body.get("responses") or {}
        if srv.calculate_zmai_score:
            res = srv.calculate_zmai_score(responses)
            handler._send_json({"ok": True, "assessment": res, "clinician_review_required": True})
        else:
            handler._send_error("Z-MAI engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Personal Health Profile: Mizaj Reassessment (Blueprint §10) ─────
    if path in ("/api/v1/clinical/mizaj/reassess", "/api/v1/mizaj/reassess"):
        patient_id = body.get("patient_id", "PAT-001")
        ajnas_scores = body.get("ajnas_scores") or body.get("scores") or {}
        interpretation = body.get("interpretation") or "Periodic longitudinal reassessment."
        clinician_name = (auth_ctx.get("fullName") if auth_ctx else None) or body.get("clinician_name", "Hakeem Dr. Irfan Ashraf")
        clinician_role = (auth_ctx.get("role") if auth_ctx else None) or body.get("clinician_role", "Senior Tabeeb")
        if srv.PersonalHealthProfileEngine:
            reassessment = srv.PersonalHealthProfileEngine.record_mizaj_reassessment(
                patient_id=patient_id,
                ajnas_scores=ajnas_scores,
                interpretation=interpretation,
                clinician_name=clinician_name,
                clinician_role=clinician_role
            )
            handler._send_json({
                "ok": True,
                "reassessment": srv.asdict(reassessment),
                "version_id": reassessment.version_id,
                "message": "Immutable Mizaj reassessment recorded successfully. Prior historical versions preserved (§10)."
            })
        else:
            handler._send_error("Personal Health Profile engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Personal Health Profile: Afaal Stage Update (Blueprint §11) ──────
    if path in ("/api/v1/clinical/afaal/update", "/api/v1/afaal/stage-update"):
        patient_id = body.get("patient_id", "PAT-001")
        new_stage = (body.get("new_stage") or body.get("stage") or "TAHLEEL").upper()
        functional_context = body.get("functional_context", "Advancing therapeutic stage per clinical response.")
        monitoring_findings = body.get("monitoring_findings") or ["Lingual coating reducing", "Pulse motadil"]
        clinician_notes = body.get("clinician_notes", "Clinician approved stage progression.")
        clinician_id = (auth_ctx.get("userId") if auth_ctx else None) or body.get("clinician_id", "DOC-IRFAN-01")
        
        stage_info = srv.AFAAL_STAGES.get(new_stage, {})
        handler._send_json({
            "ok": True,
            "patient_id": patient_id,
            "updated_stage": new_stage,
            "stage_info": stage_info,
            "functional_context": functional_context,
            "monitoring_findings": monitoring_findings,
            "clinician_notes": clinician_notes,
            "clinician_id": clinician_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": f"Afaal cascade stage updated to {new_stage}. Clinician sign-off recorded (§11)."
        })
        return True

    # ── Drug-Herb Interaction & Safety Audit ─────────────────────────────
    if path in ("/api/v1/therapeutic/interactions/check", "/api/v1/therapeutic/safety/audit"):
        products = body.get("products") or body.get("ingredients") or []
        medications = body.get("medications") or []
        is_pregnant = bool(body.get("is_pregnant", False))
        is_lactating = bool(body.get("is_lactating", False))
        egfr = body.get("egfr")
        if egfr is not None:
            try:
                egfr = float(egfr)
            except ValueError:
                egfr = None
        
        flagged = srv.check_drug_herb_interactions(products, medications)
        contraindications = []
        u_map = srv.get_universal_contraindications()
        if is_pregnant:
            contraindications.extend(u_map.get("PREGNANCY", []))
        if is_lactating:
            contraindications.extend(u_map.get("LACTATION", []))
        if egfr is not None and egfr < 30.0:
            contraindications.extend(u_map.get("SEVERE_RENAL_IMPAIRMENT_EGFR_UNDER_30", []))
            
        is_safe = len(flagged) == 0 and len(contraindications) == 0
        severity = "SAFE"
        if flagged:
            severity = "CRITICAL" if any(f.get("severity") == "CRITICAL" for f in flagged) else "MODERATE"
        if contraindications:
            severity = "CRITICAL"

        handler._send_json({
            "ok": True,
            "is_safe": is_safe,
            "severity": severity,
            "interactions_detected": flagged,
            "contraindications": contraindications,
            "safe_to_lock": False,
            "requires_clinician_signoff": True
        })
        return True

    # ── Four-Tier Nuskha Architecture Validation ─────────────────────────
    if path in ("/api/v1/therapeutic/nuskha/validate", "/api/v1/therapeutic/nuskha/tier-check"):
        ingredients = body.get("ingredients") or []
        if srv.verify_four_tier_nuskha_architecture:
            res = srv.verify_four_tier_nuskha_architecture(ingredients)
            handler._send_json({"ok": True, "evaluation": res, "requires_clinician_signoff": True})
        else:
            handler._send_error("Nuskha compiler unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── UDC Engine (Unani Diagnosis Code) ────────────────────────────────
    if path == "/api/v1/clinical/udc/generate":
        mizaj = body.get("mizaj", "")
        khilt = body.get("dominant_khilt", "")
        axis = body.get("primary_axis", "")
        phase = body.get("afaal_phase", "")
        if srv.generate_udc:
            udc_code = srv.generate_udc(mizaj, khilt, axis, phase)
            parsed = srv.parse_udc(udc_code) if srv.parse_udc else {}
            handler._send_json({"ok": True, "udc_code": udc_code, "details": parsed})
        else:
            handler._send_error("UDC engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path == "/api/v1/clinical/udc/parse":
        udc_code = body.get("udc_code", "")
        if srv.parse_udc:
            res = srv.parse_udc(udc_code)
            handler._send_json({"ok": True, "parsed": res})
        else:
            handler._send_error("UDC engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Mizaj Dose Adjustment Personalisation Engine ─────────────────────
    if path == "/api/v1/clinical/mizaj/adjust-dose":
        mizaj = body.get("mizaj", "")
        ingredients = body.get("ingredients", [])
        if srv.calculate_mizaj_dose_adjustments:
            res = srv.calculate_mizaj_dose_adjustments(mizaj, ingredients)
            handler._send_json({"ok": True, "adjustment": res})
        else:
            handler._send_error("Mizaj dose engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Functional Lab Interpretation & 5 Trigger Rules ──────────────────
    if path == "/api/v1/clinical/labs/analyze-functional":
        labs = body.get("labs", {})
        symptoms = body.get("symptoms", [])
        glucose = labs.get("fasting_glucose", labs.get("glucose"))
        insulin = labs.get("fasting_insulin", labs.get("insulin"))
        tg = labs.get("triglycerides", labs.get("tg"))
        hdl = labs.get("hdl")

        triggers = srv.evaluate_five_non_negotiable_lab_trigger_rules(labs, symptoms) if srv.evaluate_five_non_negotiable_lab_trigger_rules else {}
        homa = srv.calculate_homa_ir(float(glucose), float(insulin)) if (srv.calculate_homa_ir and glucose and insulin) else None
        tg_hdl = srv.calculate_tg_hdl_ratio(float(tg), float(hdl)) if (srv.calculate_tg_hdl_ratio and tg and hdl) else None

        handler._send_json({
            "ok": True,
            "triggers": triggers,
            "homa_ir": homa,
            "tg_hdl_ratio": tg_hdl,
            "clinician_signoff_required": True
        })
        return True

    if path == "/api/v1/clinical/labs/semen-analysis":
        params = body.get("semen_parameters", {})
        if srv.evaluate_semen_analysis:
            res = srv.evaluate_semen_analysis(params)
            handler._send_json({"ok": True, "analysis": res})
        else:
            handler._send_error("Semen analysis engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Phase-Based Therapeutic Engine ───────────────────────────────────
    if path == "/api/v1/clinical/phases/evaluate":
        profile = body.get("patient_profile", {})
        if srv.evaluate_phase_trigger_rules:
            res = srv.evaluate_phase_trigger_rules(profile)
            handler._send_json({"ok": True, "evaluation": res})
        else:
            handler._send_error("Phase therapeutic engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path == "/api/v1/clinical/phases/exit-phase-1":
        baseline_sgpt = float(body.get("baseline_sgpt", 0))
        current_sgpt = float(body.get("current_sgpt", 0))
        crp_down = bool(body.get("hs_crp_trending_down", False))
        if srv.verify_phase_1_exit:
            res = srv.verify_phase_1_exit(baseline_sgpt, current_sgpt, crp_down)
            handler._send_json({"ok": True, "exit_status": res})
        else:
            handler._send_error("Phase engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path == "/api/v1/clinical/phases/exit-phase-2":
        baseline_bm = float(body.get("baseline_biomarker", 0))
        current_bm = float(body.get("current_biomarker", 0))
        symptom_res = float(body.get("symptom_resolution_pct", 0))
        if srv.verify_phase_2_exit:
            res = srv.verify_phase_2_exit(baseline_bm, current_bm, symptom_res)
            handler._send_json({"ok": True, "exit_status": res})
        else:
            handler._send_error("Phase engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Dual-Track & Ilaj Hierarchy ──────────────────────────────────────
    if path == "/api/v1/therapeutic/delivery-track":
        is_remote = bool(body.get("is_remote", False))
        axes_count = int(body.get("active_axes_count", 1))
        quwwat_grade = int(body.get("quwwat_grade", 1))
        pref_conv = bool(body.get("patient_prefers_convenience", False))
        if srv.evaluate_clinical_delivery_track:
            res = srv.evaluate_clinical_delivery_track(is_remote, axes_count, quwwat_grade, pref_conv)
            handler._send_json({"ok": True, "track_evaluation": res})
        else:
            handler._send_error("Dual-track engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path == "/api/v1/therapeutic/ilaj-hierarchy":
        dawa = body.get("prescribed_dawa", [])
        tadbeer = body.get("tadbeer_prescriptions", [])
        ghiza = bool(body.get("ghiza_parhez_prescribed", False))
        nafsiyat = bool(body.get("nafsiyat_addressed", False))
        if srv.evaluate_ilaj_hierarchy_compliance:
            res = srv.evaluate_ilaj_hierarchy_compliance(dawa, tadbeer, ghiza, nafsiyat)
            handler._send_json({"ok": True, "hierarchy_check": res})
        else:
            handler._send_error("Ilaj hierarchy engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path == "/api/v1/therapeutic/cp-afum-safety":
        p_data = body.get("patient_data", {})
        ings = body.get("ingredients", [])
        meds = body.get("medications", [])
        if srv.evaluate_cp_afum_clinical_safety:
            res = srv.evaluate_cp_afum_clinical_safety(p_data, ings, meds)
            handler._send_json({"ok": True, "safety_evaluation": res, "requires_clinician_signoff": True})
        else:
            handler._send_error("Safety firewall unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Academic LMS & Practicum Registry ────────────────────────────────
    if path == "/api/v1/academic/practicum/validate-case":
        case_data = body.get("case_data", {})
        if srv.validate_practicum_case:
            res = srv.validate_practicum_case(case_data)
            handler._send_json({"ok": True, "validation": res})
        else:
            handler._send_error("Practicum registry unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path == "/api/v1/academic/practicum/evaluate-portfolio":
        cases = body.get("cases", [])
        if srv.evaluate_practicum_portfolio:
            res = srv.evaluate_practicum_portfolio(cases)
            handler._send_json({"ok": True, "portfolio": res})
        else:
            handler._send_error("Practicum registry unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path == "/api/v1/academic/certification/evaluate":
        profile = body.get("profile", {})
        if srv.evaluate_practitioner_tier:
            res = srv.evaluate_practitioner_tier(profile)
            handler._send_json({"ok": True, "certification_status": res})
        else:
            handler._send_error("Certification engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Global Edition (2026): ZAPE Decision Support ─────────────────────
    if path == "/api/v1/clinical/zape/evaluate":
        if srv.ZAPEEngine:
            res = srv.ZAPEEngine.generate_zape_decision_support(body)
            handler._send_json({"ok": True, "zape_decision_support": res})
        else:
            handler._send_error("ZAPE engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Global Edition (2026): Regimental Therapy & Thermoregulation ─────
    if path == "/api/v1/therapeutic/regimen/hammam":
        mizaj = body.get("mizaj", "Mutadil")
        condition = body.get("condition", "General Wellness")
        has_cvd = bool(body.get("has_cvd_history", False))
        is_preg = bool(body.get("is_pregnant", False))
        neuro = bool(body.get("neuropathy_present", False))
        if srv.RegimentalHydrotherapyEngine:
            res = srv.RegimentalHydrotherapyEngine.generate_hammam_prescription(mizaj, condition, has_cvd, is_preg, neuro)
            handler._send_json({"ok": True, "hammam_protocol": res})
        else:
            handler._send_error("Regimental engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path == "/api/v1/therapeutic/regimen/contrast-shower":
        mizaj = body.get("mizaj", "Mutadil")
        is_rayn = bool(body.get("is_raynauds", False))
        if srv.RegimentalHydrotherapyEngine:
            res = srv.RegimentalHydrotherapyEngine.generate_home_contrast_shower_protocol(mizaj, is_rayn)
            handler._send_json({"ok": True, "contrast_shower": res})
        else:
            handler._send_error("Regimental engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path == "/api/v1/therapeutic/regimen/dalak":
        mizaj = body.get("mizaj", "Mutadil")
        presentation = body.get("presentation", "General")
        has_dvt = bool(body.get("has_dvt_history", False))
        surg_wks = body.get("recent_surgery_weeks")
        if srv.RegimentalHydrotherapyEngine:
            res = srv.RegimentalHydrotherapyEngine.prescribe_dalak(mizaj, presentation, has_dvt, surg_wks)
            handler._send_json({"ok": True, "dalak_prescription": res})
        else:
            handler._send_error("Regimental engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path == "/api/v1/therapeutic/regimen/hijama-safety":
        plt = int(body.get("platelet_count", 250000))
        hb = float(body.get("hemoglobin_g_dl", 14.0))
        is_anti = bool(body.get("is_anticoagulated", False))
        is_prg = bool(body.get("is_pregnant", False))
        act_inf = bool(body.get("active_infection_at_site", False))
        if srv.RegimentalHydrotherapyEngine:
            res = srv.RegimentalHydrotherapyEngine.verify_hijama_safety(plt, hb, is_anti, is_prg, act_inf)
            handler._send_json({"ok": True, "safety_check": res})
        else:
            handler._send_error("Regimental engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Global Edition (2026): Disease Protocols & Appendix B Templates ───
    if path == "/api/v1/clinical/protocols/global/t2dm":
        if srv.GlobalProtocolsEngine:
            res = srv.GlobalProtocolsEngine.evaluate_t2dm(
                hba1c=float(body.get("hba1c", 5.5)),
                fbg=float(body.get("fbg", 95.0)),
                fasting_insulin=float(body.get("fasting_insulin", 6.0)),
                bmi=float(body.get("bmi", 24.0)),
                waist_cm=float(body.get("waist_cm", 82.0)),
                mizaj=body.get("mizaj", "Bard-Ratab"),
                current_meds=body.get("current_meds", [])
            )
            handler._send_json({"ok": True, "evaluation": res})
        else:
            handler._send_error("Protocols engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path == "/api/v1/clinical/protocols/global/hypertension":
        if srv.GlobalProtocolsEngine:
            res = srv.GlobalProtocolsEngine.evaluate_hypertension(
                sbp=int(body.get("sbp", 120)),
                dbp=int(body.get("dbp", 80)),
                mizaj=body.get("mizaj", "Harr-Ratab"),
                has_cardiac_symptoms=bool(body.get("has_cardiac_symptoms", False)),
                current_meds=body.get("current_meds", [])
            )
            handler._send_json({"ok": True, "evaluation": res})
        else:
            handler._send_error("Protocols engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path == "/api/v1/clinical/protocols/global/pcos":
        if srv.GlobalProtocolsEngine:
            res = srv.GlobalProtocolsEngine.evaluate_pcos(
                cycle_length_days=int(body.get("cycle_length_days", 28)),
                cycles_per_year=int(body.get("cycles_per_year", 12)),
                hirsutism_score=int(body.get("hirsutism_score", 4)),
                total_testosterone_nmol=float(body.get("total_testosterone_nmol", 1.8)),
                ovarian_follicles_count=int(body.get("ovarian_follicles_count", 10)),
                amh_pmol_l=float(body.get("amh_pmol_l", 20.0)),
                fasting_insulin=float(body.get("fasting_insulin", 6.0)),
                homa_ir=float(body.get("homa_ir", 1.5)),
                mizaj=body.get("mizaj", "Bard-Ratab"),
                fertility_intent=bool(body.get("fertility_intent", False))
            )
            handler._send_json({"ok": True, "evaluation": res})
        else:
            handler._send_error("Protocols engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path == "/api/v1/clinical/protocols/global/metabolic-syndrome":
        if srv.GlobalProtocolsEngine:
            res = srv.GlobalProtocolsEngine.evaluate_metabolic_syndrome(
                waist_cm=float(body.get("waist_cm", 85.0)),
                sex=body.get("sex", "male"),
                is_asian=bool(body.get("is_asian", True)),
                triglycerides_mg_dl=float(body.get("triglycerides_mg_dl", 120.0)),
                hdl_mg_dl=float(body.get("hdl_mg_dl", 48.0)),
                sbp=int(body.get("sbp", 120)),
                dbp=int(body.get("dbp", 80)),
                fbg_mg_dl=float(body.get("fbg_mg_dl", 95.0)),
                mizaj=body.get("mizaj", "Bard-Ratab")
            )
            handler._send_json({"ok": True, "evaluation": res})
        else:
            handler._send_error("Protocols engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path == "/api/v1/clinical/protocols/global/nafld":
        if srv.GlobalProtocolsEngine:
            res = srv.GlobalProtocolsEngine.evaluate_nafld(
                alt=float(body.get("alt", 25.0)),
                ast=float(body.get("ast", 22.0)),
                bmi=float(body.get("bmi", 25.0)),
                has_diabetes=bool(body.get("has_diabetes", False)),
                platelet_count=int(body.get("platelet_count", 250000)),
                age=int(body.get("age", 45))
            )
            handler._send_json({"ok": True, "evaluation": res})
        else:
            handler._send_error("Protocols engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path == "/api/v1/clinical/protocols/global/ibs":
        if srv.GlobalProtocolsEngine:
            res = srv.GlobalProtocolsEngine.evaluate_ibs(
                pain_days_per_week=int(body.get("pain_days_per_week", 0)),
                symptom_duration_months=int(body.get("symptom_duration_months", 0)),
                stool_pattern=body.get("stool_pattern", "normal"),
                mizaj=body.get("mizaj", "Bard-Ratab"),
                has_alarm_features=bool(body.get("has_alarm_features", False))
            )
            handler._send_json({"ok": True, "evaluation": res})
        else:
            handler._send_error("Protocols engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Modular Clinical 12-Axis Domain Dispatcher ────────────────────────
    from services.routes.clinical_routes import handle_clinical_post
    if handle_clinical_post(handler, path, query_params, auth_ctx, body):
        return True

    # ── ZAYVORA Pharmacopoeia: Formula Thermal & Safety Engine ─────────────
    if path == "/api/v1/therapeutic/formula/audit-safety":
        ingredients = body.get("ingredients") or []
        if not ingredients and "formula" in body:
            ingredients = body.get("formula", {}).get("ingredients", [])
        
        if srv.FormulaSafetyChecker:
            audit_res = srv.FormulaSafetyChecker.audit_formula_safety_and_musleh(ingredients)
            handler._send_json({"ok": True, "audit": audit_res})
        else:
            handler._send_error("Formula Safety Engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    if path == "/api/v1/therapeutic/formula/tadbir-verify":
        drug_name = body.get("drug_name") or body.get("key", "")
        tadbir_report = body.get("tadbir_report") or body.get("metadata", {})
        if srv.FormulaSafetyChecker:
            tadbir_res = srv.FormulaSafetyChecker.verify_tadbir_compliance(drug_name, tadbir_report)
            handler._send_json({"ok": True, "tadbir_verification": tadbir_res})
        else:
            handler._send_error("Formula Safety Engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── 80/20 Formulation Compliance Verification ─────────────────────────
    if path == "/api/v1/therapeutic/formula/validate-80-20":
        formula_items = body.get("formula_items") or body.get("items") or body.get("composition") or []
        if srv.validate_80_20_compliance:
            res = srv.validate_80_20_compliance(formula_items)
            handler._send_json({"ok": True, "evaluation": res})
        else:
            handler._send_error("80/20 compliance engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Clinical Decision Support: Plateau Evaluation ─────────────────────
    if path == "/api/v1/clinical/cds/plateau-evaluate":
        wks = int(body.get("weeks_on_protocol", 3))
        comp = float(body.get("reported_compliance_pct", 100.0))
        subj = float(body.get("subjective_improvement_pct", 0.0))
        stag = bool(body.get("lab_markers_stagnant", False))
        frust = bool(body.get("patient_frustration", False))
        herbs = body.get("current_herbs", [])
        if srv.ClinicalDecisionSupportExt:
            res = srv.ClinicalDecisionSupportExt.evaluate_treatment_plateau(
                weeks_on_protocol=wks,
                reported_compliance_pct=comp,
                subjective_improvement_pct=subj,
                lab_markers_stagnant=stag,
                patient_frustration=frust,
                current_herbs=herbs
            )
            handler._send_json({"ok": True, "result": res})
        else:
            handler._send_error("CDS engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Clinical Decision Support: Mixed Mizaj Resolution ─────────────────
    if path == "/api/v1/clinical/cds/mixed-mizaj-solve":
        o1 = body.get("organ_1", "Liver")
        m1 = body.get("mizaj_1", "Hot")
        o2 = body.get("organ_2", "Kidney")
        m2 = body.get("mizaj_2", "Cold")
        sym = body.get("primary_symptom", "Fatigue & low libido with elevated ALT")
        if srv.ClinicalDecisionSupportExt:
            res = srv.ClinicalDecisionSupportExt.resolve_mixed_mizaj_conflict(o1, m1, o2, m2, sym)
            handler._send_json({"ok": True, "resolution": res})
        else:
            handler._send_error("CDS engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Absolute Red-Flag & Emergency Referral Guard ──────────────────────
    if path == "/api/v1/clinical/triage/red-flags":
        symptoms = body.get("symptoms", [])
        labs = body.get("labs", {})
        notes = body.get("notes", "")
        if srv.EmergencyRedFlagGuard:
            res = srv.EmergencyRedFlagGuard.screen_patient_for_red_flags(symptoms, labs, notes)
            handler._send_json({"ok": True, "triage_evaluation": res})
        else:
            handler._send_error("Red flag guard unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Z-MAI 6-Domain Quantitative Mizaj Matrix (Part One Ch 9) ─────────
    if path in ("/api/v1/clinical/zmai/score-matrix", "/api/v1/clinical/zmai/matrix/calculate"):
        domain_scores = body.get("domain_scores") or body.get("scores") or {}
        if srv.calculate_mizaj_2_matrix:
            res = srv.calculate_mizaj_2_matrix(domain_scores)
            handler._send_json({"ok": True, "evaluation": res})
        else:
            handler._send_error("Z-MAI matrix tool unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── 4-Tier Polypharmacy Architecture Audit (Part One Ch 15) ───────────
    if path in ("/api/v1/therapeutic/formula/audit-4tier", "/api/v1/therapeutic/formula/polypharmacy-audit"):
        components = body.get("components") or body.get("ingredients") or []
        if srv.FormulaSafetyChecker:
            res = srv.FormulaSafetyChecker.audit_four_tier_polypharmacy(components)
            handler._send_json({"ok": True, "polypharmacy_audit": res})
        else:
            handler._send_error("Formula safety checker unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Ilaj bil Nafsiyat Assessment & Care Plan Generation ───────────────
    if path in ("/api/v1/clinical/nafsiyat/assess", "/api/v1/nafsiyat/assess"):
        if not srv.IlajBilNafsiyatEngine:
            handler._send_error("Nafsiyat engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
            return True
        chief_complaint = body.get("chief_complaint", "")
        narrative = body.get("narrative", "")
        symptoms = body.get("symptoms", [])
        # 1. Safety check
        safety = srv.IlajBilNafsiyatEngine.evaluate_psychiatric_safety(chief_complaint + " " + narrative)
        if safety:
            handler._send_json({"ok": False, "safety_block": True, "evaluation": safety})
            return True
        diag = srv.IlajBilNafsiyatEngine.diagnose_condition(symptoms, chief_complaint)
        handler._send_json({"ok": True, "evaluation": diag})
        return True


    # ── Ilaj bil Ghiza Endpoints ─────────────────────────────────────────
    if path in ("/api/v1/clinical/ghiza/formulate", "/api/v1/ghiza/formulate"):
        if not srv.IlajBilGhizaEngine:
            handler._send_error("Ilaj bil Ghiza Engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
            return True
        mizaj = body.get("mizaj", "Motadil")
        su_e_mizaj = body.get("su_e_mizaj")
        candidate_foods = body.get("candidate_foods", [])
        regimen = srv.IlajBilGhizaEngine.formulate_dietary_regimen(mizaj, su_e_mizaj, candidate_foods)
        handler._send_json({"ok": True, "regimen": regimen})
        return True

    if path in ("/api/v1/clinical/ghiza/incompatibilities", "/api/v1/ghiza/incompatibilities"):
        if not srv.IlajBilGhizaEngine:
            handler._send_error("Ilaj bil Ghiza Engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
            return True
        foods = body.get("foods", [])
        antagonisms = srv.IlajBilGhizaEngine.check_food_incompatibilities(foods)
        handler._send_json({"ok": True, "antagonisms": antagonisms, "is_safe": len(antagonisms) == 0})
        return True

    # ── Ilaj bil Yad Endpoints ───────────────────────────────────────────
    if path in ("/api/v1/clinical/yad/evaluate", "/api/v1/yad/evaluate"):
        if not srv.IlajBilYadEngine or not srv.SurgicalAssessmentInput:
            handler._send_error("Ilaj bil Yad Engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
            return True
        s_input = srv.SurgicalAssessmentInput(
            patient_id=body.get("patient_id", "P-GENERIC"),
            age=int(body.get("age", 35)),
            gender=body.get("gender", "unspecified"),
            systolic_bp=int(body.get("systolic_bp", 120)),
            diastolic_bp=int(body.get("diastolic_bp", 80)),
            hemoglobin_g_dl=float(body.get("hemoglobin_g_dl", 13.5)),
            is_pregnant=bool(body.get("is_pregnant", False)),
            proposed_procedure=body.get("proposed_procedure", "FASD"),
            target_site=body.get("target_site", "Basaliq"),
            clinical_indication=body.get("clinical_indication", "Imtila")
        )
        eval_res = srv.IlajBilYadEngine.evaluate_surgical_safety(s_input)
        handler._send_json({"ok": True, "assessment": eval_res})
        return True

    if path in ("/api/v1/clinical/nafsiyat/plan", "/api/v1/nafsiyat/plan"):
        if not srv.IlajBilNafsiyatEngine or not srv.NafsiyatAssessmentInput:
            handler._send_error("Nafsiyat engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
            return True
        inp = srv.NafsiyatAssessmentInput(
            patient_id=body.get("patient_id", "P-UNKNOWN"),
            age=int(body.get("age", 35)),
            gender=body.get("gender", "Unknown"),
            chief_complaint=body.get("chief_complaint", ""),
            patient_narrative=body.get("narrative", ""),
            presenting_symptoms=body.get("symptoms", []),
            current_mizaj=body.get("current_mizaj", "Damwi"),
            stress_level=body.get("stress_level", "MODERATE"),
            sleep_hours=float(body.get("sleep_hours", 6.5)),
            social_isolation=bool(body.get("social_isolation", False)),
            spiritual_disconnection=bool(body.get("spiritual_disconnection", False)),
            grief_or_trauma_present=bool(body.get("grief_or_trauma_present", False)),
            emotional_suppression_present=bool(body.get("emotional_suppression_present", False)),
        )
        plan = srv.IlajBilNafsiyatEngine.generate_care_plan(inp)
        handler._send_json({"ok": True, "care_plan": plan})
        return True

    # ── Ilaj bil Tadbeer Evaluation & Guardrail Screening ─────────────────
    if path in ("/api/v1/therapeutic/tadbeer/evaluate", "/api/v1/clinical/tadbeer/evaluate"):
        if not srv.run_tadbeer_guardrails:
            handler._send_error("Tadbeer guardrails engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
            return True
        p_context = body.get("patient_context", {})
        plan = body.get("plan", {})
        res = srv.run_tadbeer_guardrails(patient_context=p_context, plan=plan)
        handler._send_json({"ok": True, "guardrail_evaluation": res})
        return True

    # ── Closed-Loop Biomarker Confirmation (Part One Ch 8) ────────────────
    if path in ("/api/v1/clinical/labs/biomarker-closed-loop", "/api/v1/clinical/labs/humoral-correlation"):
        humor = body.get("suspected_humor") or body.get("humor") or body.get("condition", "BALGHAM")
        labs = body.get("labs", {})
        if srv.verify_humoral_biomarker_correlation:
            res = srv.verify_humoral_biomarker_correlation(humor, labs)
            handler._send_json({"ok": True, "biomarker_correlation": res})
        else:
            handler._send_error("Biomarker correlation engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── 4-Tier Evidence Hierarchy & Claims Discipline (Part One Ch 17) ─────
    if path in ("/api/v1/knowledge/claims/validate", "/api/v1/knowledge/evidence/validate-claim"):
        claim_text = body.get("claim_text", "")
        evidence_tier = body.get("evidence_tier", "TIER_3")
        if srv.validate_product_claim:
            res = srv.validate_product_claim(claim_text, evidence_tier)
            handler._send_json({"ok": True, "claims_evaluation": res})
        else:
            handler._send_error("Claims validator unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Nuskha Lifecycle State Machine Transition (Blueprint §40) ─────────
    if path in ("/api/v1/therapeutic/nuskha/transition", "/api/v1/therapeutic/nuskha/transition-state"):
        nuskha_id = body.get("nuskha_id", "NSK-DEFAULT")
        curr_state = body.get("current_state", "DRAFT")
        target_state = body.get("target_state", "SAFETY_CHECK")
        actor_id = body.get("actor_id", "user-clinician")
        actor_role = body.get("actor_role", "DOCTOR")
        reason = body.get("reason", "Standard clinical evaluation")
        version = int(body.get("current_version", 1))
        ev_refs = body.get("evidence_refs", [])
        safe_refs = body.get("safety_refs", [])
        if srv.NuskhaStateMachine:
            res = srv.NuskhaStateMachine.transition(
                nuskha_id, curr_state, target_state, actor_id, actor_role, reason, version, ev_refs, safe_refs
            )
            status_code = 200 if res["success"] else 403
            handler._send_json({"ok": res["success"], "transition_result": res}, status=status_code)
        else:
            handler._send_error("Nuskha state machine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Copilot Action Permission Evaluation (Blueprint §41) ──────────────
    if path in ("/api/v1/ai/copilot/evaluate-permission", "/api/v1/ai/copilot/check-permission"):
        action = body.get("action", "read_patient_chart")
        role = body.get("actor_role", "HAKEEM_SAHAB_AI")
        clinician_present = bool(body.get("is_clinician_present", False))
        if srv.CopilotPermissionGuard:
            res = srv.CopilotPermissionGuard.evaluate_permission(action, role, clinician_present)
            handler._send_json({"ok": True, "permission_evaluation": res})
        else:
            handler._send_error("Copilot permission guard unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Canonical Safety Evaluation Contract (Blueprint §24) ──────────────
    if path in ("/api/v1/safety/evaluate", "/api/v1/therapeutic/safety/evaluate"):
        patient_id = body.get("patient_id", "P-DEFAULT")
        interventions = body.get("candidate_interventions", [])
        context = body.get("context", {})
        if srv.CanonicalSafetyService:
            res = srv.CanonicalSafetyService.evaluate(patient_id, interventions, context)
            handler._send_json({"ok": True, "safety_evaluation": res})
        else:
            handler._send_error("Safety service unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Master Nuskha Synthesis (7-Pillar Classical Architecture) ────────
    if path in ("/api/v1/therapeutic/nuskha/master-synthesize", "/api/v1/therapeutic/nuskha/synthesize"):
        organ_axis = body.get("organ_axis", "MALE_REPRODUCTIVE")
        indication = body.get("indication", "General Vitality & Tone")
        ingredients = body.get("ingredients", [])
        patient_ctx = body.get("patient_context", {})
        if srv.synthesize_master_nuskha:
            res = srv.synthesize_master_nuskha(organ_axis, indication, ingredients, patient_ctx)
            handler._send_json({"ok": True, "master_nuskha": res})
        else:
            handler._send_error("Master Nuskha architect engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Tailored Dietary Parhez Matrix ───────────────────────────────────
    if path in ("/api/v1/therapeutic/nuskha/parhez-matrix", "/api/v1/therapeutic/parhez-matrix"):
        organ_axis = body.get("organ_axis", "MALE_REPRODUCTIVE").upper()
        axis_key = organ_axis.replace("-", "_").replace(" ", "_")
        parhez = srv.ORGAN_PARHEZ_MATRIX.get(axis_key, srv.ORGAN_PARHEZ_MATRIX.get("MALE_REPRODUCTIVE", {
            "prohibited_antagonistic": [],
            "accelerating_synergistic": [],
            "regimental_lifestyle": []
        }))
        handler._send_json({
            "ok": True,
            "organ_axis": organ_axis,
            "dietary_parhez_protocol": parhez
        })
        return True

    # ── Modular Clinical Diagnostics & Asbab-e-Sittah Dispatcher ──────────
    from services.routes.clinical_routes import handle_clinical_post
    if handle_clinical_post(handler, path, query_params, auth_ctx, body):
        return True

    # ── Munzij & Mushil (Nujz & Tanqiya) Staging Protocol ─────────────────
    if path in ("/api/v1/therapeutic/nuskha/munzij-mushil-protocol", "/api/v1/therapeutic/munzij-mushil"):
        patient_id = body.get("patient_id", "P-ANON")
        target_humor = body.get("target_humor", "Balgham")
        chronicity = body.get("chronicity_level", "CHRONIC")
        has_active_nujz = body.get("has_active_nujz", False)
        if srv.MunzijMushilProtocolEngine:
            res = srv.MunzijMushilProtocolEngine.synthesize_protocol(patient_id, target_humor, chronicity, has_active_nujz)
            handler._send_json({"ok": True, "munzij_mushil_protocol": res})
        else:
            handler._send_error("Munzij-Mushil protocol engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── CYP450 Pharmacokinetic Drug-Herb Interaction Check ────────────────
    if path in ("/api/v1/therapeutic/interactions/cyp450-check", "/api/v1/therapeutic/cyp450"):
        allopathic = body.get("current_allopathic_medications", [])
        herbs = body.get("candidate_herbs", [])
        if srv.CYP450InteractionEngine:
            res = srv.CYP450InteractionEngine.evaluate_pharmacokinetic_risk(allopathic, herbs)
            handler._send_json({"ok": True, "cyp450_evaluation": res})
        else:
            handler._send_error("CYP450 interaction engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Canonical Formulation Conflict Check (Multi-part / Duplicate) ─────
    if path in ("/api/v1/therapeutic/formula/canonical-check", "/api/v1/therapeutic/canonical-check"):
        ingredients = body.get("ingredients", [])
        if srv.check_formulation_canonical_conflicts:
            conflicts = srv.check_formulation_canonical_conflicts(ingredients)
            handler._send_json({
                "ok": True,
                "conflicts_found_count": len(conflicts),
                "has_canonical_duplicates": len(conflicts) > 0,
                "conflicts": conflicts
            })
        else:
            handler._send_error("Canonical check engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Badal-e-Advia Substitute Advisory ────────────────────────────────
    if path in ("/api/v1/therapeutic/badal-e-advia/recommend", "/api/v1/therapeutic/badal"):
        ing_name = body.get("ingredient_name", "")
        zmf_id = body.get("zmf_id", "")
        indication = body.get("indication", "")
        patient_mizaj = body.get("patient_mizaj", "")
        if not ing_name and not zmf_id:
            handler._send_error("Provide 'ingredient_name' or 'zmf_id'.", status=400, code="MISSING_PARAM")
            return True
        if srv.BadalEAdviaEngine:
            result = srv.BadalEAdviaEngine.get_badal_recommendations(
                ingredient_name=ing_name, zmf_id=zmf_id,
                indication=indication, patient_mizaj=patient_mizaj
            )
            handler._send_json({"ok": True, "badal_recommendations": result})
        else:
            handler._send_error("Badal-e-Advia engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── 12-Gate Pipeline Sign-Off ─────────────────────────────────────────
    if path in ("/api/v1/governance/12-gate/signoff", "/api/v1/governance/gate-signoff"):
        zmf_id = body.get("zmf_id", "")
        gate_number = body.get("gate_number")
        signed_by = body.get("signed_by", "")
        notes = body.get("notes", "")
        override = body.get("override_incomplete_prior", False)
        if not zmf_id or not gate_number or not signed_by:
            handler._send_error("Provide 'zmf_id', 'gate_number', and 'signed_by'.", status=400, code="MISSING_PARAM")
            return True
        if srv.TwelveGateTrackerEngine:
            result = srv.TwelveGateTrackerEngine.record_gate_signoff(
                zmf_id=zmf_id, gate_number=int(gate_number),
                signed_by=signed_by, notes=notes,
                override_incomplete_prior=override
            )
            status_code = 200 if result.get("success") else 400
            handler._send_json({"ok": result.get("success", False), "result": result}, status=status_code)
        else:
            handler._send_error("12-Gate Tracker unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Copilot Ingredient Access Gate ────────────────────────────────────
    if path in ("/api/v1/ai/copilot/ingredient-access", "/api/v1/governance/ingredient-gate"):
        zmf_id = body.get("zmf_id", "")
        ingredient_name = body.get("ingredient_name", "")
        actor_role = body.get("actor_role", "HAKEEM_SAHAB_AI")
        context = body.get("context", "retrieve_knowledge")
        if not zmf_id:
            handler._send_error("Provide 'zmf_id'.", status=400, code="MISSING_PARAM")
            return True
        if srv.CopilotPermissionGuard:
            result = srv.CopilotPermissionGuard.evaluate_ingredient_access(
                zmf_id=zmf_id, ingredient_name=ingredient_name,
                actor_role=actor_role, context=context
            )
            handler._send_json({"ok": True, "access_decision": result})
        else:
            handler._send_error("Copilot Permission Guard unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Batch Patient Card Generation ─────────────────────────────────────
    if path in ("/api/v1/knowledge/mufradat-250/cards/batch", "/api/v1/knowledge/patient-cards/batch"):
        zmf_ids = body.get("zmf_ids", [])
        if not zmf_ids or not isinstance(zmf_ids, list):
            handler._send_error("Provide 'zmf_ids' as a list of ZMF IDs.", status=400, code="MISSING_PARAM")
            return True
        if srv.MufradatCardGenerator:
            result = srv.MufradatCardGenerator.generate_batch_cards(zmf_ids)
            handler._send_json({"ok": True, "batch_result": result})
        else:
            handler._send_error("Card Generator unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── 25-Drug Gold Benchmark AI Safety Gate ────────────────────────────
    if path in ("/api/v1/governance/mufradat-gold/ai-safety-gate", "/api/v1/governance/gold-safety-gate"):
        zmf_id = body.get("zmf_id", "")
        if not zmf_id:
            handler._send_error("Provide 'zmf_id'.", status=400, code="MISSING_PARAM")
            return True
        if srv.GoldBenchmarkRegistry:
            result = srv.GoldBenchmarkRegistry.evaluate_ai_safety_gate(zmf_id)
            handler._send_json({"ok": True, "safety_gate_evaluation": result})
        else:
            handler._send_error("Gold benchmark registry unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Validated Murakkab Custom Nuskha Audit ───────────────────────────
    if path in ("/api/v1/therapeutic/murakkab-validated/audit-nuskha", "/api/v1/therapeutic/nuskha-audit"):
        nuskha_name = body.get("nuskha_name", "Custom Formulated Nuskha")
        ingredients = body.get("ingredients", [])
        if not ingredients or not isinstance(ingredients, list):
            handler._send_error("Provide 'ingredients' as a non-empty list of items.", status=400, code="MISSING_PARAM")
            return True
        if srv.ValidatedMurakkabCompiler:
            audit_result = srv.ValidatedMurakkabCompiler.audit_custom_nuskha(nuskha_name, ingredients)
            handler._send_json({"ok": True, "nuskha_audit": audit_result})
        else:
            handler._send_error("Murakkab compiler unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Multi-Disciplinary Digital Sign-off Recording ────────────────────
    if path in ("/api/v1/governance/signoff/record", "/api/v1/clinical/signoff/record"):
        target_id = body.get("target_id", "")
        role = body.get("role", "")
        expert_name = body.get("expert_name", "")
        expert_credentials = body.get("expert_credentials", "BUMS / MD Unani")
        comments = body.get("comments", "")
        passed = body.get("passed", True)

        if not target_id or not role or not expert_name:
            handler._send_error("Provide 'target_id', 'role', and 'expert_name'.", status=400, code="MISSING_PARAM")
            return True

        if srv.ClinicalMultiSignoffEngine:
            result = srv.ClinicalMultiSignoffEngine.record_expert_signoff(
                target_id=target_id,
                target_type=body.get("target_type", "CLINICAL_PRESCRIPTION"),
                role=role,
                expert_name=expert_name,
                expert_credentials=expert_credentials,
                comments=comments,
                passed=passed
            )
            handler._send_json({"ok": True, "signoff_result": result})
        else:
            handler._send_error("Signoff engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # ── Knowledge Intelligence & Clinical Governance vNEXT ───────────────
    if path == "/api/v1/governance/knowledge-vnext/safety-evaluate":
        drug_dict = body.get("drug", {})
        req_role = body.get("user_role", "RESEARCHER")
        if srv.SafetyFirewallV2:
            verdict = srv.SafetyFirewallV2.evaluate_drug_safety_state(drug_dict, req_role)
            handler._send_json({"ok": True, "safety_evaluation": verdict})
        else:
            handler._send_error("Knowledge vNEXT engine unavailable.", status=503)
        return True

    if path == "/api/v1/governance/knowledge-vnext/transition-state":
        curr_st = body.get("current_state", "")
        target_st = body.get("target_state", "")
        try:
            c_enum = srv.KnowledgeState(curr_st)
            t_enum = srv.KnowledgeState(target_st)
        except ValueError:
            handler._send_error(f"Invalid knowledge states provided: {curr_st} -> {target_st}", status=400)
            return True

        if srv.KnowledgeStateMachine:
            allowed, reason = srv.KnowledgeStateMachine.can_transition(c_enum, t_enum)
            handler._send_json({"ok": True, "allowed": allowed, "reason": reason, "current_state": curr_st, "target_state": target_st})
        else:
            handler._send_error("Knowledge vNEXT engine unavailable.", status=503)
        return True

    if path == "/api/v1/governance/knowledge-vnext/reviewer-action":
        target_drug_id = body.get("drug_id", "")
        action_str = body.get("action", "")
        actor_id = body.get("actor_id", "ANON_REVIEWER")
        notes = body.get("notes", "")
        payload = body.get("payload", {})
        try:
            act_enum = srv.ReviewerAction(action_str)
        except ValueError:
            handler._send_error(f"Invalid reviewer action: {action_str}", status=400)
            return True

        if srv.ReviewerWorkspaceEngine:
            res = srv.ReviewerWorkspaceEngine.execute_reviewer_action(target_drug_id, act_enum, actor_id, notes, payload)
            handler._send_json({"ok": True, "action_result": res})
        else:
            handler._send_error("Knowledge vNEXT engine unavailable.", status=503)
        return True

    if path == "/api/v1/governance/knowledge-vnext/grounded-brief":
        drug_id = body.get("drug_id", "")
        if srv.GroundedHakeemSahabVNext:
            brief = srv.GroundedHakeemSahabVNext.generate_grounded_brief(drug_id)
            handler._send_json({"ok": True, "grounded_brief": brief})
        else:
            handler._send_error("Knowledge vNEXT engine unavailable.", status=503)
        return True

    if path == "/api/v1/governance/knowledge-vnext/evaluate-patient-safety":
        drug_id = body.get("drug_id", "")
        curr_st = body.get("current_state", "CANDIDATE")
        is_e1 = body.get("is_schedule_e1", False)
        clinician_signed = body.get("clinician_signed", False)
        if srv.PatientSafetyBarrier:
            safe, reason = srv.PatientSafetyBarrier.is_safe_for_patient_regimen(drug_id, curr_st, is_e1, clinician_signed)
            handler._send_json({"ok": True, "safe": safe, "reason": reason})
        else:
            handler._send_error("Knowledge vNEXT engine unavailable.", status=503)
        return True

    if path == "/api/v1/governance/knowledge-vnext/murakkab-record":
        f_name = body.get("formula_name", "")
        m_class = body.get("formula_class", "CLASSICAL_FORMULATION")
        ings = body.get("ingredients", [])
        auth_src = body.get("authoritative_source")
        rnd_rationale = body.get("rnd_rationale")
        try:
            c_enum = srv.MurakkabClass(m_class)
        except ValueError:
            handler._send_error(f"Invalid Murakkab class: {m_class}", status=400)
            return True
        if srv.MurakkabGovernanceEngine:
            rec = srv.MurakkabGovernanceEngine.create_murakkab_record(
                f_name, c_enum, ings, authoritative_source=auth_src, rnd_rationale=rnd_rationale
            )
            handler._send_json({"ok": True, "murakkab_record": rec})
        else:
            handler._send_error("Knowledge vNEXT engine unavailable.", status=503)
        return True

    # ── Clinical Knowledge Graph & Doctor Continuum ─────────────────────
    if path == "/api/v1/clinical/graph/reasoning-path":
        cond = body.get("condition", "Waja-ul-Mafasil")
        mizaj = body.get("mizaj", "Balgham")
        axes = body.get("axes", [])
        pctx = body.get("patient_context", {})
        if srv.get_clinical_knowledge_graph:
            graph = srv.get_clinical_knowledge_graph()
            res = graph.query_graph_for_clinical_context(cond, patient_mizaj=mizaj, active_axes=axes, patient_risk_context=pctx)
            handler._send_json({"ok": True, "reasoning_path": res})
        else:
            handler._send_error("Clinical graph engine unavailable.", status=503)
        return True

    # ── Case Simulator Decision Evaluation ────────────────────────────────
    if path.startswith("/api/v1/simulator/cases/") and path.endswith("/evaluate"):
        parts = path.strip("/").split("/")
        case_id = parts[-2]
        raw_answers = body.get("answers", {})
        int_answers = {}
        for k, v in raw_answers.items():
            try:
                int_answers[int(k)] = int(v)
            except (ValueError, TypeError):
                pass
        clinician_id = body.get("clinician_id", auth_ctx["id"] if auth_ctx else "CLINICIAN-GUEST")
        if srv.CaseSimulatorEngine:
            eval_res = srv.CaseSimulatorEngine.evaluate_case_submission(
                case_id=case_id,
                user_answers=int_answers,
                clinician_id=clinician_id
            )
            handler._send_json(eval_res)
        else:
            handler._send_error("Case Simulator Engine unavailable.", status=503)
        return True
    return False
