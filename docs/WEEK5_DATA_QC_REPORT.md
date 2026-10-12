# Kiểm tra dữ liệu tuần 5 — 12/10/2026

Ứng viên `v06-rc1` có **234 clause / 5 hợp đồng / 4 similarity group / 12 nhãn**.
Validator hiện có trả **0 lỗi** sau sửa metadata và đường chạy snapshot.
RC đã chuẩn bị để review; hard test và split chưa được khóa thành benchmark.
Không tạo hoặc sửa nhãn rủi ro pháp lý.

## Phạm vi và bằng chứng

- Repo: `24021368-DucAnh/ai-contract-risk-analyzer`.
- `main` kiểm tra tại `3fadcfe` có v05 và validator từ PR #7.
- Snapshot mới nhất tìm được trên remote: `clauses_v06.csv`, commit `5ce5796`
  của nhánh `data/raw-text-offsets-v05`, chưa có trong `main` tại lúc kiểm tra.
- Nhánh PR tuần 5 tích hợp snapshot đó với validator từ `main`.
- SHA-256 v06: `c5318ebb59195536eac2a83fd223044b33a6ba3d086891d737dd5c2edc49667d`.
- Tính lại và lưu bằng chứng trong `notebooks/week5_data_qc.ipynb`,
  `reports/week5/qc_summary.json`, `duplicate_groups.csv` và
  `annotation_review_pairs.csv`. Notebook đã thực thi từ đầu đến cuối.
- Cached chat “Cập nhật tiến độ tuần 5” chỉ trả về tham chiếu nội dung assistant;
  không đọc được checklist chi tiết trước đó. Báo cáo dùng checklist trong yêu
  cầu hiện tại và các quy tắc dataset của repo, không tự suy ra chỉ tiêu tuần 5.

## Lỗi ban đầu và sửa lỗi

| Lỗi quan sát được | Nguyên nhân | Xử lý | Kết quả |
|---|---|---|---|
| Validator v06: `metadata:8: missing source file HDLD007.docx` | Metadata của release khai raw chỉ giữ local, chưa được chia sẻ trong Git | Đưa HDLD007 ra khỏi metadata của dataset; giữ URL, hash, SIM_E và trạng thái chờ trong hồ sơ intake | Validator 0 lỗi; không đưa HDLD007 vào v06 hoặc split |
| 1 test validator thất bại với 7 thông báo metadata | Test và CLI mặc định v05 trong khi metadata đã lên v06 | Cập nhật test và CLI mặc định sang v06; vẫn cho phép `--clauses` rõ ràng | 29 test: 28 pass, 1 skip |
| Hash v06 trong manifest tạm khác bytes trong Git | Windows checkout dùng CRLF, Git lưu LF | Cố định LF bằng `.gitattributes`, tính lại hash v06 và manifest split/RC | Hash v06 khớp Git và file bàn giao |
| Test nguồn HDLD007 bị skip | File không có trong checkout công khai | Giữ skip với lý do hiện có; test riêng đảm bảo intake không vào metadata release | Không coi skip là đã kiểm chứng raw HDLD007 |

Không nới quy tắc validator để bỏ qua raw thiếu. Không sửa raw, clause_type,
annotation_status hoặc nội dung clause v06. Sáu hash DOC/DOCX trong repo đều
khớp receipt trích xuất. Việc kiểm này xác minh file snapshot, không chứng minh
quyền tái phân phối hay tính đúng pháp lý của nguồn.

Hash `6ba5bede...` trong báo cáo tuần 3 là bản bytes CRLF của Windows. RC1 dùng
LF, hash `c5318ebb...` như trên; records CSV và masks giữ nguyên. Sự khác biệt
được xử lý bằng quy tắc newline, không phát hành nhãn mới.

## Phân bố nhãn

