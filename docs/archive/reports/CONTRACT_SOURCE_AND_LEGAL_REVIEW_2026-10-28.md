# Contract intake and legal-source review — 2026-10-28

Scope: 10 **independent, signed** T1 employment contracts plus 20 **additional distinct, signed** employment contracts. Candidate-only report: no PII or copied private contract text.

## Current repository evidence

- `data/intake/manifest.csv`: 22 candidates; 21 local file references checked for existence, exact size and SHA-256 with **0 errors**. The remaining deleted/invalid item has no path.
- All 22 records have `t1_eligible=no`; **0/10 T1 accepted**, **0/20 additional signed contracts accepted**. Five development contract templates with 234 annotated clauses are separate and do not count.
- Categories: 2 REGISTERED_LOCAL_TO_ANNOTATE, 15 HOLD_*, 1 LOCAL_DEV_HOLD_REDISTRIBUTION, 3 EXCLUDED_*, 1 REMOVED_*.
- `data/raw/contracts/` holds 13 local files, six tracked in Git. Raw file count is not the number of accepted, executed contracts.
- The intake plan and its Superpowers SDD ledger refer to 34 manifest rows on an earlier branch; the authoritative **current manifest has 22**. Do not create dummy records to balance historical numbers.

## Official legal reference checks and boundaries

| Source | Official URL | Evidence and consequence |
| --- | --- | --- |
| Labor Code 45/2019/QH14, effective 2021-01-01 | https://vanban.chinhphu.vn/?classid=1&docid=198540&pageid=27160&typegroupid=3 | Government-signed PDF printed pp. 12, 15–16 inspected. Article 31: return after suspension; Article 36: employer unilateral termination; Article 38: cancellation of unilateral termination. A reference in HDLD003 to Article 38 for employer termination is a suspected wrong citation to review; preserve original raw and labels. |
| Consolidation 18/VBHN-VPQH, 2026-02-12 | https://vanban.chinhphu.vn/?classid=0&docid=217002&pageid=27160 | Official consolidated publication verified. Public Cong Bao PDF pages printed 34, 35, 37 and 38 were visually checked for Articles 31, 33, 36 and 38; full article-by-article coverage and amendment applicability remain pending. Never set effective_from equal to consolidation publication date by default. |
| Personal Data Protection Law 91/2025/QH15, effective 2026-01-01 | https://chinhphu.vn/?classid=1&docid=214590&orggroupid=1&pageid=27160 | Enactment/effective date verified. Published PII-containing contract attachments do not by themselves prove authority for data processing and benchmark distribution; article-level legal review remains pending. |
| Decree 337/2025/NĐ-CP, effective 2026-01-01 | https://vanban.chinhphu.vn/?classid=0&docid=216284&pageid=27160 | Official signed PDF pp. 1–2 inspected; Article 3 defines electronic employment contracts with equivalent legal standing to paper agreements. This does not authorize bulk collection of others' signed documents. |
| Circular 08/2026/TT-BNV, effective 2026-07-01 | https://vanban.chinhphu.vn/?classid=1&docid=218200&pageid=27160 | Official PDF printed pp. 12–14 inspected: Articles 17–18 require personal data to be absent from public open data, and common/master data access to be requested in writing by eligible parties. Ministry e-contract portal is a possible lawful data-discovery route, not a public signed-contract corpus. |

## Concrete collection path

1. Inspect the publicly released open-data catalog of https://hopdonglaodong.moha.gov.vn/landing-page for eligible non-personal data. Do not use private accounts or undocumented APIs to obtain other parties' contracts.
2. Seek actual signed agreements from employers/contracting parties willing to authorize secure research processing, internal access and sharing of the de-identified derivative. Verify scope, retention and permissions before accepting any sensitive file.
3. Require per-document source page/file, original hash, executed-signature/boundary check, explicit lawful basis/reuse scope, restricted storage, duplicate/template family and holdout split. For T1, 10 truly independent original agreements must stay separate from D1/D2, prompts and training; the additional 20 may share a family but must be 20 separate executed agreements.
4. Complete PII removal on a **separate** derivative and independently inspect every visible page, copyable text, metadata, signatures and embedded objects. Obtain a second human reviewer's dated sign-off. Only then admit to evaluation datasets.
5. Ask a qualified legal reviewer to verify contractual obligations against applicable primary-law version, exact effective dates and referenced article/clause/point. The group runtime currently covers only Labor Code Articles 20–21; these references do not imply expanded runtime coverage.

## Pending approvals and risks

- No recorded permission for any held signed source to be processed/shared as a derivative; no independent redaction/reuse reviewer sign-off.
- Lawstronaut validation was unavailable in the current tool registry; the source checks above are limited primary-document spot-checks, not a full legal opinion.
- N2 assignment for corpus/retrieval/Data Graph in group PROGRESS is a proposal pending OI-04 group sign-off. Original MS-1 freeze milestone (2026-10-25) also requires group-level evidence.
- No candidate was accepted, sensitive material was published, or group repo/submodule was changed by this intake/source review.

