# WP1 RC01 status and integration boundary — 21/11/2026

This report supersedes the current-status and reviewer-governance statements in the historical scope report of 14/11. Its metric numbers remain historical snapshots, not newly measured scores.

## Approved local artifact

Owner approved the revised RC01 artifact via conversation on 20/11/2026 under `OWNER_SINGLE_APPROVER_AI_ASSISTED_V1`. AI checks support that decision; they are not additional human reviewers or proof of a digital signature.

- Corpus version: `legal_corpus_2026-11-20_v2_wp1_rc01`.
- 30 provisions across Articles 13–17, 20–22, including three structural parent nodes. This is eight articles, not 30 articles.
- Two manual `REFERS_TO` edges plus 13 generated `PARENT_OF` edges. Four unsupported manual edges were removed and two `GUIDES` edges held outside runtime.
- Nineteen mappings across nine clause labels. Removing the only `WORKING_CONDITIONS` mapping leaves nine, not ten. Clause-label coverage must not be added to risk-label counts to claim coverage of all 21 risk labels.
- All three data checksums are bound by the Owner decision sheet and release receipt. The approved loader accepted the local release with `allow_draft=False`.
- TT10 is metadata-only/HOLD; N145/N293 remain deferred to WP2 and the N399 records retain their declared future-effectivity hold. None is an active runtime source in RC01.

The manifest/receipt is Owner approval of this bounded artifact, not retroactive approval of corpus v1, comprehensive current-law certification, proof that Owner personally read every PDF page, or acceptance of a complete product model. Source usage is `INTERNAL_REPO_ONLY`; this PR contains metadata, not legal-source PDFs, raw law text, contract text, Gold, or the private conversation transcript.

## What remains open

The source verifier still reports `PENDING_MANUAL_REVIEW_SCAN_PDF` for the two scanned PDFs; that machine result must not be rewritten to PASS when Owner approves. The approval record is separate. Dev M8 for RC01 graph/weights has not been measured. D2 clause-label Gold is not approved by the corpus decision; the 250-row review queue remains a separate gate. T1/T2 stay held out and must not select rules, prompts, mappings or graph edges. The 17 historical scope exceptions are a restricted post-freeze adjudication task, not a quota for adding law or positive Gold.

## Delivery order

1. PR #22: scope/status correction only.
2. PR #23: nine-source register and text-free RC01 release metadata; preserve the existing candidate queue.
3. PR #24: D2 converter supports the Owner-only mode explicitly while preserving the legacy dual-review default; no Gold is written by preparing or merging this code.
4. Once actual Data commits exist on remote, use their verified SHA for Pipeline pinning. Do not pin temporary local audit SHAs. Review the Pipeline release/runtime/startup integration and run Dev evaluation separately.

PR #24 currently targets the PR #23 branch. After #23 merges, verify its new base and retarget #24 if needed. Local conflict simulations and GitHub mergeability are evidence for the inspected heads only; recheck after remote changes.

RC01 approval does not authorize an automatic push, PR comment, merge, or public release of restricted files.