| Label | Số clause | Tỷ lệ |
|---|---:|---:|
| COMPENSATION_BENEFITS | 41 | 17.52% |
| CONTRACT_TERM | 13 | 5.56% |
| EMPLOYEE_OBLIGATIONS_DISCIPLINE | 34 | 14.53% |
| EMPLOYER_RIGHTS_OBLIGATIONS | 24 | 10.26% |
| INSURANCE_SAFETY | 13 | 5.56% |
| JOB_INFO | 21 | 8.97% |
| LEAVE | 16 | 6.84% |
| OTHER | 21 | 8.97% |
| TERMINATION | 20 | 8.55% |
| TRAINING | 13 | 5.56% |
| WORKING_CONDITIONS | 7 | 2.99% |
| WORKING_TIME | 11 | 4.70% |
| **Tổng** | **234** | **100%** |

Số clause theo hợp đồng: HDLD001 39, HDLD002 40, HDLD003 61,
HDLD004 43, HDLD005 51. Cả 234 row mang `REVIEWED` trong snapshot có sẵn.
Không có duplicate clause_id, required field trống, enum sai, count/version
metadata lệch hoặc offset ngoài giới hạn theo validator. Trạng thái REVIEWED
không thay thế review độc lập hoặc inter-annotator agreement.

## Offset EXACT / CONTEXT

- **225 EXACT (96.15%)**: span `[start,end)` khớp clause_text sau normalization
  khoảng trắng; toàn bộ được kiểm lại, 0 mismatch.
- **9 CONTEXT (3.85%)**: span hợp lệ, không rỗng, có `OFFSET_CONTEXT`; câu
  annotation có ngữ cảnh lặp hoặc khác nguồn nên không phải gold exact clause.
- IDs: `HDLD001_C014`, `HDLD003_C018`, `HDLD003_C018A`,
  `HDLD004_C023`, `HDLD004_C024`, `HDLD004_C025`, `HDLD004_C026`,
  `HDLD004_C027`, `HDLD004_C043`.
- Đối chiếu CONTEXT với anchor/phrase nguồn được test tái tạo. HDLD001_C014
  giữ khác biệt ký tự `S` ở nguồn; không tự chữa lỗi nguồn. Các ca còn lại
  chủ yếu do split đa chủ đề/lặp ngữ cảnh.
- Chỉ số là Unicode code point của Python, tính trên đúng raw_text đã hash;
  không phải byte UTF-8 hay UTF-16 của JavaScript.

## Duplicate, leakage và annotation consistency

| Kiểm tra | Kết quả | Diễn giải |
|---|---:|---|
| Text trùng sau gom khoảng trắng | 31 nhóm, 64 row liên quan, 33 row dư | Đây là số `duplicate texts` của validator; không xóa tự động |
| Text trùng sau thêm casefold | 31 nhóm, 65 row liên quan, 34 row dư | Thêm biến thể hoa/thường của HDLD001_C021 / HDLD002_C022 / HDLD003_C027 |
| Text giống sau casefold nhưng nhãn khác | 0 nhóm | Không thấy mâu thuẫn nhãn ở các text giống nhau |
| Text gần nhau >=0.85 nhưng nhãn khác | 23 cặp | Lưu toàn bộ ID, text, label, score để review; không kết luận 23 lỗi |
| Nhóm template nằm nhiều split | 0 | SIM_A dev; SIM_B và SIM_D train; SIM_C test |
| Manifest split tái tạo | Khớp hoàn toàn | Dataset hash và toàn bộ masks/denominators khớp |
| Matches xuyên split còn được chấm | 0 | Theo EXACT/SequenceMatcher và điều kiện độ dài hiện hành |

Các cặp khác nhãn thường có placeholder dài, khác topic hoặc khác chủ thể:
C030/C033 là nghĩa vụ NLĐ so với quyền NSDLĐ; C038/C039 là khiển trách so
với sa thải; C040/C041 đổi bên chịu bồi thường. C023/C024 dùng cùng context
nhưng khác chủ đề nghỉ/học nghề. Reviewer cần xác nhận theo taxonomy và
nguồn; similarity ký tự không đủ để sửa nhãn. Queue 23 cặp là review mở,
không phải quyết định gán lại annotation.

| Split | Clause gốc | Được chấm clause | Được chấm exact span | Loại khỏi chấm |
|---|---:|---:|---:|---:|
| Train | 112 | 112 | 110 | 0 |
| Dev | 79 | 49 | 48 | 30 |
| Test | 43 | 34 | 28 | 9 |

