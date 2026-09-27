# Data Sources

Danh sách các nguồn hợp đồng lao động tiếng Việt được khảo sát và sử dụng cho project **AI Contract Risk Analyzer**.

## 1. Danh sách nguồn

| Source ID | Tên nguồn | Link | Loại nguồn | Số hợp đồng đã lấy | Trạng thái | Ghi chú |
|---|---|---|---|---:|---|---|
| `SRC001` | Thư Viện Pháp Luật | https://thuvienphapluat.vn/ | Mẫu hợp đồng lao động / biểu mẫu pháp lý tiếng Việt | 6 | Đã tải | Gồm `HDLD001`–`HDLD006`. Một số tài liệu là mẫu tham khảo; `HDLD004`–`HDLD006` có căn cứ văn bản pháp luật ghi trực tiếp trong tài liệu. |

> Với `HDLD001`–`HDLD003`, URL trang tải gốc chưa được lưu từ thời điểm thu thập ban đầu. Không tự điền URL đoán; cần truy vết lại nếu project yêu cầu provenance đầy đủ.

## 2. Truy vết từng hợp đồng

| Contract ID | Source ID | File raw | Loại hợp đồng | Trạng thái dữ liệu | Similarity group | Nguồn/ghi chú truy vết |
|---|---|---|---|---|---|---|
| `HDLD001` | `SRC001` | `data/raw/contracts/HDLD001.doc` | Mẫu HĐLĐ chung | Đã annotate | `SIM_A` | URL gốc: TODO truy vết lại |
| `HDLD002` | `SRC001` | `data/raw/contracts/HDLD002.doc` | HĐLĐ xác định thời hạn | Đã annotate | `SIM_A` | URL gốc: TODO truy vết lại; near-duplicate với `HDLD001` |
| `HDLD003` | `SRC001` | `data/raw/contracts/HDLD003.doc` | HĐLĐ không xác định thời hạn | Đã annotate | `SIM_B` | URL gốc: TODO truy vết lại |
| `HDLD004` | `SRC001` | `data/raw/contracts/HDLD004.docx` | HĐLĐ giúp việc gia đình | Đã annotate | `SIM_C` | Trang tham khảo: https://thuvienphapluat.vn/hoi-dap-phap-luat/mau-hop-dong-lao-dong-giup-viec-gia-dinh-moi-nhat-338634.html |
| `HDLD005` | `SRC001` | `data/raw/contracts/HDLD005.docx` | HĐLĐ thực hiện công việc hỗ trợ, phục vụ | Chờ annotate | `SIM_D` | Mẫu ghi rõ Phụ lục II Thông tư 05/2023/TT-BNV; trang tải/tham khảo: https://thuvienphapluat.vn/banan/tin-tuc/tai-mau-hop-dong-lao-dong-theo-nghi-dinh-111-2022-nd-cp-moi-nhat-2026-mau-hop-dong-theo-nghi-dinh-11-20855.html |
| `HDLD006` | `SRC001` | `data/raw/contracts/HDLD006.docx` | HĐLĐ thực hiện công việc chuyên môn, nghiệp vụ | Giữ raw / chưa annotate full | `SIM_D` | Near-duplicate/template-family với `HDLD005`; giữ để kiểm thử duplicate và truy vết nguồn |

## 3. Quy ước ID

- `SRCxxx`: định danh **nguồn/publisher** dữ liệu.
- `HDLDxxx`: định danh từng hợp đồng/tài liệu cụ thể.
- Một nguồn có thể cung cấp nhiều hợp đồng.
- `SIM_X`: nhóm template/similarity. Các hợp đồng trong cùng nhóm phải được giữ cùng dataset split để tránh leakage.

## 4. Quy ước trạng thái nguồn

- `Chưa kiểm tra`: mới tìm thấy nguồn.
- `Đã kiểm tra`: đã mở và xác nhận có dữ liệu phù hợp.
- `Đã tải`: đã lưu file raw vào `data/raw/contracts/`.
- `Loại bỏ`: dữ liệu không phù hợp với project.

## 5. Quy ước trạng thái từng hợp đồng

Các giá trị tương ứng với cột `dataset_status` trong `contracts_metadata.csv`:

- `ANNOTATED`: đã segment + gán `clause_type` + review, có mặt trong dataset processed hiện tại.
- `TO_ANNOTATE`: file raw đã sẵn sàng nhưng chưa đưa vào dataset processed.
- `HOLD_NEAR_DUPLICATE`: chủ động chưa annotate full vì near-duplicate với contract khác.
- `EXCLUDED`: không sử dụng cho dataset.

## 6. Checklist kiểm tra nguồn

Mỗi nguồn/hợp đồng cần kiểm tra:

- Có phải hợp đồng lao động tiếng Việt không?
- Là hợp đồng thật hay mẫu hợp đồng?
- Có thể tải xuống và lưu trữ phục vụ project không?
- Có đủ nội dung điều khoản không?
- Có dữ liệu trùng lặp hoặc gần trùng lặp không?
- Có thông tin cá nhân cần ẩn danh không?
- Có giới hạn sử dụng/bản quyền cần lưu ý không?
- Có lưu được URL chính xác của trang/file gốc để truy vết không?
- Có xác định được `similarity_group` trước khi chia train/dev/test không?

## 7. Trạng thái hiện tại

- Raw contracts: **6**
- Contracts đã annotate: **4** (`HDLD001`–`HDLD004`)
- Contract tiếp theo: **`HDLD005`**
- Contract hold near-duplicate: **`HDLD006`**
- Dataset processed hiện tại: **`data/processed/clauses_v03.csv` — 183 clauses**
