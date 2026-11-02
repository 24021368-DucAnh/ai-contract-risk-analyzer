# Đối chiếu nguồn cục bộ cho clauses v07 — 29/10/2026

Phạm vi: đối chiếu `data/raw/contracts/HDLD010.pdf`–`HDLD013.pdf` với
`data/intake/manifest.csv` và các PDF đã lưu trong khu vực `restricted/`.
Đây là kiểm tra kỹ thuật cục bộ bằng SHA-256 và dấu vân tay 5 từ trên lớp text
PDF. Không xuất nội dung hợp đồng, ảnh trang hoặc thông tin cá nhân. Kết quả
không thay thế việc kiểm bằng mắt, xác minh quyền xử lý hay duyệt pháp lý.

| File local | Trang | Kết quả đối chiếu | Trạng thái |
| --- | ---: | --- | --- |
| `HDLD010.pdf` | 4 | Không trùng SHA-256 với manifest. Mức phủ 5 từ cao nhất chỉ 14,5% với `CAND-MOH-MINHTIEN-2020`; chưa đủ gán nguồn. Trang 4 không có lớp text trích được. | Chưa xác minh nguồn, giữ `NEEDS_REVIEW`. |
| `HDLD011.pdf` | 4 | Không trùng SHA-256; mức phủ cao nhất 2,5% với các PDF manifest. Chưa có clause v07. | Chưa xác minh nguồn. |
| `HDLD012.pdf` | 6 | SHA-256 trùng chính xác `CAND-MOH-LONGCHAU-2021` trong manifest (`305782cb8390beaf26beb6b2cacaf74fe551043f5974ff7cfbf6fa67a751c028`). | Nguồn đã liên kết; candidate vẫn `HOLD_ACTUAL_PII_REUSE_RIGHTS_SOURCE_CONTEXT`, `t1_eligible=no`. |
| `HDLD013.pdf` | 4 | Không trùng SHA-256 toàn tệp. Cả bốn trang có 100% dấu vân tay 5 từ xuất hiện tại các trang PDF 23–26, theo đúng thứ tự, của `CAND-HP-HOSPITAL-2025` (manifest có 37 trang). | Liên kết nội dung ở mức lớp text; ranh giới hợp đồng, ảnh/scan, quyền và ẩn danh chưa được duyệt. Candidate vẫn `HOLD_PII_REUSE_RIGHTS_VISUAL_BOUNDARY`, `t1_eligible=no`. |

`HDLD012.pdf` là bản trùng nguyên byte với PDF nguồn mà manifest ghi còn PII
và chữ ký. Bản này đang nằm trong `data/raw/contracts/` local, ngoài khu vực
`restricted/`; cần rà lại cách lưu trữ và các bản dẫn xuất trước khi chia sẻ
hoặc đưa vào release. Không tự di chuyển/xóa file vì v07 đang tham chiếu đến
raw text của nó và phải giữ chuỗi truy vết hiện tại.

Kiểm tra lớp text chỉ cho phép liên kết kỹ thuật; không chứng minh tệp đã được
ẩn danh hoặc chỉ chứa một hợp đồng. Với `HDLD013`, manifest trước đây mới nêu
ít nhất một hợp đồng ở trang 23–24 và khả năng có bản khác trong cùng hồ sơ.
Cần người kiểm độc lập xác nhận trang 25–26 thuộc hợp đồng nào trước khi chốt
đơn vị dữ liệu, `similarity_group` hoặc metadata release.

## Việc còn mở

1. Tìm receipt gốc và quyền xử lý cho `HDLD010`; không gán source ID bằng mức
   giống văn bản 14,5%.
2. Xác minh ranh giới và bản ẩn danh của `HDLD012`/`HDLD013` bằng người kiểm
   độc lập; giữ trạng thái HOLD và `NEEDS_REVIEW` cho tới lúc có bằng chứng.
3. Sau khi có metadata hợp lệ, đối chiếu số clause v07: `HDLD010=23`,
   `HDLD012=36`, `HDLD013=13`. Chỉ khi bản snapshot được chốt mới thay
   `dataset_version`; metadata v06 hiện vẫn phản ánh bản release trước.

Không có hợp đồng mới được nghiệm thu vào T1 hoặc tập 20 bổ sung từ lần đối
chiếu này.
