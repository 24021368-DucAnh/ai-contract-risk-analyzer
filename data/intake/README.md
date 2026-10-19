# Hàng chờ kiểm tra nguồn hợp đồng

Thư mục này nằm trong repo trên ổ D. `manifest.csv` ghi URL nguồn, đường dẫn
tệp, SHA-256 và trạng thái QC. Bản gốc trong `private/` và `restricted/`
chỉ lưu trên máy, được Git ignore; `restricted/` dành cho tệp chưa loại trừ
thông tin cá nhân.

`HDLD007.docx` đã có sẵn tại `data/raw/contracts/` trước lượt chuyển tệp
ngày 13/10. Hash khớp hồ sơ ngày 05/10/2026 nên không ghi đè. Vòng tìm nguồn
ngày 19/10 bổ sung hai mẫu DOCX hợp lệ, một DOCX bị hỏng và ba hồ sơ PDF có
hợp đồng đã điền. Xem `docs/CONTRACT_INTAKE_QC_2026-10-19.md` để biết trang
chứa hợp đồng, kiểm tra trùng mẫu và quyết định cho từng nguồn.

**Chưa tệp nào trong intake được duyệt cho T1.** Mẫu trống chỉ phục vụ thử
pipeline; hồ sơ thực tế vẫn có thông tin cá nhân và quyền tái sử dụng chưa
được xác nhận. Không chuyển chúng sang `data/raw/contracts/`, metadata hay
release. Không sửa bản gốc; nếu tách hoặc ẩn danh, lưu bản dẫn xuất riêng,
giữ hash và trang nguồn để truy vết. Bảy hợp đồng trong hồ sơ An Giang dùng
chung một khuôn, không được tính như bảy nguồn độc lập.
