# Data Sources

Danh sách các nguồn hợp đồng lao động tiếng Việt được khảo sát và sử dụng cho project AI Contract Risk Analyzer.

| Source ID | Tên nguồn | Link | Loại nguồn | Số hợp đồng đã lấy | Trạng thái | Ghi chú |
|---|---|---|---|---:|---|---|
| SRC001 | Thư Viện Pháp Luật | TODO: bổ sung URL trang tải gốc | Mẫu hợp đồng lao động tiếng Việt | 3 | Đã tải | Gồm HDLD001, HDLD002, HDLD003; đều là mẫu tham khảo |

## Quy ước ID

- `SRCxxx`: định danh nguồn dữ liệu.
- `HDLDxxx`: định danh từng hợp đồng/tài liệu cụ thể.
- Một nguồn có thể cung cấp nhiều hợp đồng.

## Quy ước trạng thái

- `Chưa kiểm tra`: mới tìm thấy nguồn.
- `Đã kiểm tra`: đã mở và xác nhận có dữ liệu phù hợp.
- `Đã tải`: đã lưu dữ liệu vào `data/raw/contracts/`.
- `Loại bỏ`: dữ liệu không phù hợp với project.

## Ghi chú kiểm tra nguồn

Mỗi nguồn cần kiểm tra:

- Có phải hợp đồng lao động tiếng Việt không?
- Là hợp đồng thật hay mẫu hợp đồng?
- Có thể tải xuống và lưu trữ phục vụ project không?
- Có đủ nội dung điều khoản không?
- Có dữ liệu trùng lặp hoặc gần trùng lặp không?
- Có thông tin cá nhân cần ẩn không?
- Có giới hạn sử dụng hoặc bản quyền cần lưu ý không?
- Có lưu được URL chính xác của trang/file gốc để truy vết nguồn không?
