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

## Quy trình nhận hợp đồng T1 (tuần 2 của kế hoạch mới)

T1 cần ít nhất 10 **hợp đồng gốc độc lập**, tách khỏi D1/D2, dữ liệu few-shot
và prompt. Ưu tiên đủ PDF và DOCX, nhiều kiểu đánh số, ngành và độ dài.
Một biểu mẫu chưa điền, nhiều bản cùng khuôn, hoặc phụ lục của cùng hợp đồng
không được tính thành các hợp đồng độc lập. `t1_eligible=no` trong manifest
chỉ đổi sau khi hoàn tất mọi cổng dưới đây; không suy ra quyền dùng từ việc
URL tải được công khai.

1. **Nguồn và quyền dùng:** ghi đúng `source_page`, `source_file`, ngày nhận,
   định dạng, dung lượng và SHA-256 của bản gốc. Xác minh quyền lưu, xử lý,
   chia sẻ nội bộ và đưa bản đã ẩn danh vào bộ đánh giá. Nếu chưa rõ, giữ
   trong `private/` hoặc `restricted/` và ghi `HOLD` trong `qc_status`.
2. **Bản gốc và tính độc lập:** xác định chính xác trang chứa hợp đồng, phân
   biệt hợp đồng đã ký với mẫu, phụ lục và hồ sơ đính kèm. So hash, văn bản
   trích và cấu trúc với D1/D2, T1 đã nhận; gán `similarity_group`. Giữ cả
   nhóm cùng một tập, không đếm những bản cùng mẫu thành nhiều nguồn độc lập.
3. **Ẩn danh trên bản dẫn xuất:** rà cả trang scan, hình, bảng, header/footer,
   chữ ký và metadata tệp. Che tên, địa chỉ, số định danh, điện thoại, email,
   tài khoản, chữ ký, con dấu và dữ liệu có thể nhận diện gián tiếp; sau đó
   xuất bản dẫn xuất riêng. Không sửa bản gốc. Kiểm lại bằng mắt từng trang
   của bản dẫn xuất và thử trích text/copy để phát hiện lớp chữ còn sót.
4. **Hai người nghiệm thu:** một người thực hiện, người thứ hai kiểm độc lập
   bản dẫn xuất, quyền dùng, khả năng đọc, tính độc lập và phạm vi che. Ghi
   reviewer, ngày, quyết định và lý do trong hồ sơ QC của ứng viên; nếu bất
   đồng thì giữ `HOLD`. Chỉ khi có đủ bằng chứng mới chuyển vào T1.
5. **Khóa tập test:** ghi hash bản dẫn xuất và nguồn gốc để Evaluation Lead
   kiểm chứng. Không dùng nội dung hay gold T1 để sửa prompt, model, cấu hình,
   guideline hoặc hệ thống. Gold T1 chỉ gán sau mốc MS-1 đóng băng taxonomy,
   severity rubric và guideline; phải lưu người gán, người xác minh, bất đồng
   và tỷ lệ gán đôi theo BRD §8.2.

**Hồ sơ hiện tại:** HDLD007–009 là mẫu phát triển và còn chờ quyền tái phân
phối; MOJ gần trùng HDLD003; KTBK là bundle chưa xác định quyền/nhóm trùng;
bốn hồ sơ PDF có thông tin cá nhân hoặc các trang scan cần xử lý; mẫu DOCX
Quảng Ngãi bị hỏng đã loại. Không hồ sơ nào được chuyển sang T1 ở bước này.