## Direct source/data citation QC (2026-10-28)

- Local `data/processed/raw_text/HDLD003.txt` line 81 cites Article 38 of the 2019 Labor Code for the employer's unilateral-termination right. The signed 2019 enactment puts that right in **Article 36**, while **Article 38** governs withdrawal of unilateral termination.
- The same raw text at line 85 and processed row `HDLD003_C044` cite **Article 33** for a worker returning after suspension; the official 2019 enactment covers return after suspension in **Article 31**, while Article 33 concerns modification/supplement to an employment contract.
- Across 234 current clause rows, a narrow automated scan for references to Articles 31/33/36/38 found only `HDLD003_C044`; it is **not** a full legal risk audit. Both mismatches are source-text QC findings, not grounds to rewrite the historical input or silently change annotation labels. They need version-aware law review and explicit risk findings.
- Public Ministry portal landing page and document catalog show platform features and legal/guidance documents; the browsed public pages did **not** list a downloadable corpus of independently licensed, de-identified signed agreements. Pursue lawful source-holder contributions/access decisions before treating this as an intake source.

## Unit-level intake gate added 2026-10-28

- The new `data/intake/contract_unit_review_queue.csv` enumerates **10 historically reported signed units** with 1-based PDF spans: seven An Giang (one family), one Quảng Ngãi GSP, one Quảng Ngãi Việt Mỹ and one VIMDA Long Châu. Four local source PDFs have 50, 19, 22 and 6 pages respectively (checked by `pypdf`). They need fresh human verification; all remain HOLD.
- The gate in `scripts/validate_intake_gate.py` checks linked source hash/size, evidence path, second reviewer, derivative hash, declared permission, and template/split integrity for claimed acceptance. Five focused tests cover both allowed and denied cases. Structural checks cannot substantiate a human permission decision, visual redaction, or legal opinion.
- `docs/CONTRACT_SOURCE_HOLDER_REQUEST_AND_REVIEW.md` supplies the lawful-source request and independent review process. Counts still **0/10 T1 and 0/20 additional** until each unit passes all gates.

## Fresh integrity and admission-gate verification — 2026-10-28

- Recomputed SHA-256 and byte size for **all 21 manifest rows with local files**: 21/21 matched; the twenty-second row is a removed/invalid document with an empty file path. This is a byte-integrity check, not verification of legal collection rights or contractual signatures.
- Checked all ten queued PDF page spans against their four original files (50, 19, 22 and 6 pages): **all spans in bounds, no duplicated or overlapping page spans**. No clause content or personal identifiers were emitted into this report. PDF page counts do not prove the historical signature findings.
- Hardened `scripts/validate_intake_gate.py` to reject out-of-bounds PDF spans, overlap within a source PDF, a purported redacted derivative identical to its original, and rights-evidence paths outside the project's ignored `data/intake/restricted/` or `data/intake/private/` locations. The validator inspects declared statuses, file paths and hashes; manual authorization, de-identification and legal decisions remain mandatory.
- Ran the full project test suite: **38 tests passed**, including nine intake-gate cases; `python scripts/validate_intake_gate.py` still reports **10 HOLD, 0/10 T1, 0/20 additional**. No push/merge or submodule change occurred.

### Quantified sourcing gap and next admissible actions

- The existing ten leads comprise seven agreements in one An Giang template family and only three other reported agreements. Even if each lead were eventually accepted, at most **four** of these ten could be independent T1 samples if all three other agreements prove different from one another. At least **six more independent T1 families** are therefore needed under this best-case assumption.
- The two targets must use **30 distinct signed agreements in total** (ten Tier 1 plus twenty additional, no double counting). With ten unresolved leads, at least **twenty additional distinct signed leads** are still required even in the best case. Additional agreements from the same employer may contribute to the 20, subject to rights, individual-document identity and leakage controls.
- First collect grant-of-authority and lawful processing evidence for the four existing source PDFs through the source-holder form; obtain fresh signature/contract-boundary review only within authorized processing. Pursue at least six independent contract families and twenty distinct agreements through consenting employers or authorized contributors. Create de-identified derivatives and obtain *another human's* dated QA decision before assigning accepted status. For legal gold, request qualified article-level, effective-date-aware review; the named Lawstronaut/Legal Data Hunter tools were not discoverable in this turn's Codex tool registry.

## Source-reference queue for legal reviewer — 2026-10-28

