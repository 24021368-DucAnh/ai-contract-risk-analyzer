# Review routing by documented role

User requested role-based allocation on 25/11/2026. This routing applies to these work packages. The underlying PROGRESS/BRD table calls its allocation a proposal; this document does not fabricate group acceptance or close OI-04.

| Role | Person / GitHub | Scope now | Tracked work |
|---|---|---|---|
| N1 | Ngô Hoàng Nhật / sosadsonar | Clause/provider review; frozen Clause Dev outputs | #27 |
| N2 | Đức Anh / 24021368-DucAnh | Corpus/source bindings, Gold, retrieval and evaluation; fix reviewer feedback | #31; PR #25 and this handoff |
| N3 | Hoàng Phạm Anh Tú / AnhTuHoangPahm | Risk schema/rubric, migration compatibility, WP2 mapping semantics and frozen Risk predictions | #28 |
| N4 | Nguyễn Huy Minh / ghoulixia | Host full regression, installer/config integration, actual Pipeline PR | #29; assignee of PR #26 |
| N5 | Cao Khắc Phan Sang / ckpsang06 | X-10 intake, rights evidence and de-identification handoff; highlight only if canonical changes | #30 |

PR #25 needs actual N1/N3 review for the OI-10 label-policy boundary; N2 is the author/code owner and is not an independent reviewer. PR #26 is review-only: N4 integrates, N1 reviews Clause/provider, N3 reviews Risk, N2 supplies data/corpus checks. N5 is not assigned WP2 legal review or unrelated backend/provider code.

## Reading and identity evidence

- [PROGRESS §2](https://github.com/sosadsonar/ai-contract-risk-analyzer-pipeline/blob/d930e0092fa27f92cabf2ef8161d9fab86c60272/PROGRESS.md#2-phân-công-đề-xuất): proposed N1–N5 scopes, including X-10 transfer to N5.
- [BRD §9.6](https://github.com/sosadsonar/ai-contract-risk-analyzer-pipeline/blob/d930e0092fa27f92cabf2ef8161d9fab86c60272/docs/splitted_docs/BRD/15_9-rang-buoc-gia-dinh-phu-thuoc.md): baseline ownership and still-open coordination.
- [CONTRIBUTING §7](https://github.com/sosadsonar/ai-contract-risk-analyzer-pipeline/blob/d930e0092fa27f92cabf2ef8161d9fab86c60272/CONTRIBUTING.md#7-đổi-taxonomy-nhãn-clause): Clause-policy changes cross N1/N2/N3; changing a validator does not approve a Gold packet.
- Role-tagged Pipeline PRs: [N1 #21](https://github.com/sosadsonar/ai-contract-risk-analyzer-pipeline/pull/21), [N3 #30](https://github.com/sosadsonar/ai-contract-risk-analyzer-pipeline/pull/30), [N4 #27](https://github.com/sosadsonar/ai-contract-risk-analyzer-pipeline/pull/27), [N5 #28](https://github.com/sosadsonar/ai-contract-risk-analyzer-pipeline/pull/28) and [N5 #33](https://github.com/sosadsonar/ai-contract-risk-analyzer-pipeline/pull/33).
- Data source-review handoff and D2 review handoff preserve Owner-only governance; AI support is not a human scan read, new source rights or independent legal validation.

## Exact 24-file patch routing

The readable previews below are display-only (line-end whitespace removed). Apply only the decoded original patch after checking MANIFEST.json; previews are not an alternative machine patch. No application source, Gold, corpus text, model output or runtime default is changed by this routing.

| Pipeline path | Primary | Consult | Preview |
|---|---|---|---|
| ai_pipeline/evaluation/d2_clause_gold.py | N2 | N1, N3 | [N2](N2_REVIEW.md) |
| backend/app/ai/dev_local_client.py | N1 | N2 | [N1](N1_REVIEW.md) |
| backend/app/ai/risk_adapter.py | N3 | N2 | [N3](N3_REVIEW.md) |
| backend/app/clause/dev_tfidf_baseline.py | N1 | N2 | [N1](N1_REVIEW.md) |
| backend/app/legal/corpus_loader.py | N2 | N3, N4 | [N2](N2_REVIEW.md) |
| docs/superpowers/plans/2026-11-24-owner-d2-full-oracle.md | N2 | N1, N3 | [N2](N2_REVIEW.md) |
| scripts/align_d2_source_labels.py | N2 | N1, N3 | [N2](N2_REVIEW.md) |
| scripts/audit_data_lead.py | N2 | N1, N3 | [N2](N2_REVIEW.md) |
| scripts/audit_dev_risk_support.py | N2 | N1, N3 | [N2](N2_REVIEW.md) |
| scripts/generate_receipts_after_human_signoff.py | N2 | N1, N3 | [N2](N2_REVIEW.md) |
| scripts/install_approved_corpus.py | N2 | N3, N4 | [N2](N2_REVIEW.md) |
| scripts/measure_m8_dev.py | N2 | N1, N3 | [N2](N2_REVIEW.md) |
| scripts/prepare_wp2_scope_candidate.py | N2 | N1, N3 | [N2](N2_REVIEW.md) |
| tests/unit/test_d2_oracle_gold.py | N2 | N1, N3 | [N2](N2_REVIEW.md) |
| tests/unit/test_d2_source_alignment.py | N2 | N1, N3 | [N2](N2_REVIEW.md) |
| tests/unit/test_dev_local_client_oi05.py | N1 | N2 | [N1](N1_REVIEW.md) |
| tests/unit/test_dev_risk_support_audit.py | N2 | N1, N3 | [N2](N2_REVIEW.md) |
| tests/unit/test_dev_tfidf_baseline.py | N1 | N2 | [N1](N1_REVIEW.md) |
| tests/unit/test_install_approved_corpus.py | N2 | N3, N4 | [N2](N2_REVIEW.md) |
| tests/unit/test_legal_corpus_v2_release.py | N2 | N1, N3 | [N2](N2_REVIEW.md) |
| tests/unit/test_m8_source_clusters.py | N2 | N1, N3 | [N2](N2_REVIEW.md) |
| tests/unit/test_native_bounded_risk_schema.py | N3 | N2 | [N3](N3_REVIEW.md) |
| tests/unit/test_runtime_config.py | N4 | N2 | [N4](N4_REVIEW.md) |
| tests/unit/test_wp2_scope_controls.py | N2 | N1, N3 | [N2](N2_REVIEW.md) |

All review decisions remain PENDING until the named person actually reviews. Independent legal expertise is not assumed for any student role. N2 prepares WP2 source/effectivity/rights evidence with N3 semantic input; Sang is not substituted as a legal approver. Public issue threads carry metadata and blockers only; restricted source/Gold transfers use the existing authorized private route.
