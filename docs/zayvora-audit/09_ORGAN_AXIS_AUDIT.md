# ZAYVORA HEALTH™ — Production Readiness Audit
## 09. Organ-Axis Differential Diagnostics Audit
*Tagline: “Ancient Wisdom. Modern Science. Intelligent Care.”*

---

### 1. Functional Organ Axes
In Unani physiology, organs operate in connected functional networks centered around the three primary organs (*A'da-e-Ra'eesah*):
- **Qalb-Dimagh Axis** (Heart-Brain Axis): Emotional-cognitive and autonomic regulation.
- **Kabid-Middah Axis** (Liver-Stomach Axis): Digestion, metabolic transformation, and humoral generation.
- **Kulyah-Masana Axis** (Kidney-Bladder Axis): Fluid balance, waste filtration, and retention.

---

### 2. Findings

#### Finding OA-01: Multi-Organ Interaction Diagnostic Engine
1. **Feature/module name**: Organ-Axis Differential Diagnostics
2. **Expected behavior**: Analyzes patient symptoms to determine whether primary pathology is located in root organ or sympathetic reflected organ.
3. **Actual implementation status**: Implemented in `organ_axis_engine.py` with multi-axis correlation scoring.
4. **Evidence**:
   - **file path**: `services/clinical/app/engines/organ_axis_engine.py` & `routers/organ_axis.py`
   - **function/class/component**: `OrganAxisEngine.evaluate_axes()`, `assess_organ_axes()`
   - **API route**: `POST /api/v1/clinical/organ-axis/assess`
   - **database table**: Linked to `encounters`
   - **test result**: `test_organ_axis_and_evidence.py` — PASSED (7/7 tests passing)
5. **Status**: FULLY IMPLEMENTED
6. **Severity**: P2 Medium
7. **Recommended fix**: Add gastrointestinal microbiome biomarker inputs to refine the Kabid-Middah axis evaluation.
8. **Dependencies**: `services/clinical`
9. **Acceptance criteria**: Correctly distinguishes between primary gastric dyspepsia and secondary hepatic dyscrasia.
