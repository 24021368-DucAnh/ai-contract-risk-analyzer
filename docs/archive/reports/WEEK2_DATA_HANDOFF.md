# Bàn giao Data Lead — mốc tuần 2 (snapshot v05)

## Phạm vi đã hoàn thành

- Batch annotation đầu đã được mở rộng tới 183 clause `REVIEWED` thuộc bốn hợp
  đồng HDLD001–HDLD004, lưu tại `data/processed/clauses_v05.csv`.
- Đã thống kê phân bố 12 nhãn và gán `similarity_group` trong
  `data/contracts_metadata.csv`.
- Đã tạo bản chia **tạm** tại `data/splits/provisional_v05.json` bằng
  `scripts/build_provisional_split.py`. Script dùng toàn bộ hợp đồng làm đơn vị
  chia; không chia ngẫu nhiên từng clause.

| Tập | Nhóm / hợp đồng | Clause gốc | Clause có thể chấm sau kiểm tra trùng | Gold span EXACT có thể chấm |
|---|---|---:|---:|---:|
| Train | SIM_B / HDLD003 | 61 | 61 | 59 |
| Dev | SIM_A / HDLD001, HDLD002 | 79 | 55 | 54 |
| Test | SIM_C / HDLD004 | 43 | 43 | 37 |

`SIM_A` được giữ trọn trong dev. Train dùng `SIM_B` vì nhóm này có ít nhất
một clause cho cả 12 nhãn. Test dùng `SIM_C`, là mẫu hợp đồng khác rõ rệt.

## Chống trùng lặp khi chấm điểm

Manifest giữ nguyên mọi clause trong dataset, nhưng liệt kê `exclusions` để
không chấm những clause của tập sau trùng với tập trước. So sánh chuẩn hóa
khoảng trắng và chữ hoa/thường; near-duplicate dùng độ tương đồng ký tự
`SequenceMatcher >= 0.90`, chiều dài tối thiểu 30 ký tự và tỷ lệ chiều dài
ít nhất 0.85.

- Dev: loại khỏi **phần chấm điểm** 6 clause trùng nguyên văn và 18 clause gần
  trùng train. Không xóa chúng khỏi CSV hay khỏi bản chia.
- Test: không phát hiện cặp vượt ngưỡng so với train/dev.
- Đây là bộ lọc bảo thủ theo văn bản, không chứng minh mọi trường hợp trùng về
  ngữ nghĩa đã được phát hiện. Cần review thủ công trước benchmark chính thức.
- Khi đánh giá segmentation/span, chỉ dùng thêm những row có
  `offset_quality=EXACT`. Row `CONTEXT` vẫn dùng được để hiển thị hoặc bài toán
  phân loại nếu không nằm trong `exclusions`, nhưng không phải gold exact span.

Teammate có thể đọc `splits[<tập>].contracts` để lọc `contract_id` trong CSV;
trước khi tính metric trên dev/test, bỏ các `clause_id` thuộc
`splits[<tập>].excluded_clause_ids`. Không dùng số liệu từ bản chia này làm
benchmark cuối kỳ: mới có ba template family độc lập, dev không có nhãn
`TERMINATION`, còn nhiều nhãn chỉ có 1–2 ví dụ mỗi tập.

## Phân bố nhãn và hướng thu thập tiếp

Snapshot v05 có 183 clause / 12 nhãn. Các nhãn có ít hơn 10 mẫu là
`WORKING_CONDITIONS` (6), `CONTRACT_TERM` (7) và `WORKING_TIME` (9); nhãn nhiều
nhất là `COMPENSATION_BENEFITS` (32). Ngưỡng 10 chỉ dùng để **ưu tiên tìm dữ
liệu**, không phải tiêu chuẩn chất lượng hay lý do nhân bản ví dụ.

Đợt kế tiếp nên annotate HDLD005 đã có raw text, rồi tìm thêm hợp đồng thuộc
template family khác, đặc biệt có nội dung cho ba nhãn ít mẫu. HDLD006 đang
`HOLD_NEAR_DUPLICATE` với HDLD005; không đưa tự động vào tập đánh giá. Sau khi
có thêm nhóm độc lập, tạo split version mới và mới quyết định dev/test cố định.

## Tái tạo và kiểm tra

Từ thư mục repo data:

```powershell
python scripts/build_provisional_split.py --dataset-version v05
python -m unittest discover -s tests -v
```

Manifest chứa SHA-256 của `clauses_v05.csv` để nhận biết khi nguồn thay đổi.
Nếu dataset mới là v06, cần thiết kế lại bản chia và tạo manifest mới; không
ghi đè `provisional_v05.json` bằng nội dung v06.