- `scripts/audit_legal_citations.py` generates `data/intake/legal_citation_review_queue.csv` from available local raw text and annotation **notes**. It emits only contract IDs, source-file hashes, file/line/offset, referenced article numbers and clause IDs; it **does not export source paragraphs or personal information**. Rerun after any raw-text or `clauses_v06.csv` change.
- The current scan located **13 occurrences in raw text across 7 contract IDs**, plus **one distinct reference in an annotation note** (`HDLD004_C043`, article 11): **14 review items** in all. These are string-pattern locators, and some references may refer to the contract's own articles rather than legislation. The scan does not cover references written without the literal word `Điều`, image-only scans, or relevant laws not explicitly cited in contract text.
- Two high-priority suspected mismatches remain: `HDLD003.txt:81` (article 38 versus candidate article 36 regarding employer unilateral termination) and `HDLD003.txt:85` / `HDLD003_C044` (article 33 versus candidate article 31 regarding return after contract suspension). The referenced **2019 law** appears on the [official Government publication page](https://chinhphu.vn/?docid=198540&pageid=27160); the [official 2026 consolidated-text entry](https://vanban.chinhphu.vn/?classid=0&docid=217002&pageid=27160) must be checked against each contract's execution date and intervening amendments.
- All 14 items have `HUMAN_LEGAL_REVIEW_REQUIRED`; **zero law citations have been signed off by an independent legal reviewer**. In particular, the script neither certifies risk labels nor changes contract sources, clause annotations, applicable law or the T1 holdout.
- `python -m unittest discover -s tests -v` and `python scripts/validate_intake_gate.py` are the two relevant automated checks. Their passing result cannot establish source-holder authority, secure anonymization or expert legal verification.

## Source-holder permission work queue

`data/intake/source_holder_outreach_queue.csv` now identifies **14** held PDF source receipts: the original four groups behind ten historically reported signed-document leads plus ten additional already-manifested PDF sources triaged separately in `data/intake/additional_signed_lead_triage_2026-10-28.csv`. The accompanying `source_contact_routes_2026-10-28.csv` maps **17** public referral routes, including a separate Hai Phong city portal route for a PDF on city CDN whose originating publisher is unknown. The contacts are not rights holders by default. Each entry is `NOT_SENT`; **no permission request has been sent or consent implied**, and none of the ten newly triaged PDFs has any independently verified executed unit. The relevant documentary evidence must be stored separately, in restricted local storage. Public Ministry e-contract platform descriptions explain controlled stakeholder access but provide no basis to treat individual signed employment contracts as an open research dataset.

## 2026 consolidated Labor Code: targeted follow-up evidence

- The Government's official [18/VBHN-VPQH publication](https://vanban.chinhphu.vn/?classid=0&docid=217002&pageid=27160), issued **2026-02-12**, links the [Cong Bao signed PDF](https://congbaocdn.chinhphu.vn/180507251028987904/2026/3/5/468971-1772684381_v1_1772690833_signed.pdf). The PDF opening states that Labor Code 45/2019/QH14 entered into force 2021-01-01 and identifies subsequent amending enactments, including different effective dates. A consolidation is an aid to identifying applicable text, not an independent new effective date for every provision.
- Visual inspection of **printed page 34 / PDF page 13** confirmed Article 31 covers returning to work after suspension. **Printed page 35 / PDF page 14** confirmed Article 33 covers modifying/supplementing a contract. **Printed page 37 / PDF page 16** confirmed Article 36 covers the employer's right to unilaterally terminate. **Printed page 38 / PDF page 17** confirmed Article 38 covers withdrawing unilateral termination. These headings remain consistent with the already-reviewed 2019 enactment for the two HDLD003 citation candidates.
- **Status remains `HUMAN_LEGAL_REVIEW_REQUIRED`** for both citations and all other locator rows. The source snippets, signing date, parties, complete clauses, effective-time history, and any exceptions require qualified human analysis. No historic raw text or clause annotation was changed, and this focused cross-check is not a full legal-risk determination.
- Codex Security finished a **static nine-script review** for the local source-to-output workflow at revision `80452e4`; it reported **one low-severity potential PII export issue** (`scripts/export_highlight_payload.py` and `scripts/build_highlight_preview.py` can include unredacted full text in JSON/HTML). The attack path requires manual processing and sharing; no actual leak was established. Before admitting signed personal-data sources, require redacted, authorized derivatives and independent signoff, and apply release-gate protections to any distributable export.

Follow-up hardening in the current **uncommitted working tree**: JSON exports now
fail closed for signed-unit IDs unless the source, rights, redaction, derivative
hash and independent reviewer pass the intake gate. Approved exports read only
the exact reviewed `.txt` derivative from `data/processed/approved/`; unreviewed
`raw_text/` is never substituted. Historical highlight development IDs require
`--local-fixture` with a frozen SHA-256 allowlist. HTML previews write only
under Git-ignored `data/intake/private/`; new generated raw text, approved
derivative work, and HTML previews are Git-ignored. This is a technical privacy
boundary, **not** authorization to publish, legal approval, or evidence that any
new signed contract has passed intake. The frozen security scan remains a report
of revision `80452e4`, not a fresh assessment of these local edits.

Local verification after hardening (2026-10-28): `python -m unittest discover -s
tests -q` passed **47 tests** (including signed-unit PII canary/HTML export
guards). `python scripts/validate_intake_gate.py`: **10 queued / 0 T1
accepted / 0 additional accepted**. `data/intake/legal_citation_review_queue.csv`
still has **14 legal-reference locators, all needing human legal review**.
These tests cover code behavior and structural evidence checks; they do not
constitute legal findings, independent signature checks or permissions.
