# ZAYVORA HEALTH™ — Production Readiness Audit
## 07. Nuskha Nawisi (Prescription Compiler & Clinical Sequencing) Audit
*Tagline: “Ancient Wisdom. Modern Science. Intelligent Care.”*

---

### 1. Nuskha Nawisi Methodology
Nuskha Nawisi is the formal sequential methodology of Unani clinical prescribing:
1. Identify underlying etiology (*Asbab*)
2. Formulate diagnostic assessment (*Tashkhis*)
3. Establish therapeutic principle (*Usool-e-Ilaj*)
4. Select active therapeutic agents (*Adwiya*)
5. Specify correctives (*Musleh*) and adjuvants
6. Enforce dietary restrictions (*Parhez*)

---

### 2. Findings

#### Finding NN-01: Stepwise Prescription Compiler & Posology Engine
1. **Feature/module name**: Nuskha Nawisi Compiler & Posology Validator
2. **Expected behavior**: Validates formulation sequence, computes posology limits, balances temperamental properties, and enforces Safety Firewall review before draft approval.
3. **Actual implementation status**: Engine in `nuskha_compiler.py` and router in `services/therapeutic/app/routers/nuskha.py`.
4. **Evidence**:
   - **file path**: `services/therapeutic/app/engines/nuskha_compiler.py` & `routers/nuskha.py`
   - **function/class/component**: `NuskhaCompiler.compile()`, `create_nuskha_draft()`, `approve_nuskha_draft()`
   - **API route**: `POST /api/v1/therapeutic/nuskha/compile`, `POST /api/v1/therapeutic/nuskha`
   - **database table**: `nuskha_drafts`
   - **test result**: `test_nuskha_compiler.py` — PASSED (7/7 tests passing)
5. **Status**: FULLY IMPLEMENTED
6. **Severity**: P1 High
7. **Recommended fix**: Implement automatic Badal (substitute) recommendation when a primary herb is marked out of stock in hospital pharmacy.
8. **Dependencies**: `services/therapeutic`, `services/knowledge`
9. **Acceptance criteria**: Drafts cannot be approved if the Safety Firewall assigns a `DO_NOT_RECOMMEND` verdict without authenticated override.
