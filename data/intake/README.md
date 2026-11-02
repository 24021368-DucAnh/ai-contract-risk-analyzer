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

### Trạng thái hiện tại của manifest

**Hàng chờ theo từng hợp đồng:** `contract_unit_review_queue.csv` tách 10
đơn vị hợp đồng được nêu trong QC lịch sử từ bốn PDF nguồn. Các bản này đều
`HOLD`: chưa đủ quyền sử dụng, ẩn danh và duyệt độc lập; không tăng số mẫu
được nhận. Kiểm tra bằng `python scripts/validate_intake_gate.py`; xem
`docs/CONTRACT_SOURCE_HOLDER_REQUEST_AND_REVIEW.md` để xin nguồn và nghiệm thu.
Tuyến liên hệ công khai đã rà soát ngày 28/10 (không phải quyền sử dụng):
`source_contact_routes_2026-10-28.csv` và
`docs/SOURCE_HOLDER_CONTACT_RESEARCH_2026-10-28.md`. Mọi tuyến đều chưa gửi
yêu cầu và chưa xác minh thẩm quyền của các bên ký.
Mười PDF khác trong manifest có bảng sàng lọc ưu tiên nguồn riêng
additional_signed_lead_triage_2026-10-28.csv và
docs/ADDITIONAL_SIGNED_LEAD_TRIAGE_2026-10-28.md. Đây là hồ sơ chờ xác minh
và **không** cộng thêm hợp đồng đã ký/được nghiệm thu vào T1 hoặc 20 bổ sung.
Manifest vẫn là receipt nguồn/tệp; hàng chờ này không tự sửa `t1_eligible`.
Đã bổ sung 10 hồ sơ này vào `source_holder_outreach_queue.csv` để chuẩn bị
xác minh bên có thẩm quyền, và 10 tuyến công khai vào
`source_contact_routes_2026-10-28.csv`. Tổng hàng chờ xin quyền hiện là
14 nguồn, 17 tuyến/đầu mối tham chiếu (có các địa chỉ công khai lặp lại theo
từng hồ sơ). Tất cả đều `NOT_SENT`, chưa ai xác minh quyền cấp phép.
Riêng PDF từ CDN Hải Phòng có tuyến Cổng thành phố; chưa xác định đơn vị
thực sự phát hành hoặc chủ thể cấp quyền.

**Đợt giới thiệu đầu mối (28/10/2026):**
`source_referral_batches_2026-10-28.csv` gom 14 ứng viên đang chờ quyền thành
5 nhóm theo cổng An Giang, Quảng Ngãi, VIMDA/Bộ Y tế, Sở Y tế Hải Phòng và
Cổng thành phố Hải Phòng. Đối chiếu bằng mã đã xác nhận 14/14 ứng viên được
phủ đúng một lần, 14 cặp ứng viên/tuyến trùng khớp bảng 17 tuyến liên hệ.
Tất cả nhóm ở `DRAFT_ONLY`, chủ thể có quyền chưa xác minh và thư chưa gửi.
Mẫu thư giới thiệu đầu mối và lời mời đối tác cấp hợp đồng thật nằm tại
`docs/SIGNED_CONTRACT_REFERRAL_AND_PARTNER_PACK_2026-10-28.md`. Chỉ khi được
cấp phép hợp lệ và duyệt độc lập mới bắt đầu nhập dữ liệu hợp đồng.

**Nguồn giới thiệu doanh nghiệp ngoài 14 hồ sơ:** bảng
`consenting_employer_referral_routes_2026-10-28.csv` và tài liệu
`docs/CONSENTING_EMPLOYER_REFERRAL_RESEARCH_2026-10-28.md` ghi năm đầu mối
liên hệ tổ chức công khai (VCCI có hai đầu mối, VINASME, VINASA, HAWA) với
khả năng giới thiệu doanh nghiệp tự nguyện. Các đầu mối đang `RESEARCH_ONLY`,
chưa liên hệ và chưa có doanh nghiệp/hợp đồng hay quyền xử lý nào được xác minh.
Không cộng đầu mối hiệp hội vào số hợp đồng nghiệm thu.

**Phiếu xác nhận quyền đóng góp (bản nháp 28/10/2026):**
`docs/CONTRACT_CONTRIBUTION_PERMISSION_FORM_DRAFT_2026-10-28.md`
đưa ra các lựa chọn quyền riêng cho lưu bản gốc, xử lý cục bộ, tạo bản dẫn
xuất ẩn danh, dùng trong T1 kín hoặc tập bổ sung và sử dụng dịch vụ AI bên thứ
ba (mặc định không cho phép). Phiếu hiện ở trạng thái `DRAFT_ONLY`, chưa ký,
chưa được người có chuyên môn pháp lý duyệt và không phải bằng chứng có quyền
nhập dữ liệu. VCCI có hai địa chỉ email khác tên miền trong các trang công khai;
cần xác nhận đầu mối thực tế qua điện thoại chính thức trước khi gửi yêu cầu.

