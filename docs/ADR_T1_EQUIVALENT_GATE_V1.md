# ADR: T1_EQUIVALENT_GATE_V1

Date: 2026-11-06
Decision: Approved as a project evaluation deviation by `DucAnh_N2`, `argon`, and `Minh_N1`, as attested in the owner's instruction.
Scope: Local academic evaluation only; no public redistribution of contract text.

## Decision

Use a ten-document composite evaluation gate alongside the unchanged BRD §8.2 original-contract intake gate. The composite consists of four owner-attested restricted real-world/internal documents (`HDLD010–013`), five public-template/stress-test documents (`HDLD005–009`), and one author-composed unsigned synthetic calibration control (`HDLD014`). The composite is reported as `10/10 ACCEPTED_UNDER_EQUIVALENT_GATE_V1`, never as ten independently verified original executed contracts.

The four restricted documents have local PDF hashes and matching document-number cues. Their signatures, external provenance, controller authority, processing basis and reuse rights have not been independently established by the automated validator. `T1_privacy_gold_v01` records reviewed PII spans for nine documents, but the Gold does not prove that all personal data was removed. Raw contracts and Gold remain local in Git-ignored storage.

`HDLD005` and `HDLD006` are a deliberate near-duplicate granularity ablation pair and must not be treated as independent documents in the `slice_unique_8` analysis. `HDLD007` is an out-of-corpus citation stress case with 2025/2026 references; Tier 1 citation coverage must be reported separately. `HDLD014` is a synthetic control with no real signature or personal data and is excluded from original-contract acceptance.

## Required reporting slices

- `slice_unique_8`: HDLD005, 007, 008, 009, 010, 011, 012, 013.
- `slice_t1_real_9`: HDLD005–013; the word `real` is a historical slice name and includes templates. Report 747 full label rows and 340 clean clause rows separately.
- `slice_composite_10`: HDLD005–014, including the synthetic control.
- T2: nine derived documents, 872 segmentation spans and 30 injected cases.

No T1/T2 Gold labels, injection labels or legal citations may enter prediction generation. Models/rules must be frozen using Dev data before reading Test Gold. Missing predictions or unsupported metrics remain `NOT_RUN`; never substitute Gold as predictions. Bootstrap uses 1,000 contract-cluster resamples with seed 0.

## Gate interpretation

`T1_EQUIVALENT_GATE_V1` is an owner-approved academic alternative for technical assessment. The original BRD §8.2 gate remains independently visible at its actual accepted count. This ADR does not assert legal compliance, independent source authentication, or equivalence to generalization on ten executed contracts.
