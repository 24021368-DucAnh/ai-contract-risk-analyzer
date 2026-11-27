# N2 Pipeline follow-up · 27 November 2026

These files are review artifacts for the Pipeline repository. PR #26 is a draft in the Data repository. Pipeline integration has its own branch and checks.

## Review and replay

Use an isolated Pipeline checkout at `d930e0092fa27f92cabf2ef8161d9fab86c60272`. Decode and verify the three files in [the verification receipt](n2_pipeline_offline_verification.json). Run `git apply --check` and `git apply` for each patch in the listed order. When using a Git setting that flags CRLF as trailing whitespace, use `git -c core.whitespace=cr-at-eol apply` to preserve the originally verified bytes. Keep the Data gitlink unchanged.

1. [Original 24-file source patch](pipeline_code_only.patch.b64). The original manifest is still authoritative for this step.
2. [D2 label whitespace](n2_d2_label_whitespace.patch.b64). The Dev loader trims whitespace around each label before comparing it to the exported Gold list, matching the converter. Label order, reviewer approval, taxonomy rules, checksums and source offsets remain enforced. Two synthetic regressions cover three ordered labels and `OTHER` alone. Both failed before the change and passed afterward.
3. [D1 fixture gates](n2_d1_fixture_gates.patch.b64). The integration test module requires D1 fixtures only for the three cases that read them. The synthetic offset test and the T1 ID rejection test can run without Data. The T1 rejection test uses an empty temporary directory and passes before file access.

## Offline results for all three patches

- Without Data fixtures, **1,196 passed**, 18 skipped and four model tests deselected. The D1 clause-run module went from five skips to two passes and three skips in this profile.
- With the D1-only fixture profile, **1,216 passed**, one skipped and four model tests deselected. The fixture bytes came from the Data commit pinned by Pipeline, `d9b393efa7b51eef55326bf808cea352891348c5`. The profile uses only four D1 inputs and 183 D1 rows from each versioned annotation CSV. It was assembled and removed in a temporary directory. It is a scoped regression profile.
- In the original set of 20 skip entries, 18 ran as individual passing cases. The segmenter placeholder expanded to four passing cases. The remaining skip is the blank-template PII test that needs the HDLD005 held-out input. The gate test references the ID alone. No held-out document was loaded.
- Ruff passed. Fake-provider smoke produced four clauses, two risks, two citations and zero schema errors. The bound D2 Dev loader verified 250/250 adjudicated rows across four documents. Actual provider calls were zero.

The [verification receipt](n2_pipeline_offline_verification.json) records the patch hashes and each original skip disposition. The test results are N2 technical self-review. The integration decision stays with the Pipeline maintainer. No change to runtime defaults, legal decisions, Gold or held-out scope is recorded here.
