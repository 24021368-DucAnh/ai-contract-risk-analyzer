# Twenty Additional Contract Intake Plan

> **For agentic workers:** Execute this plan inline in the existing `codex/contract-source-intake` worktree; keep the ledger current and do not push, open a PR, or merge.

**Goal:** Add and quality-check 20 additional unique signed employment contract documents into the project’s established local data structure, with each contract admitted only after source, privacy, independence, extraction, and review gates pass.

**Architecture:** Search primary sources and contributor-provided material. Keep unverified originals in ignored `data/intake/restricted/`; only move eligible, de-identified derivatives into the established `data/raw/contracts/` and associated raw-text/metadata paths. Obtain a Legal Data Hunter review only after an individual contract passes the project’s intake gates. If no eligible/authorized records are available, document the blocker and do not manufacture a completion count.

**Tech Stack:** Existing repository CSV/PDF/DOCX tools, local extraction and similarity checks, project intake manifest and documentation, Legal Data Hunter for law/source review.

**Spec:** `data/intake/README.md`, `docs/data_sources.md`, `CONTRIBUTING.md`, current Data Lead plan and contract source-intake QC records.

## Global Constraints

- Target is 20 additional accepted unique signed contract documents. Do not count blank models, appendices, bundles, exact duplicate copies, or holds. Distinct executed agreements may share an employer/template; record the similarity group and keep it together for evaluation splits.
- Do not infer processing, redistribution, or benchmark rights from a public URL.
- Do not commit raw PII, OCR text with PII, signatures, or unredacted contract pages to tracked files.
- Preserve source bytes and record exact source URL, source page, hash, size, page boundaries, and QC status in the existing manifest.
- Do not invent legal-risk labels or treat structural draft labels as reviewed gold.
- Do not push, create a PR, or merge.

## Review Focus

1. Same employer/template filings may look like separate contracts but form one leakage group; compare known content and page layouts.
2. Public attachments can contain personal data, identity documents, signatures, and seals; keep restricted and do not expose those fields in tracked notes.
3. PDF text layers can be corrupt or omit scan text; compare extracted text against page images before trusting offsets.
4. A published government attachment does not by itself establish a reuse license or authority to process personal information for this project.
5. A locally split contract or OCR draft is not an accepted benchmark example until boundaries, anonymization, rights, and second-person review are documented.

---

### Task 1: Reconcile current repository state

**Files:** Read `data/intake/manifest.csv`, `data/contracts_metadata.csv`, `data/intake/README.md`, `docs/data_sources.md`, and current raw/processed directories.

- [x] Count current intake records and accepted additions separately: 34 manifest rows, 0 accepted toward the 20-additional target; the 34 rows include fragments and non-contract/duplicate/excluded records and must not be read as 34 contracts.
- [x] Preserve existing user changes and ensure no source documents are edited in place.
- [x] Record the current accepted count toward the 20-additional target in the ledger.

### Task 2: Find and register primary-source candidates

**Files:** Add candidate receipts to `data/intake/manifest.csv` and concise non-PII QC notes to `data/intake/README.md`.

- [ ] Search government, employer-authorized, academic, and contributor sources for actual employment contracts. Search continues; official VIMDA search surfaced further actual agreements, but public posting does not establish project reuse rights.
- [ ] Confirm the attachment is an employment contract, not a blank model, annex, dossier, or public-service work contract.
- [ ] Download only to ignored `data/intake/restricted/` while rights and privacy are unresolved; avoid acquiring additional identifiable copies when the project lacks a lawful basis/reuse authorization and the existing restricted queue already exceeds review capacity.
- [ ] Check file identity, page count, exact boundary, hashes, duplicate/template group, and scan/text quality.

### Task 3: Apply acceptance gates and process eligible contracts

**Files:** For accepted items only, update established raw contract, raw-text, metadata, and intake documentation paths.

- [ ] Confirm authority to store/process, internal share, and use the de-identified derivative for evaluation.
- [ ] Create a separate de-identified derivative; inspect every page and text layer, including metadata, tables, headers, signatures, seals, and indirect identifiers.
- [ ] Record the independent reviewer and decision; keep unresolved items on HOLD.
- [ ] Extract text and draft clause boundaries only after redaction and readable source/text alignment; preserve offsets, hashes, and source-page provenance.
- [ ] Do not add legal-risk gold without supported legal review and the project’s annotation rules.
- [ ] Ask Legal Data Hunter to review applicable primary law or rights only when the specific candidate meets its intake gate and when the tool’s coverage fits the question.

