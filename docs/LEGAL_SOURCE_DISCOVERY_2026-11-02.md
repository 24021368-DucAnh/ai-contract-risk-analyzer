# Legal source discovery — 2026-11-02

This is a source-discovery record for the labour-law corpus. It is not legal
advice, provision-level verification, an amendment map, or approval to release
candidate text into retrieval.

## Primary-source records checked

| Instrument | Official record observed | Corpus handling |
|---|---|---|
| Bộ luật Lao động 45/2019/QH14 | [Government legal-document record](https://vanban.chinhphu.vn/?classid=1&docid=198540&orggroupid=1&pageid=27160) identifies the law, promulgation date 2019-11-20, and effective date 2021-01-01. | Existing local signed PDF remains a source artifact. Verify each provision and later changes independently. |
| VBHN 18/VBHN-VPQH | [Government legal-document record](https://vanban.chinhphu.vn/?classid=0&docid=217002&pageid=27160) identifies a consolidated Labour Code, issued 2026-02-12. | Existing local PDF/OCR is a comparison candidate only; consolidation does not replace checking article-level amendment history or effectivity. |
| Decree 145/2020/NĐ-CP | [Government legal-document record](https://vanban.chinhphu.vn/default.aspx?docid=201967&pageid=27160) identifies the decree, promulgation date 2020-12-14, and effective date 2021-02-01. Its signed PDF is already in restricted intake with a receipt. | Keep the original as a source artifact. Check later amendment history and the applicable interval before extracting operative provisions. |
| Draft amendment to Decree 145/2020/NĐ-CP | [Government consultation page](https://vanban.chinhphu.vn/?pageid=30187&title=-du-thao-nghi-dinh-sua-doi-bo-sung-mot-so-dieu-cua-nghi-dinh-so-145-2020-nd-cp-ngay-14-12-2020-q&vbid=7877) says the Ministry of Home Affairs opened consultation on 2026-07-10 and the consultation period ended on 2026-07-19. | Monitoring-only draft. It is not evidence of an issued amending decree; do not ingest its proposed clauses as effective law. |
| Decree 293/2025/NĐ-CP on minimum wages | [Government legal-document record](https://vanban.chinhphu.vn/?docid=215832&pageid=27160) identifies the instrument and effective date 2026-01-01. | Add as a priority source candidate for time-dependent wage checks; verify its operative regions, transition/repeal clauses, and relation to the earlier Decree 74 before creating corpus provisions. |
| Decree 74/2024/NĐ-CP on minimum wages | [Government legal-document record](https://vanban.chinhphu.vn/?classid=0&docid=210536&pageid=27160) identifies its effective date as 2024-07-01. | Retain only as a historical/time-bounded candidate; do not apply to 2026 contract dates without checking the later instrument. |
| Law 41/2024/QH15 on Social Insurance | [Government legal-document record](https://vanban.chinhphu.vn/?classid=1&docid=211199&orggroupid=1&pageid=27160) identifies its effective date as 2025-07-01. | Candidate for social-insurance clause checks; record relevant articles and transition rules only after scope and legal review. |
| Decree 12/2022/NĐ-CP on labour and social-insurance penalties | [Government legal-document record](https://vanban.chinhphu.vn/default.aspx?docid=205182&pageid=27160) identifies the instrument, issued and effective 2022-01-17. A later [Government article](https://baochinhphu.vn/lao-dong-nuoc-ngoai-duoc-tra-them-1-tien-luong-thay-bao-hiem-that-nghiep-10226101211144485.htm) reports it ceased to apply from 2026-09-10. | Historical/time-bounded candidate for earlier conduct and transition review; do not use as the current default after 2026-09-10. |
| Decree 283/2026/NĐ-CP on labour and social-insurance penalties | [Government legal-document record](https://vanban.chinhphu.vn/?docid=218871&pageid=27160&typegroupid=4) lists issue date 2026-07-15, effective date 2026-09-10 and its official signed PDF. The Government article identifies the new decree ([Chinhphu.vn](https://baochinhphu.vn/quy-dinh-moi-xu-phat-vi-pham-hanh-chinh-trong-linh-vuc-lao-dong-bao-hiem-xa-hoi-102260715215333228.htm)). | Current priority source candidate. Verify the full repeal and transitional text in the signed PDF before applying the time split. Decree 12 remains a historical source candidate for earlier conduct, not a current default. |
| Draft amendment to Decree 12/2022/NĐ-CP | [Government consultation page](https://vanban.chinhphu.vn/du-thao-vbqppl/du-thao-nghi-dinh-sua-doi-bo-sung-mot-so-dieu-nghi-dinh-so-12-2022-nd-cp-ngay-17-1-2022-cua-chin-7284) records a draft consultation opened 2025-02-05. | Monitoring-only; the later promulgated Decree 283/2026 is a separate instrument. Do not treat the 2025 draft as issued law. |
| Draft minimum-wage instrument listed in 2026 consultation pages | [Government consultation listing](https://vanban.chinhphu.vn/du-thao-vbqppl?_piref135_446244_135_446237_446237.id=2780&_piref135_446244_135_446237_446237.mode=displayreply) lists a draft minimum-wage instrument with a 2026-07-22 to 2026-07-31 comment period. | Monitoring-only; inspect final promulgated records before changing any wage rule. |

## Search-source quality note

Legal Data Hunter's Vietnam source catalog lists `VN/PhapLuatGov` as a Tier 1
Government legislation database and `VN/CongBao` as a Tier 2 source. Exact
identifier queries for 45/2019/QH14, 18/VBHN-VPQH and 145/2020/NĐ-CP returned
mostly unrelated records in the available search results. Therefore those
search results were not used to establish instrument identity or current
effectivity; the primary Government records above were opened directly.

## Required before corpus approval

1. Check the official promulgated-document records and gazette for any issued
   amendments affecting the Code or Decree 145 after the local source snapshots.
2. Record the exact instrument, affected provisions, effective intervals and
   transition clauses in a versioned amendment map.
3. Compare each candidate provision against the source page/image, including
   punctuation and paragraph boundaries; OCR remains `UNPROOFREAD` until that
   comparison is completed.
4. Obtain qualified legal review before changing candidate rows, manual graph
   edges, or corpus release status.

The 2026 search identifies additional time-sensitive candidate sources,
including a minimum-wage decree effective from 2026-01-01. The corpus remains
`DRAFT`; no provision, edge, label mapping, or effectivity value was changed
by this search.

## Freshness correction — penalty instrument

The official registry now identifies Decree 283/2026/NĐ-CP as effective
2026-09-10. A Government news article states Decree 12/2022/NĐ-CP ceased to
apply from that date, with transition handling for earlier conduct. Decree 12
must therefore not be treated as the current general penalty source; retain
it only for historical intervals/transition cases pending review of the signed
texts. This corrects the earlier monitoring note's open question; it does not
approve a provision-level effectivity map.

## Local source acquisition

Four official attachments were downloaded to ignored
`data/intake/restricted/legal_sources/` and recorded in
`data/intake/legal_source_receipts_2026-11-02.csv`:

| Instrument | Local evidence | Mechanical result |
|---|---|---|
| 283/2026/NĐ-CP | `ND_283_2026_original.pdf` | Official PDF downloaded on 2026-11-02; 100 pages, no extractable text layer; hash/source URL recorded. Full OCR candidate and metadata-only structure index created; all nodes pending review. |
| 41/2024/QH15 | `BHXH_41_2024_original.pdf` | Hash and 88-page count match receipt; PDF text layer has 193,247 extractable characters. |
| 12/2022/NĐ-CP | `ND_12_2022_original.pdf` | Hash and 83-page count match receipt; no extractable PDF text layer. An 83-page OCR candidate was generated. |
| 293/2025/NĐ-CP | `ND_293_2025_min_wage.pdf` | Hash and 14-page count match receipt; no extractable PDF text layer. OCR candidate exists but remains unproofread. |

Six OCR derivative receipts are in
`data/intake/legal_ocr_candidate_receipts_2026-11-02.csv`. The OCR outputs have
ordered page markers, all pages non-empty, matching source hashes, and no
Unicode replacement characters. These checks validate file structure and
encoding only, not OCR correctness.

The 18/VBHN-VPQH OCR candidate has all 86 source pages in order and matching
source SHA-256. Its metadata-only Article review queue contains 220 rows; 215
article numbers have OCR heading matches and 5 are not detected. Every row is
`PENDING_VISUAL_REVIEW`; those counts are not proof that any provision is
correct, complete, or absent from the source.

An initial OCR candidate was decoded using the Windows default code page and
contained corrupted Vietnamese characters. It was retained under the explicit
`_cp1252_INVALID` filename in restricted storage. The corrected UTF-8 candidate
was regenerated from the source PDF and checked for replacement characters;
only that corrected file is used for the structural review queue.

Decree 283/2026/NĐ-CP has an OCR candidate and a separate metadata-only
structure index with 1 document, 68 article IDs, 312 clause candidates and
665 point candidates. Article 33 was not detected as a heading. All nodes
remain `PENDING_LEGAL_REVIEW`; this index is not an approved legal dataset.

## Visual-review receipt correction — 2026-11-02

An integrity test found that the three existing visual-review log rows for
`LAW-BLLD-VBHN-18-2026` carried a source SHA-256 that matched no source receipt.
Pages 44, 45 and 61 were re-rendered from the receipt-matched
`VBHN_18_2026_original.pdf` (SHA-256
`5a01a5b4b778b78c7bc9372e3a7270735bd98c28160604bff95db06bb3345a6f`). The
visible headings matched the logged article occurrences: 116–118, 118–120 and
165–167 respectively. The three log hashes now match the source receipt, and
`tests/test_legal_visual_review_log.py` checks source-hash and page-bound
consistency for all entries. This is structural Data QA only: it does not
transcribe provisions, update the OCR structure index, establish effectivity,
or replace legal review; all index rows remain pending legal review.

## Recheck of Circular 10/2020 source metadata — 2026-11-02

The national legal database managed by the Ministry of Justice has an exact
record for Circular 10/2020/TT-BLĐTBXH at
<https://vbpl.vn/botuphap/Pages/vbpq-toanvan.aspx?ItemID=146696>. The record
displays the instrument number/title, effective date 2021-01-01, and status
“Còn hiệu lực” as observed on 2026-11-02. This is registry metadata, not an
independent amendment-history review or provision-level approval. The linked
record redirected to the portal landing page in the local browser and the
previous official-host download attempt timed out; no PDF was obtained, so the
existing receipt remains `SOURCE_FOUND_DOWNLOAD_FAILED`, with no local hash,
page count, OCR, or corpus text. Retry the signed attachment from the registry
when its download endpoint is reachable, then compare it with the observed
metadata and review the instrument's history before importing any provision.

## Secondary copy lead — Circular 10/2020 — 2026-11-02

A full-text PDF copy is discoverable on the University of Danang's public legal
education portal at
<https://pbgdpl.udn.vn/FileCongvan/2022/1/2022m1_100000000.9754103PBQPPL_CVD_454406.pdf>.
The web text view exposes the instrument heading and provisions, but this copy
was not downloaded into restricted storage or compared page-by-page with the
signed registry attachment. Treat it only as a
retrieval lead: it does not change the failed official-attachment receipt,
provide a local source hash, establish current effectivity, or authorize text
to enter the legal corpus. Next, obtain the registry attachment or compare a
locally receipted copy against it and review the instrument's amendment history.