Manifest hiện có 22 ứng viên: 2 ở trạng thái `REGISTERED_LOCAL_TO_ANNOTATE`,
15 ở các trạng thái `HOLD_*`, 1 ở trạng thái
`LOCAL_DEV_HOLD_REDISTRIBUTION`, 3 ở các trạng thái `EXCLUDED_*` và 1 ở
trạng thái `REMOVED_*`. Cả 22 ứng viên đều có `t1_eligible=no`.

`HDLD008` và `HDLD009` vẫn là các mẫu phát triển trong hàng chờ, không phải
dữ liệu T1 đã được duyệt. Manifest là nguồn tham chiếu cho trạng thái intake
hiện tại; các báo cáo QC theo ngày được giữ làm bằng chứng lịch sử và không
tự động phản ánh trạng thái mới nhất.

Receipt của DOCX bị hỏng giữ URL, hash và dung lượng lịch sử, `local_path`
để trống và trạng thái `REMOVED_INVALID_DOCX`. Không coi các trường hash/bytes
ở row này là cam kết còn lưu binary. Hai ảnh contact-sheet đã bỏ vì có thể
tái tạo từ PDF và chứa thêm bản sao thông tin cá nhân.

**Chưa có ứng viên nào được duyệt cho T1.** Hai ứng viên đã đăng ký annotate
chưa đồng nghĩa với việc quyền tái phân phối đã được xác nhận hoặc dữ liệu
đã được chấp nhận vào dataset. Các hồ sơ còn PII/chữ ký, chưa rõ quyền sử
dụng hoặc chưa qua đủ cổng kiểm tra phải tiếp tục được giữ ngoài release.

Nếu tạo bản ẩn danh, lưu bản dẫn xuất riêng, giữ provenance cần thiết để truy
vết và kiểm tra bản dẫn xuất trước khi xem xét đưa vào tập đánh giá. Bảy hợp
đồng trong hồ sơ An Giang dùng chung một khuôn, không được tính như bảy nguồn
độc lập.
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
các hồ sơ PDF giữ trong `restricted/` có PII/scan hoặc quyền dùng chưa rõ;
mẫu DOCX Quảng Ngãi bị hỏng đã loại. Không hồ sơ nào được chuyển sang T1 ở
bước này.

### Kiểm tra thêm ngày 20/10/2026

Ứng viên `CAND-MOH-LONGCHAU-2021` được tải từ [tệp PDF trên cổng VIMDA
thuộc Bộ Y tế](https://vimda.moh.gov.vn/documents/10182/25329986/upload_00043800_1641803953228.pdf?fileId=25383880&version=1.0).
Sáu trang có text trích được: trang 1–4 là hợp đồng lao động đã điền và ký;
trang 5–6 là tài liệu nhân sự liên quan, không tự tính thành hợp đồng khác.
Bản PDF có tên, số định danh, địa chỉ và chữ ký đọc được; giữ nguyên trong
`restricted/`, ngoài Git. So 5-gram đối xứng với raw text HDLD001–009 cho
mức cao nhất 0,1141 (HDLD002), nên ghi nhóm độc lập **tạm thời**. Chưa có
trang hồ sơ gốc giải thích ngữ cảnh công bố và chưa xác nhận quyền tái sử dụng;
chưa có bản dẫn xuất ẩn danh hoặc người kiểm thứ hai. Vì vậy `t1_eligible=no`.
Hash, dung lượng và URL chính xác nằm trong `manifest.csv`; không chép thông
tin cá nhân vào Git hay báo cáo QC.

### Sàng lọc bổ sung ngày 20/10/2026

Đã thêm 11 hồ sơ từ cổng VIMDA/Bộ Y tế và hồ sơ công bố của Sở Y tế Hải Phòng
vào manifest; bản tải được giữ trong `restricted/` và bị Git ignore. Kết quả
phân loại: có hồ sơ PDF trích được chữ, nhiều hồ sơ scan cần OCR; một bản
VIMDA trùng HDLD003 cao (0,4839) và bị loại khỏi T1; một bản là hợp đồng
làm việc viên chức, ngoài phạm vi HĐLĐ nên bị loại. Một hồ sơ bệnh viện Hải
Phòng chứa ít nhất hai HĐLĐ trong cùng một bộ công bố và được gắn chung nhóm,
không mặc định tính hai mẫu độc lập.

Các hồ sơ còn lại đều chưa qua đủ cổng: còn PII/chữ ký, quyền tái sử dụng và
ngữ cảnh công bố chưa xác minh, hoặc ranh giới hợp đồng/chất lượng OCR chưa
kiểm tra. Do đó tổng `t1_eligible=yes` vẫn là **0**. Đã tìm được nhiều hơn
13 đường dẫn/ứng viên, nhưng đó không phải 13 hợp đồng T1 đạt chuẩn; cần quyền
dùng được xác nhận và hai người nghiệm thu bản ẩn danh trước khi annotate.
