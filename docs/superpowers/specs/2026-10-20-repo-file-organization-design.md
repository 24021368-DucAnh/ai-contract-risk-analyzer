# Repository File Organization Design

Date: 2026-10-20
Status: awaiting user review
Repository: `ai-contract-risk-analyzer`
Branch: `codex/contract-source-intake`

## Goal

Make the repository easier to navigate by establishing clear current-document entry points, reducing duplicated intake narrative, using consistent names for active documentation, and correcting stale location/count guidance. Preserve dataset provenance and all existing user work.

## Current structure

- `docs/README.md` is already the Data Lead documentation entry point.
- Current guidance is in `docs/`; historical reports and taxonomy snapshots are in `docs/archive/reports/` and `docs/archive/taxonomy/`.
- `data/intake/manifest.csv` tracks candidate-level intake metadata; `docs/data_sources.md` tracks project contract IDs and source context; `docs/dataset_schema.md` describes dataset files and schemas.
- `data/intake/README.md` includes the intake workflow plus a long chronological narrative that overlaps the manifest, data-source catalog, and archived QC reports.
- `docs/README.md` currently states nine local raw contracts, while the inspected workspace has 13 raw contract files (six tracked and seven local-only).
- `docs/HIGHLIGHT_HANDOFF.md` is the only active document using uppercase naming; current links reference that path.
- Versioned clause CSVs, split manifests, raw documents, and ignored local/private materials have provenance, runtime, privacy, or test significance.

## Design

### 1. Keep stable data and code paths

Do not move or rename files under `data/raw/`, `data/processed/`, `data/splits/`, `scripts/`, `tests/`, or `backend/`. Existing scripts, tests, offsets, metadata, and provenance refer to these paths. Do not alter or delete source contracts, restricted/private files, local-only annotations, `.superpowers/`, or the existing untracked contract-intake plan.

Keep `clauses_v01.csv` through `clauses_v06.csv` and split snapshots in place. They are historical dataset artifacts and some are read by tests or reconstruction workflows. Keep the existing `docs/archive/` tree and its archived filenames intact.

### 2. Define document ownership

- `docs/README.md`: navigation, current project status, canonical pointers, and links to archived history.
- `data/intake/README.md`: intake rules, the immediate queue state, and pointers to the manifest and detailed archived screening history.
- `data/intake/manifest.csv`: authoritative per-candidate intake receipt/status/hash/path record.
- `docs/data_sources.md`: project-level source/contract ID catalog and accepted/held status for project raw contracts; avoid duplicating candidate screening narratives already in the intake manifest/history.
- `docs/dataset_schema.md`: schema and versioned-data semantics only; status summaries should link to the index rather than repeat it.
- `docs/annotation_guideline.md` and `docs/clause_taxonomy_v03.md`: active annotation rules and label definitions; historical taxonomy snapshots remain archived.
- `docs/highlight_handoff.md`: offset and rendering handoff guidance.
- `docs/archive/reports/`: immutable historical QC, handoff, and progress evidence.

### 3. Shorten current intake guidance without losing history

Before rewriting the intake README, screen its full contents for personal identifiers, confidential contract text, and secrets. Preserve non-sensitive historical content in a dated archive snapshot under `docs/archive/reports/`; if the screen finds sensitive material, redact that material in the archive and retain only non-sensitive provenance/status pointers. Then reduce `data/intake/README.md` to the intake workflow, present queue/status summary, links to the manifest, data-source catalog, relevant QC reports, and explicit no-PII/restricted-data rules. The manifest remains authoritative for candidate-level status; historical narrative remains available in the archive and existing QC reports.

### 4. Standardize active document naming and correct navigation

Rename only `docs/HIGHLIGHT_HANDOFF.md` to `docs/highlight_handoff.md`, then update every tracked reference. Because Windows file systems are commonly case-insensitive, use a temporary intermediate filename for the case-only rename and verify Git records the final lowercase path. Keep archived filenames unchanged to preserve historical identifiers and avoid needless churn. Update `docs/README.md` and `CONTRIBUTING.md` as needed so the index consistently points to the canonical active documents.

Correct the `docs/README.md` count to distinguish 13 local raw files from six Git-tracked and seven local-only files, and retain the current annotation and T1 eligibility caveats. Do not treat the 13 local files as accepted T1 examples.

### 5. Preserve local and Git state

Keep all pre-existing modified files and untracked user content. Do not push, pull, create a PR, merge, or rewrite Git history. Do not delete tracked or restricted data. Remove only generated Python bytecode caches (`scripts/__pycache__/`, `tests/__pycache__/`) after confirming they remain ignored and can be recreated; leave `.superpowers/` state untouched.

## Verification

After implementation:

1. Search all tracked documentation/code for the old handoff filename and verify no stale reference remains.
2. Verify all new Markdown links resolve to existing files and all intake paths remain unchanged.
3. Parse `data/intake/manifest.csv` and `data/contracts_metadata.csv`; confirm no candidate status or dataset row was changed by documentation cleanup.
4. Run `python -m unittest discover -s tests -p test_source_intake.py -v` and any repository test that directly imports or reads a renamed documentation path.
5. Run `git diff --check`; inspect the complete diff and confirm there are no deletions of user data or PII-bearing files.
6. Confirm working branch and pre-existing modifications are preserved; no remote Git operation is performed.

## Security scope and limitation

This design changes documentation organization only and does not modify backend behavior, application code, data contents, or access controls. The latest available Codex Security scan is the completed scan for revision `402e662b6f9a6217c54f9ee380c5ab3de11f038c`; it reported a Medium CWE-400 PDF upload resource-exhaustion finding and excluded binary/private contract contents. This session does not expose the Codex Security scan-start/preflight tools, so no new whole-repository scan can be claimed for the current worktree. File organization must not be represented as remediation of that finding.

## Self-review

- No dataset or executable path is moved, so offsets and runtime import paths remain stable.
- The archive preserves non-sensitive historical intake notes; a pre-copy PII/secret screen prevents creating another tracked copy of any sensitive content.
- Candidate statuses remain in one manifest; raw-contract project IDs remain in the data-source catalog.
- The handoff rename accounts for case-insensitive Windows file systems.
- Local-only materials and all pre-existing edits remain untouched.
- Security scan status is explicitly dated and scoped; it is not presented as a fresh scan.
