# T1 M2 closed-corpus metadata handoff — 2026-11-13

The versioned T1 M2 Gold v02 manifest is stored locally under ignored `data/intake/restricted/T1_m2_risk_gold_v02/`. Its source CSV stays under ignored `data/intake/private/m2_review_submissions_2026-11-13/`. Neither artifact is committed to public Git.

The exporter validates 1,494 role rows and records 3 adjudicated positives, 1,474 in-corpus verified negatives, and 17 named corpus-scope exceptions. The manifest includes each exception's role unit ID and offset span. The sync utility derives 95 segmentation-only T1 references by subtracting the 747 clause-label Gold IDs from 842 segmentation Gold IDs. It records 190 projected role IDs, but **zero of these appear in the 1,494-row M2 packet**. This distinction prevents treating 190 nonexistent CSV rows as M2 negatives or positives.

Pipeline M2 scoring merges exclusion regions at gaps of at most 15 characters within each document/role, and records excluded predictions and smaller partial-overlap warnings. T1 text is not read by the metadata utilities. Evaluation with T1 still requires passing the manifest's excluded regions to the scorer and preserving the held-out model/rule freeze.

Local test gate: exporter/context utilities compiled; exporter and D1 converter tests 5/5 pass. Data suite with one unrelated privacy test excluded: 138 passed and 2 subtests passed. The full Data suite currently fails during collection because `tests/test_convert_d1_privacy_review_to_gold.py` imports `_validate_privacy_gold`, which is absent from the connected pipeline checkout. This is an existing cross-checkout import gate, not a failure in the M2 metadata exporter.
