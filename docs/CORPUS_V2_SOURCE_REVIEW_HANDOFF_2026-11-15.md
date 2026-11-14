# Corpus v2 source review handoff — 15/11/2026

This packet prepares employment-contract law candidates for N2/N3 and an independent content/effectivity reviewer. It does **not** approve a legal node, change Gold, or activate a runtime corpus. The scope matrix and PR sequence are in Data [PR #22](https://github.com/24021368-DucAnh/ai-contract-risk-analyzer/pull/22).

## Reproducible inventory

- `data/intake/corpus_v2_source_register_2026-11-15.csv` records nine source files/parts, official record URLs, local SHA-256, document-level effective-date metadata and open review gates. Source files are local and restricted. Source hashes were recomputed from the physically present files; the two signed NĐ 399/2026 attachments were downloaded on 15/11 from the [Government record](https://vanban.chinhphu.vn/?docid=220166&orggroupid=2&pageid=27160).
- `data/intake/corpus_v2_priority_review_queue_2026-11-15.csv` has **160 text-free metadata rows**: 29 proposed articles, 86 clauses and 45 points. It is generated from the 86-page official VBHN 18 PDF OCR candidate: source PDF SHA-256 `5a01a5b4b778b78c7bc9372e3a7270735bd98c28160604bff95db06bb3345a6f`; OCR candidate JSONL SHA-256 `b2b15e82b5dac782a2811b250898f050d904aa32569a74dffafd2f0181cb194b`. Public queue SHA-256 `73bb05d9ae4a1cf51ccdbfb4c0d952758199ba0572cdf194f68a245697d35b90`.
- The paired **private** sheet is `D:\DHCN\Nam3_Ky1\CVDKHMT\corpus-v2-private-review-2026-11-15\restricted\priority_bll_review_v01.csv`, SHA-256 `b198681b5cc228bd04ba9c09ba900b58bfe502826f57b9d59c197b0426c0fb54`. It contains OCR candidates and blank `verified_text`, amendment/effectivity and reviewer fields. Keep it outside public Git. Its source page hints use the **86-page portal PDF**, whereas the Công báo comparison PDF has 88 pages; reviewers must locate the corresponding Gazette page rather than copy a page number.
- `scripts/build_corpus_v2_review_packet.py` reproduces the paired sheets. It rejects source hash mismatch, duplicate node IDs, empty OCR candidates, bad pages and already approved rows. It never places candidate text in the public queue.

Selected article IDs: 20, 24–27, 29, 33, 35–36, 40–41, 46–48, 94–98, 101, 105, 107, 109–115. This is a candidate shortlist from taxonomy and Dev needs, **not** a quota or scope approval. The v1 Articles 13–17 and 21 remain in their original snapshot and require their own release evidence.

## Reviewer instructions

For every candidate clause/point, N2 checks the signed official page image against the OCR candidate and enters the exact wording in `verified_text`. A second reviewer checks article/clause/point identity, amendments, applicable dates and legal effect. Both record names/date/decision; disagreements remain `PENDING_REVIEW`. N3 checks that proposed risk and clause-label mappings reflect the reviewed provision. An accepted node also needs its source hash, official URL, access date and permitted-use decision in a versioned release receipt. No OCR text or hash match alone is an approval.

The [signed NĐ 399/2026 main text](https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/11/399_2026_nd-cp_02112026_6-signed.signed.pdf) Article 5(1–2) states 01/01/2027 commencement and cessation of NĐ 293/2025 from that date. This supports a **candidate** NĐ 293 interval ending 31/12/2026 under the current inclusive `effective_to` convention. The [signed annex](https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/11/399_2026_nd-cp_02112026_7-signed.pdf) has the 2027 region list. A reviewer must verify both instruments' operative text and locality rules before importing a wage provision or setting a product threshold. NĐ 145 and TT 10 are P1 guidance candidates; the local TT 10 copy has a hash, but the official attachment could not be retrieved and authenticated, so it is excluded from runtime intake.

## Data and evaluation boundary

This public package contains no T1/T2 contract text or Gold. The 17 T1 corpus-scope exceptions remain a **separate restricted reviewer queue after v2 is frozen**. Their labels or model misses are not used to select provisions, edges, prompts or weights. D2 clause-label Gold and M1 annotation-unit policy need N1/N2 adjudication; D1 labels transfer only where canonical source hashes and exact spans match. A fresh M8-oracle or held-out M2/M6 score must not be reported from candidate rows.


## Completion gates for the next package

1. N2/N3 agree the adopted article/instrument subset and source rights.
2. Two human review decisions and exact source-page transcriptions exist for every admitted provision, including amendment/effectivity interval.
3. A versioned v2 loader validates receipts, checksums, IDs, NFC, interval overlap and graph/mapping provenance; v1 remains unchanged.
4. Only then build new `provisions.jsonl`, label map, edges and `manifest.yaml` with `DRAFT` until release sign-off. Run Dev retrieval and citation-relevance review before changing runtime pin.
