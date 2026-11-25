# D2 clause Gold converter — review handoff

This source-only change rejects ambiguous clause annotations before exporting a new D2 Gold version: at most three distinct labels are accepted, and OTHER cannot coexist with a substantive label. Segmentation/source hashes, complete packet coverage, approved reviewer identities and dates remain required.

Validation on the exact proposed converter/test bytes: 22 converter tests passed; Ruff passed for both changed Python files. These tests use temporary synthetic sources. The full Data repository suite was not rerun against this public-only snapshot because its historical local fixtures and intake/release resources are separate dependencies. Prior reference-fixture regression (126 passed, 3 skips) is historical context, not a new result for this PR.

Review focus:

- Preserve both supported approval policies and reject AI aliases as human reviewer identities.
- Reject duplicate, unknown, excessive labels and OTHER mixed with other labels before writing outputs.
- Preserve complete source/geometry/packet bindings and existing Gold; do not change labels to improve model scores.

Independent review is pending. Approval of this code does not approve an annotation packet or a new taxonomy migration. D2 Risk Gold remains on risk_taxonomy_v01 until its separate compatibility and contextual review is complete.

No source contracts, labeled Gold, held-out inputs, usage-rights evidence or runtime pin changes are included. Current Owner authorization permits pushing this review branch and opening the PR; older no-push notes refer to prior sessions. Merge remains a separate reviewer decision.