### Task 4: Completion audit

- [ ] Verify exactly 20 additional accepted unique signed agreements. Same-family signed agreements can count as documents, but their similarity group must be recorded and must not be presented as independent test sources.
- [ ] Validate manifest consistency, hashes, exact span offsets, duplicate/leakage groups, privacy review, and second-person sign-off.
- [ ] Run only relevant existing validators/tests and inspect all outputs.
- [ ] Report completed count and remaining blockers; leave all GitHub publishing/integration actions undone.

### Dated intake reconciliation — 2026-10-28

The 34-row count in Task 1 was captured on an earlier worktree and is retained as a historical snapshot. The current authoritative `data/intake/manifest.csv` on `codex/data-intake-status-2026-10-27` has 22 rows (21 file-linked local receipts with matching sizes and SHA-256, one removed/invalid item with no file). All `t1_eligible=no`; accepted T1 0/10, additional signed contracts 0/20. See `docs/archive/reports/CONTRACT_SOURCE_AND_LEGAL_REVIEW_2026-10-28.md` for the new official e-contract access/legal-source path and gates. Continue Task 2 without recreating missing historical rows. Do not publish held sources.

### Task 3 legal-reference preparation — 2026-10-28

Ruling: source-reference discovery can proceed on the existing **local** raw-text corpus before signed-source admission, provided it exports only PII-free locators and leaves all legal decisions pending; this enables targeted outside legal review without creating unsupported gold labels. `scripts/audit_legal_citations.py` creates `data/intake/legal_citation_review_queue.csv` with 14 review items (13 raw-text mentions and one annotation note), two suspected article mismatches, and no human approvals. This does **not** satisfy Task 3's signed-source or second-review gates. Source-collection Task 2 and acceptance Task 3 remain open pending authorization, distinct signed documents, anonymization, and independent review.

### Task 2 source-holder referral preparation — 2026-10-28

`data/intake/source_referral_batches_2026-10-28.csv` groups 14 held source candidates into 5 **draft-only** non-PII referral requests across government publisher channels; 14 candidate/route pairs match the already registered 17 public contact routes, and every source is mapped exactly once. `docs/SIGNED_CONTRACT_REFERRAL_AND_PARTNER_PACK_2026-10-28.md` provides the draft publisher-referral request and a separate employer-led invitation to obtain genuinely executed agreements with appropriate rights and worker-data safeguards. All requests are still unsent; no owner, rights-holder authorization, or legal-human sign-off is recorded. Verified official effective dates for Law 91/2025/QH15 and Decree 356/2025/ND-CP are 2026-01-01, but applicable provisions and transition rules require independent legal assessment. Task 2 is open, Task 3 acceptance remains 0/10 T1 and 0/20 additional, and Task 4 is open.

Expanded potential opt-in employer introductions in `data/intake/consenting_employer_referral_routes_2026-10-28.csv` and `docs/CONSENTING_EMPLOYER_REFERRAL_RESEARCH_2026-10-28.md`: five verified public organization-level contact paths through four distinct business networks (two VCCI routes, VINASME, VINASA and HAWA). These are only potential channels to employers, not a claim of participation, source authorization, available contract families, signed documents, or successful contact. Every record stays `RESEARCH_ONLY`; no message has been sent. Contract acceptance remains 0/30.

The optional employer contribution form `docs/CONTRACT_CONTRIBUTION_PERMISSION_FORM_DRAFT_2026-10-28.md` was drafted and checked into the **local working tree only**. It requires evidence of provider authority and lawful processing of worker data, with separate permissions for original retention, local OCR, de-identification, internal T1 evaluation and additional split; public disclosure and third-party AI use default to NO. Its status is `DRAFT_ONLY`: no signature, permission, legal validation, or incoming agreement exists. The VCCI member-affairs page and a September 2026 event page publish conflicting `.com.vn`/`.org.vn` email domains; authenticate the recipient by an official phone route before any outreach. Neither the form nor the contacts advance Task 3 acceptance or Task 4 completion.
