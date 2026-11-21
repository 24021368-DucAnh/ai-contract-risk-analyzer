# D2 clause-label review handoff — updated 21/11/2026

This PR adds an explicit `--approval-mode OWNER_SINGLE_APPROVER_AI_ASSISTED_V1` to the source-pinned converter. It does not adjudicate any actual D2 row, write Gold, or produce an M8 oracle score. Approval of the WP1 RC01 corpus is not approval of D2 clause labels.

## Preserved input and review boundary

The restricted 15/11 worksheet covers 250 D2 segmentation Gold spans, with 34 exact unique D1 matches offered only as suggestions and 216 unmatched rows. Those are historical packet counts; this PR does not alter the worksheet or fill decisions. Actual spans, source hashes, clause units and final labels must be reviewed before converting to a new Gold version. Exact matching alone, shared IDs or model predictions do not transfer Gold. T1/T2 held-out files stay outside this task.

## Owner-only mode

The CSV schema remains unchanged. For a genuinely reviewed row, put the single real Owner identifier in legacy `reviewer_n1`, leave `reviewer_n2` empty, and fill `adjudicated_labels`, `reviewed_on` and `decision` only after the Owner decision. The same Owner identifier must be used across all rows/documents. The flag makes these legacy columns unambiguous; never fill a second person or AI name. The converter rejects AI/placeholder identifiers, a nonempty second-reviewer field in this mode, mixed Owner identifiers, incomplete decisions, invalid labels, source/hash/span changes, duplicate/unknown refs and incomplete segmentation coverage. Keep `suggested_labels` as trace evidence.

The default `DUAL_HUMAN_REVIEW_V1` remains available for legacy callers and still requires two distinct valid reviewers. Selecting a mode does not approve the rows. The identifier filter rejects known AI/placeholder patterns, including punctuation and model-version suffixes; it is not independent identity authentication or proof that a human actually performed the review.

## Conversion steps (restricted local files only)

First run `python -m scripts.convert_d2_clause_review_to_gold --restricted-root <existing-restricted-root> --packet <actually-reviewed-csv> --output <new-restricted-output> --approval-mode OWNER_SINGLE_APPROVER_AI_ASSISTED_V1 --check-only` with the required .venv Python. The CLI additionally requires exactly 250 spans over the four configured D2 documents. An unreviewed worksheet must fail closed and write no Gold. Only after READY_TO_WRITE and Owner review should the same command be run without `--check-only`, to a new output directory under the restricted root.

The produced Gold/manifest explicitly records `approval_governance_mode`; the manifest binds the reviewed packet SHA and D2 source hashes. Tests use synthetic fixture strings, not actual D2 review or evidence of human Gold approval. M8 oracle and M1 unit-policy acceptance remain separate tasks.

## PR dependency

PR #24 currently targets the source-register branch of PR #23. Merge/review #22 -> #23 -> #24 and confirm the base after #23 merges. Do not copy temporary local SHAs into Pipeline. This package is prepared locally for review; it does not authorize push or merge.
