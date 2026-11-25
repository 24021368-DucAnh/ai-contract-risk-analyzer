# Data Lead source integration — independent review handoff

Base: main d930e0092fa27f92cabf2ef8161d9fab86c60272. This PR contains the 24 prepared source/test/plan files plus this handoff. The base tree was checked against GitHub blob hashes, then the code-only patch was replayed without editing protected worktrees.

Behavior to review:

- Fully source-pinned D2 clause Gold supports an explicit Dev-only M8 oracle; primary classifier and risk Gold stay separate.
- Clause-label alignment and risk-support audits preserve source offsets and report supported labels without forcing positives.
- WP2 preparation retains HOLD and controls for broad/delegated mappings; candidate corpus does not become an approved release automatically.
- Approved internal corpus installation validates the source/version/checksum gate and refuses overwrite; source rights and effective-date receipts remain prerequisites.
- Local-provider usage normalization and bounded risk response schema remain subject to provider contract and cross-field checks. These inherited integration changes are included because the frozen candidate was verified with them.

The separate Data converter PR rejects excessive/mixed OTHER clause labels. Review that dependency separately; this PR does not change the ai_pipeline/data gitlink.

Independent review is pending. Please examine provenance validation, path/write boundaries, compatibility of opt-in oracle results, legal effective windows, and provider schema/usage behavior. Self-review and automated tests do not establish human source review or legal acceptance.

## Remaining data and evaluation gates

WP2: four source-rights records, scan transcription checks, effectivity/amendment evidence, and label/citation decisions remain open. Risk migration: rubric/taxonomy compatibility and contextual decisions remain open. Sang/Nhật delivery requires complete manifests and rights/annotation evidence.

D3 has a separate internal AI-reviewed Dev reference (20 pairs/10 families), authorized by the Owner. Its labels and sources are not published in this PR. M10 is NOT_MEASURED until actual frozen predictions arrive for both roles and both graph modes. The author self-reviewed D3; there is no independent or direct human per-item annotation claim. Provider execution/budget receipts require a separate audit.

T1/T2 remain closed until final corpus/model/prompt/taxonomy/Gold/evaluator/config freeze and rights/protocol readiness. Local engineering freeze is not final product acceptance.

Historical plans in this change describe earlier no-push checkpoints. Current Owner instructions explicitly permit publishing review branches and PRs. No merge, runtime activation, new Gold migration or legal release is performed here.