Dev exclusions gồm 6 EXACT_CROSS_SPLIT + 24 NEAR_CROSS_SPLIT; test gồm
9 NEAR_CROSS_SPLIT. Dùng masks trong `provisional_v06.json` trước khi tính
metric. Các row vẫn được lưu trong dataset. Không có đủ dữ liệu để kết luận
không còn leakage ngữ nghĩa hoặc model đã từng thấy test từ lịch sử huấn luyện.

## Hard test và release candidate

`data/evaluation/hard_test_v06_rc1.jsonl`: **20 ca / 11 nhãn**, đều từ 34 row
test có thể chấm của SIM_C. **14 EXACT**, **6 CONTEXT**. Có các cặp contrast
nghĩa vụ/quyền, bồi thường, PPE/chỗ ở, nghĩa vụ tuân thủ an toàn, khiển trách/
sa thải, split đa chủ đề và lặp chủ ngữ ngày hiệu lực.

Mỗi ca chứa input, nhãn kỳ vọng kế thừa từ v06, text nguồn, parent line,
offset, hash, notes và quy tắc taxonomy. CONTEXT có `gold_exact_clause_span=null`.
Tất cả có `independent_review_status=PENDING`; reviewer cần adjudicate trước
khi dùng làm benchmark. Riêng C003 cần xác nhận treatment của thử việc trong
CONTRACT_TERM; C022 cần review quyền lợi của NLĐ so với nghĩa vụ thanh toán
của NSDLĐ bằng section context. Không đổi nhãn bằng suy đoán.

`data/releases/v06-rc1/manifest.json` đóng băng hash đầu vào, masks và evidence;
trạng thái `CANDIDATE_REVIEW_REQUIRED`. Bộ candidate đủ bằng chứng cơ học để
review clause/exact span; chưa có ground truth được adjudicate cho risk pháp lý.

## Warnings và blockers

12 nhóm warning được lưu trong JSON, với tác động cụ thể:
9 CONTEXT, duplicate, 39 exclusions, 23 cặp review, nhãn ít mẫu, thiếu
WORKING_TIME ở test, thiếu TERMINATION ở dev, hard gold chờ review, URL gốc
HDLD001–003 còn TODO, HDLD007 chờ quyền chia sẻ, leakage ngữ nghĩa chưa được
review và thiếu legal risk gold.

| Việc còn mở | Ai xử lý | Điều kiện hoàn tất |
|---|---|---|
| Review 20 hard ca và 23 cặp annotation | Data reviewer + AI/Evaluation Lead | Record reviewer, ngày, quyết định và lý do; adjudicate bất đồng |
| Khóa benchmark đủ nhãn | Data Lead + Evaluation Lead | Thêm template độc lập, đủ WORKING_TIME/TERMINATION ở phần đánh giá; review leakage |
| Legal risk ground truth | Reviewer có chuyên môn pháp lý | Căn cứ nguồn chính thức, điều/khoản/điểm, ngày hiệu lực và rationale cho từng nhãn |
| HDLD007 intake | Người quản lý nguồn | Xác nhận quyền chia sẻ file/annotation rồi mới vào metadata và annotate |
| Provenance HDLD001–003 | Data Lead | Bổ sung URL gốc hoặc hồ sơ nguồn kiểm chứng được |
| Cập nhật fixture pipeline | AI/Evaluation Lead | Dùng đúng v06/hash/masks; fixture v0.3 cũ chỉ có 174 EXACT |

Không có metric từ model chạy trong task này. Không có bằng chứng IAA hoặc
review pháp lý độc lập. Do đó không báo tuần 5 hoàn tất toàn bộ.

## Tái tạo

Từ root repo, Python 3.10+:

```powershell
python -m scripts.validate_dataset
python -m unittest discover -s tests -v
python -m jupyter nbconvert --execute --to notebook --inplace notebooks/week5_data_qc.ipynb
```

Validator và test dùng standard library. Notebook cần Jupyter/nbconvert,
nbformat và Python kernel. Notebook ghi lại report, hard candidate và manifest;
review diff trước khi chấp nhận thay đổi hash. Không chạy script extraction
đè raw_text hiện hành vì sẽ làm mất nền offset.
