# Bàn giao AI / Evaluation Lead — v06 RC1

Ngày: 12/10/2026. Phạm vi: phân loại clause và source span cho HĐLĐ tiếng Việt.
Dataset và hard test đang ở trạng thái candidate để review trong PR.

## File nhận bàn giao

- Release receipt: `data/releases/v06-rc1/manifest.json` (hash từng file).
- Dataset: `data/processed/clauses_v06.csv` — 234 clause, 5 contract.
- Metadata: `data/contracts_metadata.csv` — 6 raw đã chia sẻ; HDLD006 hold.
- Nguồn offset: `data/processed/raw_text/HDLD001.txt` tới `HDLD006.txt`.
- Split/masks: `data/splits/provisional_v06.json`.
- Hard test candidate: `data/evaluation/hard_test_v06_rc1.jsonl` — 20 ca.
- Evidence: `docs/WEEK5_DATA_QC_REPORT.md`, `reports/week5/` và
  `notebooks/week5_data_qc.ipynb`.

Không chọn CSV theo tên glob hoặc phiên bản fixture cũ. Xác nhận hash v06
`c5318ebb59195536eac2a83fd223044b33a6ba3d086891d737dd5c2edc49667d`
và kiểm toàn bộ hash trong manifest trước chạy experiment. Ghi commit PR,
release ID, model/prompt version, seed và masks vào log evaluation.

## Đọc split và chấm điểm

1. Chia theo contracts/similarity_groups của manifest: train SIM_B+SIM_D,
   dev SIM_A, test SIM_C. Không random từng clause.
2. Bỏ `excluded_clause_ids` của dev/test khỏi metric. Counts phải là
   train/dev/test **112/49/34** cho classification.
3. Span metric lọc thêm `offset_quality=EXACT`: **110/48/28**.
   CONTEXT chỉ là source reference/highlight, không phải gold exact clause.
4. Dùng raw text nguyên snapshot, `[start,end)` theo Unicode code point.
   Không normalize trước khi áp offset; chỉ normalize khoảng trắng khi
   kiểm khớp như validator. Không đổi raw text bằng extraction mới.
5. Báo support từng nhãn, confusion matrix và macro/per-class F1 với định
   nghĩa rõ. Test không có WORKING_TIME và dev không có TERMINATION sau masks;
   không coi nhãn vắng là F1=0 hay bỏ qua âm thầm. Ghi label set và zero-division
   policy trong báo cáo; không so macro-F1 giữa các label set khác nhau.
6. Khóa test khỏi lựa chọn prompt, threshold và hyperparameter. Việc test đã
   công khai trong repo cần được ghi là hạn chế; kiểm lịch sử model exposure
   trước khi coi là held-out benchmark.

Fixture `ai_pipeline/eval/fixtures/build_golden_v0_3.py` ở repo pipeline cũ
chỉ xuất 174 EXACT của snapshot cũ. Cần adapter v06 với masks nêu trên trước
chạy evaluation. Task này không sửa repo pipeline hoặc chạy model.

## Adjudicate hard test

Hard candidate chọn SIM_C từ scorable test, gồm 20 clause, 11 nhãn,
14 EXACT và 6 CONTEXT. Trường `expected_clause_type` kế thừa v06 REVIEWED;
nguồn và offsets có thể đối chiếu ngay trong từng record. Nhãn pháp lý là null.

- Reviewer mở raw DOCX + raw text đã hash, đối chiếu source span và parent line.
- Đọc basis theo taxonomy v0.3/guideline v1.0. Review C003 (thử việc) và C022
  (quyền lợi/thanh toán) bằng section context; input_text đơn lẻ có thể thiếu actor.
- Ghi reviewer, ngày, quyết định `ACCEPT/CHANGE/NEEDS_REVIEW`, rationale và
  bằng chứng. Bất đồng cần adjudicator; không sửa snapshot v06 trong PR này.
- Nếu đổi ground truth, tạo version hard test mới và cập nhật hash/manifest.
- Chỉ sau sign-off mới dùng classification gold làm benchmark. Exact source
  span cũng cần thống nhất mục tiêu: span clause trong raw document khác
  với nhãn cho classifier nhận một clause đã tách sẵn.
- 6 CONTEXT có `gold_exact_clause_span=null`; không chuyển source_reference_span
  thành exact gold trong adapter. Chấm riêng abstention/highlight nếu cần.

`annotation_review_pairs.csv` có 23 cặp gần text nhưng khác label. Đây là
review queue; placeholder và actor/topic contrast có thể là đúng. Không
relabel theo similarity score.

## Tiêu chí nhận RC và việc còn mở

- [x] Validator 0 lỗi, test 28 pass + 1 skip nguồn HDLD007.
- [x] 6 hash raw DOC/DOCX khớp receipt; split tái tạo khớp; 0 match vượt
  ngưỡng xuyên split sau masks; 0 mâu thuẫn label ở text giống sau casefold.
- [x] Có hard candidate với bằng chứng nguồn và manifest hash.
- [ ] Reviewer Data xác nhận provenance và review queue.
- [ ] AI/Evaluation Lead adjudicate hard gold, adapter v06 và denominators.
- [ ] Bổ sung template độc lập/coverage trước khi khóa benchmark cuối kỳ.
- [ ] Có ground truth risk/citation pháp lý với căn cứ và ngày hiệu lực
  nếu muốn đánh giá module Risk Analyzer.

HDLD007 nằm trong intake queue ở `CONTRACT_INTAKE_QC_2026-10-05.md`, chờ
quyền chia sẻ và annotation. URL nguồn gốc HDLD001–003 còn cần truy vết.
Các việc này vẫn được báo là mở. PR cần reviewer; không tự merge.
