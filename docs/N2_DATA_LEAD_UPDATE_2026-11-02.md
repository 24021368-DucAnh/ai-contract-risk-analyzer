# N2 Data Lead update — 2026-11-02

This update records local source-acquisition and structural-QC work. It does
not represent legal review, accepted benchmark data, or a release-ready law
corpus.

## Work completed

- Added direct Government-portal source checks for the Labour Code 45/2019,
  consolidated text 18/VBHN-VPQH, Decree 145/2020, Social Insurance Law
  41/2024, labour-penalty Decree 12/2022, and minimum-wage Decrees 74/2024
  and 293/2025. Drafts remain monitoring-only. Details and source links are in
  `LEGAL_SOURCE_DISCOVERY_2026-11-02.md`.
- Downloaded three official PDFs into ignored restricted storage. The new
  receipt records match file hashes, sizes and page counts. Law 41/2024 has a
  searchable text layer (193,247 extracted characters); Decrees 12/2022 and
  293/2025 do not.
- Generated UTF-8 OCR candidates for VBHN 18/VBHN-VPQH (86 pages), Decree
  293/2025 (14 pages), and Decree 12/2022 (83 pages). All 183 page markers are
  ordered and non-empty, each source hash matches its receipt, and no Unicode
  replacement characters were found. All candidates remain unproofread.
- OCR detected 215 distinct article numbers from 1–220 in VBHN 18; 76–79 and
  166 were not detected. This is only heading detection.
- Generated a metadata-only review queue with 220 rows, one per expected
  article number. It records detected heading counts/pages and marks every row
  `PENDING_VISUAL_REVIEW`; it contains no provision text.
- Built an additional restricted hierarchy index from the UTF-8 OCR candidate:
  1 document, 220 article nodes, 592 clause candidates, and 252 point
  candidates (1,065 rows total). Every row remains `PENDING_LEGAL_REVIEW`;
  five article placeholders require manual search. The index stores identifiers,
  page references, counts, source hash and evidence labels only; it does not
  store provision text or modify the reviewed legal corpus. OCR numbering is a
  review aid and has not been confirmed against the PDF.
- Extended OCR and structural indexing to the original Labour Code 45/2019 and
  Decree 145/2020 source PDFs: 83/83 and 122/122 pages produced non-empty OCR
  candidates. After tightening heading detection to reject line-start article
  references, their metadata-only indexes contain respectively 993 nodes
  (220 article IDs, 551 clause candidates, 221 point candidates; 15 article
  placeholders) and 821 nodes (115 article IDs, 355 clause candidates, 350
  point candidates; 8 placeholders). Older loose-regex indexes are retained
  separately and marked `broad_heading_v1`.
