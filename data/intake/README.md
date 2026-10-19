# Hàng chờ kiểm tra nguồn hợp đồng

Thư mục này nằm trong repo trên ổ D. `manifest.csv` ghi URL nguồn, đường dẫn
tệp, SHA-256 và trạng thái QC. Bản gốc trong `private/` và `restricted/`
chỉ lưu trên máy, được Git ignore; `restricted/` dành cho tệp chưa loại trừ
thông tin cá nhân.

`HDLD007.docx` đã có sẵn tại `data/raw/contracts/` trước lượt chuyển tệp
ngày 13/10. Hash khớp hồ sơ ngày 05/10/2026 nên không ghi đè. Vòng tìm nguồn
ngày 19/10 bổ sung hai mẫu DOCX hợp lệ, một DOCX bị hỏng và ba hồ sơ PDF có
hợp đồng đã điền. Xem `docs/archive/reports/CONTRACT_INTAKE_QC_2026-10-19.md` để biết trang
chứa hợp đồng, kiểm tra trùng mẫu và quyết định cho từng nguồn.

Ngày 19/10 đã tích hợp hai mẫu hợp lệ theo quy trình HDLD007: LTV Law thành
`HDLD008` / `SRC003` / `SIM_F`, LegalZone thành `HDLD009` / `SRC004` / `SIM_G`.
File đã có tại `data/raw/contracts/`, raw text trích bằng Word nằm tại
`data/processed/raw_text/`; metadata và `docs/data_sources.md` là sổ quản lý
chính. Hai bản trùng trong intake đã được chuyển vào Recycle Bin sau khi
kiểm khớp hash; manifest hiện trỏ thẳng đến HDLD008/009 trong raw.

Receipt của DOCX bị hỏng giữ URL, hash và dung lượng lịch sử, `local_path`
để trống và trạng thái `REMOVED_INVALID_DOCX`. Không coi các trường hash/bytes
ở row này là cam kết còn lưu binary. Hai ảnh contact-sheet đã bỏ vì có thể
tái tạo từ PDF và chứa thêm bản sao thông tin cá nhân.

**Chưa tệp nào được duyệt cho T1.** Hai mẫu nhận raw local đang `TO_ANNOTATE`;
nội dung giữ ngoài Git như HDLD007 chờ quyền tái phân phối. Hồ sơ thực tế
còn PII vẫn ở hàng chờ, chưa nhận raw/metadata/release. Nếu tách hoặc ẩn danh,
lưu bản dẫn xuất riêng, giữ hash và trang nguồn để truy vết. Bảy hợp đồng trong hồ sơ An Giang dùng
chung một khuôn, không được tính như bảy nguồn độc lập.
