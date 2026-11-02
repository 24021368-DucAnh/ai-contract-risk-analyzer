# Legal source status monitor — 2026-11-01

## Purpose and limits

This is a source-freshness note for the Data Lead's law-corpus work. It records
official publication and legislative-stage pages found on 2026-11-01. It is
not a legal opinion, article-by-article amendment map, or approval to change
the DRAFT corpus.

## Official source checks

| Item | Official record observed | Data handling |
|---|---|---|
| Bộ luật Lao động 45/2019/QH14 | The Government portal lists the promulgation date as 2019-11-20 and the effective date as 2021-01-01; the signed PDF is attached on the record page. | Keep as the original instrument/source record. Do not infer current wording of every article from the original PDF. |
| VBHN 18/VBHN-VPQH | The Government portal lists the consolidated text as issued 2026-02-12. | Retain as a consolidated-text source for comparison; still verify each provision's amendment history and effective interval before approval. |
| Draft bill amending the Labour Code and four related laws | National Assembly pages report Standing Committee comments on 2026-09-04, then the Government submission and appraisal report at the Assembly on 2026-10-21, followed by group discussion. The September page describes 2027-03-01 as the draft's proposed effective date. | Monitoring-only. Do not ingest draft text as effective law or create approved provisions/edges from it. Recheck enacted records and final transition clauses before any future corpus update. |
| Draft amendment to Decree 145/2020/NĐ-CP | The Government portal's draft page says the Ministry of Home Affairs was consulting on a draft on 2026-07-10. | Monitoring-only. Do not treat the draft as current subordinate legislation. Recheck for a promulgated decree before updating corpus. |
| Decrees 12/2022 and 283/2026 on labour/social-insurance penalties | New check on 2026-11-02 found the official record for [Decree 283/2026](https://vanban.chinhphu.vn/?docid=218871&pageid=27160&typegroupid=4), issued 2026-07-15 and effective 2026-09-10. A [Government news item](https://baochinhphu.vn/quy-dinh-moi-xu-phat-vi-pham-hanh-chinh-trong-linh-vuc-lao-dong-bao-hiem-xa-hoi-102260715215333228.htm) describes its promulgation; a second [Government article](https://baochinhphu.vn/lao-dong-nuoc-ngoai-duoc-tra-them-1-tien-luong-thay-bao-hiem-that-nghiep-10226101211144485.htm) records Decree 12/2022 expired from 2026-09-10 and cites the new Decree's transition provisions. | Treat Decree 283 as the current priority candidate from its effective date; retain Decree 12 only for historical conduct and transition review. The 283 PDF was downloaded to restricted storage; verify its repeal/transition text and affected provisions before changing any corpus intervals. |

## Data action

No provision text, effective dates, graph edges, or release status were changed
from these pages. The repository's legal candidates remain subject to
the review gates already recorded in `docs/W4_LEGAL_DATA_ACQUISITION_2026-10-29.md`:
source-file receipt, per-provision transcription check, amendment/effectivity
review, and qualified legal reviewer sign-off.

Before the next corpus release:

1. Check the official gazette / Government legal-document record for any
   promulgated amendment to 45/2019/QH14 after VBHN 18/VBHN-VPQH.
2. If promulgated, record the amending instrument, exact affected provisions,
   effective dates, and transition rules separately; do not overwrite prior
   versions.
3. Check whether the Decree 145 draft became an issued instrument and inspect
   its final text and effective date.
4. Obtain independent legal review before changing candidate rows or graph
   relations from `PENDING_LEGAL_REVIEW`.

## Sources

- [Government portal: Law 45/2019/QH14](https://vanban.chinhphu.vn/?classid=1&docid=198540&orggroupid=1&pageid=27160)
- [Government portal: consolidated text 18/VBHN-VPQH](https://vanban.chinhphu.vn/?classid=0&docid=217002&pageid=27160)
- [National Assembly: Standing Committee comments on the five-law draft, 2026-09-04](https://quochoi.vn/cacvilanhdao/Pages/hoat-dong.aspx?ItemID=101387)
- [National Assembly: submission and appraisal on the five-law draft, 2026-10-21](https://quochoi.vn/tintuc/Pages/tin-hoat-dong-cua-quoc-hoi.aspx?ItemID=102307)
- [Government portal: draft amendment to Decree 145/2020/NĐ-CP](https://vanban.chinhphu.vn/?pageid=30187&title=-du-thao-nghi-dinh-sua-doi-bo-sung-mot-so-dieu-cua-nghi-dinh-so-145-2020-nd-cp-ngay-14-12-2020-q&vbid=7877)