- Freshness check found [Decree 283/2026/NĐ-CP](https://vanban.chinhphu.vn/?docid=218871&pageid=27160&typegroupid=4),
  issued 2026-07-15 and effective 2026-09-10. A [Government notice](https://baochinhphu.vn/lao-dong-nuoc-ngoai-duoc-tra-them-1-tien-luong-thay-bao-hiem-that-nghiep-10226101211144485.htm)
  confirms Decree 12/2022 ceased to apply on that date and points to transition
  provisions. The signed 100-page 283 PDF was downloaded to restricted storage
  and receipted. Its 100/100-page OCR candidate and metadata-only index now
  contain 1,046 rows (68 article IDs, 312 clause candidates, 665 point
  candidates); Article 33 needs manual search. Treat 12/2022 as a
  historical/time-bounded candidate, not a current default. No effectivity
  intervals or approved provisions were changed.
- The receipt table now covers six OCR candidates. Every new index row remains
  `PENDING_LEGAL_REVIEW`; indexes contain no provision text and do not alter
  the DRAFT corpus.
- Also built restricted metadata-only indexes for the previously acquired
  Decree 12/2022 (827 rows: 64 articles, 311 clause candidates, 451 point
  candidates) and minimum-wage Decree 293/2025 (57 rows: 5 articles, 43
  clause candidates, 8 point candidates). Both remain unproofread candidate
  structures; Decree 12 is time-bounded historical input after 2026-09-10.
- Added a public-metadata receipt for all six structure indexes at
  `data/intake/legal_ocr_structure_index_receipts_2026-11-02.csv`: **4,826
  rows** total. It records each index hash/size, OCR-candidate hash, expected
  article IDs and manual-search placeholders. Every index and node remains
  pending visual/legal review.
- Completed the D1 inventory/scope decision from the local dataset evidence:
  D1 stays HDLD001–004 (39+40+61+43 = 183 clauses) to match BRD §8.2;
  HDLD005's 51 v06 clauses remain supplemental and outside D1. A fresh scan
  of the four canonical texts found 0 emails, 0 continuous 9–12 digit strings,
  and 0 phone-pattern matches. This does **not** prove de-identification:
  names, addresses, image/signature content, metadata and indirect identifiers
  have not had manual/independent review. Raw source files remain unverified
  for privacy and rights; no data were admitted to gold or T1. BRD unchanged.
- Closed the N2-scoped offline evaluation harness item in the sibling pipeline
  repo: strict `load_dataset`, M3a/M4/M5 metrics, paired M8 metric and callback
  runner. **32 focused tests passed**. C-18 overall remains open; this does not
  include production wiring, M1/M2/M6/M7 ownership, approved gold or D1/T2 runs.
- Recorded hashes, bytes, page markers and text-character counts for all three
  OCR candidates in `data/intake/legal_ocr_candidate_receipts_2026-11-02.csv`.
- Fixed the OCR subprocess decoder to read UTF-8, with a regression test. The
  first incorrectly decoded Labour Code output is retained in restricted
  storage with `_cp1252_INVALID` in its filename and is not used downstream.

## Checks

- `python -m unittest discover -s tests -q`: **79 tests passed**.
- Ruff could not be run in this checkout because neither the `ruff` command
  nor the Python `ruff` module is installed. Python compilation and the full
  test suite passed.
- `git diff --check`: **passed**; Git reported existing LF/CRLF normalization
  warnings on pre-existing working-tree files.
- OCR receipts now cover **5 candidates**; each source PDF hash matches its
  receipt, all page markers are ordered/complete, and every output remains an
  unproofread candidate.

## Progress and gates

The separate pipeline checklist is now **7/19 = 36.8%** by its documented
checkbox-count method: the D1 inventory/scope and N2 offline-evaluation items
were closed with the evidence and limits above. The OCR/index and legal-source
expansion do not close legal approval, corpus, gold, privacy, or benchmark items.

The legal corpus remains `DRAFT`. No provisions, effectivity intervals,
manual graph edges, label mappings, D1 gold labels, or accepted T1/T2 records
were changed. Current intake remains 0/10 accepted T1 and 0/20 accepted
additional contracts. OCR, source presence and structural queue coverage do
not establish reuse rights, privacy approval, legal accuracy, or benchmark
readiness.

## Follow-up: provision review queue

The pipeline corpus working tree contains 16 unique provision candidates across
Articles 13–17 and Article 21, plus five label-map entries. A metadata-only
review queue was generated at
`data/intake/restricted/legal_corpus_review_queue_2026-11-02.csv` from those
provisions and the local OCR candidate for VBHN 18/VBHN-VPQH. All 16 rows have
source page hints and remain `PENDING_VISUAL_LEGAL_REVIEW`; 7 normalized exact
text matches and 9 non-matches are navigation signals only. The queue contains
identifiers, hashes, page hints and blank reviewer fields, not provision text.
The OCR file itself is marked unproofread, so no mismatch was corrected and no
legal text, effectivity interval, corpus file or manifest checksum was changed.

The new queue builder has 3 focused tests; the full data-repository suite now
reports **93 tests passed**. Ruff is unavailable in this Python environment;
`py_compile` and `git diff --check` passed (Git emitted existing line-ending
normalization warnings). These checks do not close X-03 or approve the draft
corpus.

## Follow-up — C-13(a) source check and X-10 kickoff — 2026-11-02

Subsequent work in the sibling pipeline repository added one `REFERS_TO` edge
from Article 14 clause 1 to clause 2 after visual verification on page 7 of
the official 18/VBHN-VPQH PDF. The corpus remains `DRAFT`; this records only a
literal cross-reference check, not current effectivity or independent legal
approval. The sibling pipeline audit records the C-13(a) first technical batch
as closed and 50 corpus/graph tests passing.

The X-10 kickoff is also closed at its stated start-only scope: source triage,
rights/privacy intake procedure and outreach queues are prepared. The intake
manifest has 22 unique candidates, all `t1_eligible=no`; no permission request
was sent and no contract was accepted into T1. The intake-gate tests pass 9/9.
The full X-10 target (at least 10 rights-cleared and de-identified contracts)
remains open. The current sibling-pipeline N2 checklist count is **11/19 =
57.9%**, using the same Weeks 1–7 top-level-checkbox method; this is not legal
readiness or completion of the whole project.

The D1 segmentation review queue currently covers 183/183 reviewed v06 clause
IDs with valid candidate spans and no missing rows. Reviewer ID/note fields
remain empty on all 183 rows, so no segmentation gold or M1 score is claimed.

The six-source structural-index review also found and repaired a source-hash
mismatch in three VBHN visual-review log rows. Those pages were re-rendered
from the receipt-matched PDF; the corrected log now passes a regression test.
This improves source provenance only: the OCR index is unchanged and remains
pending legal review.

## V07 preview span-audit follow-up â€” 2026-11-02

Fixed `scripts/audit_preview_dataset.py` so newly added rows with incomplete source metadata still undergo code-point bounds and EXACT-text checks against available local raw text. Missing metadata remains a release blocker and is no longer treated as a reason to skip span validation.

A re-audit of the local v07 preview found 72 `NEEDS_REVIEW` rows with structurally valid spans: HDLD010 (23), HDLD012 (36), and HDLD013 (13). These are counted as `span_structural_only`; they have no accepted source metadata. The audit reports 234 spans validated with existing metadata, 72 structurally checked without it, 0 span errors, and 0 structural errors. The preview remains blocked by 12 release-blocker groups, including pending annotation and missing provenance for the new rows.

The regression test confirms valid spans are counted while metadata blockers remain, and invalid bounds increment `span_errors` and `structural_errors`. The full data-repository suite passes **94 tests**. No v07 row, contract metadata, or release status was changed. This closes no legal, privacy, rights, or human-review gate and does not change the N2 plan count (11/19).
