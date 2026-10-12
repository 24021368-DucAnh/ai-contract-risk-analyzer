# Tiến độ Data Lead sau mốc tuần 2 — 05/10/2026

## Đã làm ở local

- Annotate `HDLD005` (mẫu hỗ trợ, phục vụ theo Phụ lục II Thông tư
  05/2023/TT-BNV): **51 clause REVIEWED**, tất cả có offset `EXACT` vào
  `raw_text/HDLD005.txt`. Phần hành chính, chữ ký và footnote hướng dẫn điền
  mẫu và mục “nghĩa vụ khác theo thỏa thuận” chưa điền không được gán nhãn.
  Hai nhánh thời hạn ở Điều 1 là lựa chọn thay thế,
  không phải hai điều khoản cùng áp dụng cho một hợp đồng đã ký.
- Tạo `clauses_v06.csv`: **234 clause / 5 hợp đồng / 12 nhãn**. Giữ nguyên
  toàn bộ 183 row v05. Tổng offset: 225 `EXACT`, 9 `CONTEXT`.
- Nhận `HDLD007.docx` và trích `HDLD007.txt`, gán `SIM_E`, trạng thái
  `TO_ANNOTATE`. File này **chưa** nằm trong v06 hoặc các split.
- Tạo `provisional_v06.json`; đây vẫn là split **tạm**, không phải test set
  cố định cuối kỳ.

## Bản chia v06

| Tập | Nhóm / hợp đồng | Tổng clause | Có thể chấm điểm | Exact span có thể chấm |
|---|---|---:|---:|---:|
| Train | SIM_B/HDLD003 + SIM_D/HDLD005 | 112 | 112 | 110 |
| Dev | SIM_A/HDLD001–002 | 79 | 49 | 48 |
| Test | SIM_C/HDLD004 | 43 | 34 | 28 |

30 row dev và 9 row test trùng/gần trùng với tập trước được ghi trong
`exclusions` của manifest; vẫn giữ nguyên trong CSV, nhưng không tính F1.
Sau kiểm tra sâu, ngưỡng near-duplicate của v06 giảm từ 0.90 xuống 0.85:
8 row thêm vào exclusions là các biến thể template về phối hợp công việc,
nghỉ phép/nghỉ lễ, nâng lương và thời gian nghỉ trong ngày. v05 giữ quy tắc
0.90 để tái tạo mốc lịch sử; không dùng mốc đó làm benchmark đã khóa.
Hash SHA-256 của `clauses_v06.csv` là
`6ba5bede89cabf127697dbdfc781fe7742c0d8dfcb4c6a757315a4fd2f8aa981`.

## Việc tiếp theo

1. Gán nhãn `HDLD007` theo guideline, có offset vào bản raw text hiện tại;
   chỉ sau QC mới tạo v07. Kiểm tra kỹ các câu dẫn chiếu luật trong mẫu,
   nhưng không sửa văn bản nguồn theo trí nhớ.
2. Tiếp tục tìm template khác họ, nhất là điều khoản về công cụ, thiết bị,
   điều kiện vật chất. `WORKING_CONDITIONS` hiện chỉ có **7** row, ít nhất
   trong 12 nhãn.
3. Sau khi có thêm nhóm độc lập, tạo lại split và đánh giá leakage từng
   clause; chưa khóa test set.

Phần dataset v06, split, script, test và tài liệu được chuẩn bị đưa lên branch
data theo yêu cầu người dùng. DOCX và raw text HDLD007 giữ local, chưa đưa lên
Git vì chưa xác nhận quyền tái phân phối; URL và hash vẫn có trong hồ sơ QC.
