# N2 WP2: visual source review and effectivity research — 2026-11-25

This is a review handoff, not a corpus release or a real Pipeline implementation PR.

Completed in this session:

- Displayed and compared 21 hash-bound Gazette PDF pages against all 118 WP2 candidate entries and 7 excluded delegated dependencies. Observed 125 matches allowing NFC/layout whitespace only; no content mismatch observed. Reviewer: AI assistant under owner-authorized self-review, not a named human or independent reviewer.
- Recorded each citation, content hash and source page in the internal evidence packet. All 7 excluded dependencies remain outside the 118-entry candidate and all 17 held mapping pairs remain held. No Gold or source contracts are published here.
- Checked the direct Labor Code amendment targets in laws 71/2025/QH15 (art49cl4), 113/2025/QH15 (art29cl1) and 124/2025/QH15 (art43cl1), including relevant official PDF pages and effective-date clauses. Their direct targets do not intersect the candidate articles. This bounded finding does not certify a complete amendment history or applicability of each mapping.
- Retrieved and visually checked the signed 293/2025/ND-CP decree pages 1–4: effective 2026-01-01, replacing 74/2024 at that date. The locality appendix is not fully reviewed and this decree has not been admitted to runtime.
- Verified a statutory copyright basis for official legal text in art15cl2 of the IP Law, official consolidated text 160/2026/VBHN-LQ-VPQH PDF page14. This is not a consent receipt for contracts/personal data and is not a fabricated CC license.
- Rehashed 666 frozen source/resource files: unchanged. Runtime defaults and the Data gitlink are unchanged; no new model calls and no held-out T1/T2 used.

## Newly identified legal follow-ups for N3

1. [Official government report, 2026-11-21](https://baochinhphu.vn/quoc-hoi-dong-y-bo-sung-2-ngay-nghi-le-duoc-huong-nguyen-luong-102261121121448218.htm) reports adoption of the five-law amendment including the Labor Code, with effect from 2027-03-01 and two additional paid holidays. Do not keep describing this solely as a September draft. The numbered signed law was not retrieved in this review. Watch art112 and verify the complete amending article before certifying future-date coverage; do not inject future rules into the frozen 2026 evaluation.
2. The signed law 113/2025/QH15 PDF page13 prints `49/2019/QH14` in art29cl1 when referring to the Labor Code. Visually confirmed as source text, not merely extraction noise. Preserve source/hash and reconcile against any correction and the consolidated text; do not silently rewrite it. Its art139 target is outside this WP2 candidate.

Primary sources:

- [Labor Code consolidation 18/VBHN-VPQH](https://vanban.chinhphu.vn/?docid=217002&pageid=27160)
- [71/2025/QH15](https://vanban.chinhphu.vn/?docid=214609&pageid=27160)
- [113/2025/QH15](https://vanban.chinhphu.vn/?docid=216497&pageid=27160)
- [124/2025/QH15 official Gazette PDF](https://congbaocdn.chinhphu.vn/180507251028987904/2026/1/24/124signed-17692389053721694633254.pdf)
- [293/2025/ND-CP](https://vanban.chinhphu.vn/?docid=215832&pageid=27160)
- [IP Law consolidation 160/2026/VBHN-LQ-VPQH](https://vanban.chinhphu.vn/?docid=219876&pageid=27160)

## Blocking handoffs already routed

| Owner | Existing task | Required input |
|---|---|---|
| N1 / sosadsonar | #27 | Clause/provider review; frozen model/prompt/config and real Dev outputs |
| N3 / AnhTuHoangPahm | #28 | WP2 legal/mapping dispositions, rubric/taxonomy compatibility, frozen Risk outputs; new legal follow-ups above |
| N4 / ghoulixia | #29 | Decode exact patch, host checks, actual Pipeline PR; current integration cannot write to Pipeline |
| N5 / ckpsang06 | #30 | X-10 rights/intake/deidentification/deduplication and T1/M6 handoff |
| N2 / 24021368-DucAnh | #31 | Incorporate accepted handoffs, evaluate Dev and freeze final data |

PR #25/#26 remain draft with no review submitted, and #27–#31 have no comments at this session's check. M10 remains NOT_MEASURED. No release, merge or end-to-end PASS is claimed. Historical test results are not fresh integration evidence. The Windows full-suite run previously stalled in asyncio socketpair; that boundary remains blocked pending a suitable host.
