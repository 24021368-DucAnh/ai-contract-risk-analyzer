# Corpus v2 source review handoff — updated 21/11/2026

The nine-source register and `data/intake/corpus_v2_wp1_rc01_release_metadata_2026-11-21.json` now describe the bounded, locally Owner-approved RC01 artifact. They do not change the Pipeline runtime pin or import a source PDF, raw provision text, private decision sheet, contract text or Gold into this PR.

## Current scope and governance

RC01 has 30 provisions across eight articles, two manual REFERS_TO edges, thirteen generated PARENT_OF edges, and nineteen mappings across nine clause labels. It uses `OWNER_SINGLE_APPROVER_AI_ASSISTED_V1`: one real Owner decision, with AI checks recorded as support. The previous requirement to impersonate or find two additional reviewers is superseded for this Owner-approved workflow. Approval via conversation on 20/11/2026 is not a cryptographic signature or proof of personally reading every scan.

The four BLLĐ/VBHN source rows have `OWNER_APPROVED_WP1_RC01_SCOPE_ONLY` and `INTERNAL_REPO_ONLY`. Only the original BLLĐ, portal VBHN and Gazette PDF are active source IDs in the release receipt; Gazette DOCX is an approved comparison auxiliary. The machine verifier still marks the two scanned PDFs `PENDING_MANUAL_REVIEW_SCAN_PDF`; keep this separate from the Owner decision. TT10's local hash matches but fresh-download provenance is pending; keep it HOLD/metadata-only. N145/N293 are deferred, N399 MAIN/ANNEX keep the recorded future-effectivity hold. Their existing date/locality metadata is not reverified or activated by this PR.

## Preserved candidate intake

The public priority queue remains 160 text-free metadata rows (29 proposed articles, 86 clauses, 45 points) from the 15/11 packet, not 160 approved nodes. `scripts/build_corpus_v2_review_packet.py` and the restricted OCR/review sheet keep their existing schema. Legacy `reviewer_n2` / `reviewer_independent` column names do not require fake people under the later Owner policy; they are candidate-sheet fields, not the release receipt. Exact source text, article/clause/point identity, amendment chain, applicable interval, source hash and usage rights still need a real decision for each newly admitted provision. No OCR or hash alone grants approval.

The queue and original dates are preserved. This update imports the known local hash/decision metadata; it does not claim a new network download or a fresh comprehensive amendment audit.

## Next gates

1. Review and merge Data PR #22 then #23, preserving v1 and the candidate intake.
2. PR #24 adds explicit Owner-only mode to the D2 converter; corpus approval does not approve the D2 labels. Do not run a Gold write with a blank worksheet.
3. After Data has a real remote commit, pin that SHA in Pipeline and integrate the signed RC01 artifact through review. No temporary audit SHA is supplied here as a pin.
4. Measure M8/citation relevance on Dev, preserve baseline reports, and keep T1/T2 held out. Only after corpus/model freeze may reviewers adjudicate held-out scope and run a versioned held-out measurement.
