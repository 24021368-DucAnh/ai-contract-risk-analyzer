# Kiểm tra nguồn hợp đồng bổ sung — 19/10/2026

Phạm vi: chỉ sàng lọc nguồn để xây dựng dữ liệu dự án. Tệp tải về nằm tại
`data/intake/private/` hoặc `data/intake/restricted/` trên máy của Data Lead;
hai thư mục này được Git ignore. `data/intake/manifest.csv` là receipt sàng
lọc, ghi URL, dung lượng và SHA-256 bản tải. Sau đối chiếu cấu trúc repo,
hai mẫu hợp lệ đã được nhận raw local thành HDLD008/009 như mục bổ sung cuối
báo cáo. Dataset v06, nhãn và split lịch sử giữ nguyên.

## Kết quả

| ID | Nguồn | Kiểm tra tệp và nội dung | Quyết định |
|---|---|---|---|
| CAND-LTVLAW-2026 | [LTV Law](https://ltvlaw.com/tin-tuc/hop-dong-lao-dong), [DOCX](https://ltvlaw.com/mau-don/hop-dong-lao-dong.docx) | DOCX hợp lệ, không macro; 8 dấu mốc Điều, khoảng 563 từ, 24 dấu chỗ trống; không thấy chuỗi số 9–12 chữ số trong text trích xuất. Trùng 5-gram tối đa 15,2% với HDLD007. | **Giữ làm mẫu thử dev**, chưa xác nhận quyền tái sử dụng; không phải hợp đồng gốc T1. |
| CAND-LEGALZONE-2026 | [LegalZone](https://legalzone.vn/hop-dong-lao-dong-cong-nhan/), [DOCX](https://legalzone.vn/wp-content/uploads/legalzone-templates-2026/mau-hop-dong-lao-dong-cong-nhan.docx) | DOCX hợp lệ, không macro; 12 dấu mốc Điều, khoảng 2.924 từ kể cả bảng, 31 dấu chỗ trống; không thấy chuỗi số 9–12 chữ số. Trùng 5-gram tối đa 2,6% với HDLD007. | **Giữ làm mẫu thử dev** vì cấu trúc công nhân/ca kíp khác; chưa phải hợp đồng gốc T1. |
| CAND-QN-SERVICE-2026 | [Cổng UBND xã Thiện Tín](https://thientin.quangngai.gov.vn/van-ban/cong-van-giao-so-luong-hop-dong-lao-dong-theo-nghi-dinh-173-2025-nd-cp.html), [DOCX](https://thientin.quangngai.gov.vn/upload/2007031/20260403/%C3%9D%20%20-%20H%E1%BB%A2P%20%C4%90%C3%94NG%20LAO%20%C4%90%E1%BB%98NG%20TH%E1%BB%B0C%20HI%E1%BB%86N%20NHI%E1%BB%86M%20V%E1%BB%A4%20THEO%20%20Th%C3%B4ng%20t%C6%B0%2016.2025%20%28M%C6%A0%29.docx) | Server trả 43.996 byte và MIME DOCX nhưng ZIP thiếu phần kết; trình đọc báo `BadZipFile`. | **Loại khỏi corpus**; bản tải chỉ giữ để truy vết lỗi nguồn. |
| CAND-QN-GSP-2025 | [Hồ sơ Sở Y tế Quảng Ngãi](https://syt.quangngai.gov.vn/upload/2006968/20250507/GSP-FVC_CN_Binh_Chanh_065cf.pdf) | PDF scan 19 trang, hợp đồng lao động đã điền ở trang PDF 4–5. Hồ sơ có thêm giấy tờ cá nhân. Không trích được text; chưa OCR, chưa đo được trùng nội dung. | **Giữ hạn chế**; có PII, cần ẩn danh thủ công và xác nhận quyền sử dụng. |
| CAND-QN-VIETMY-2025 | [Hồ sơ Sở Y tế Quảng Ngãi](https://syt.quangngai.gov.vn/upload/2006968/20251118/CV_so_66_PKVM_vv_de_nghi_dang_tai_danh_sach_dang_ky_nguoi_hanh_nghe_tai_PKDK_QT_Viet_My_binh_Son_6f903.pdf) | PDF scan 22 trang, hợp đồng đã điền ở trang PDF 14–18. Các trang khác chứa giấy tờ cá nhân. Không trích được text; chưa OCR. | **Giữ hạn chế**; có PII, cần ẩn danh thủ công và xác nhận quyền sử dụng. |
| CAND-AG-HEALTH-2025 | [Hồ sơ Sở Y tế An Giang](https://syt.angiang.gov.vn/Lists/TinTuc/Attachments/7833/Van%20bang%20-%20chung%20chi%20-%20hop%20dong.pdf) | PDF 50 trang; 7 cặp trang chứa hợp đồng đã điền: **7–8, 14–15, 19–20, 27–28, 35–36, 41–42, 49–50**. Text trích xuất được một phần. Mỗi bản trùng trên 90% 5-gram với ít nhất một bản khác trong cùng hồ sơ; so với HDLD001–007, mức cao nhất khoảng 5,9–6,8%. | **Giữ hạn chế**; 7 bản cùng một khuôn, có PII và chưa xác nhận quyền sử dụng. Không tính là 7 nguồn T1 độc lập. |

Các tỷ lệ trùng là phép đo sàng lọc trên bộ 5 từ liên tiếp sau chuẩn hóa
chữ thường; chúng không thay cho người xác nhận độc lập nguồn/tập mẫu. Với hai
PDF Quảng Ngãi không có text, chưa thể kết luận về trùng lặp. Các chuỗi số
không phát hiện trong hai DOCX chỉ là kiểm tra sơ bộ, chưa phải xác nhận đã
loại hết PII.

## Quyết định về T1 và bước tiếp

- **0/6 nguồn mới đủ điều kiện đưa vào T1 ở thời điểm kiểm tra.** Hai DOCX là
  mẫu trống; một DOCX hỏng; ba PDF là hồ sơ thực tế nhưng còn PII và quyền
  sử dụng chưa được xác nhận. Bảy bản trong một PDF chỉ tạo một nhóm mẫu
  tương tự, không được chia qua dev/test.
- Nếu dùng hai DOCX cho dev, phải giữ nhãn `template`, xác nhận quyền dùng
  và tránh đưa cùng khuôn sang T1. Không tự điền thông tin giả rồi gọi đó là
  hợp đồng thật.
- Muốn dùng hồ sơ PDF, trước tiên cần xác nhận quyền, tách bản dẫn xuất theo
  trang, ẩn danh cả chữ lẫn ảnh/chữ ký/số định danh, kiểm lại bằng người thứ
  hai, sau đó OCR và đối chiếu từng offset với bản text đã hash. Giữ bản gốc
  trong `restricted/`; bản dẫn xuất phải có mã nguồn/trang/hash riêng.
- T1 theo kế hoạch hiện hành cần ít nhất 10 hợp đồng gốc độc lập, đa dạng PDF
  và DOCX. Cách khả thi hơn để đạt mục tiêu là xin bản hợp đồng thật từ các
  thành viên/đơn vị có quyền chia sẻ sau khi được ẩn danh, thay vì cộng các
  mẫu tải công khai. Chưa có căn cứ để gán nhãn rủi ro pháp lý cho các tệp này.

## Tích hợp vào cấu trúc hiện có — 19/10/2026

Quyết định: dùng đúng quy trình HDLD007 thay vì để hai mẫu hợp lệ chỉ nằm
trong intake. Nhận raw local không đồng nghĩa đủ điều kiện T1 hoặc được
phép tái phân phối công khai. Không sửa nội dung nguồn.

- HDLD008 / SRC003 / SIM_F: `data/raw/contracts/HDLD008.docx`, 3 trang.
  SHA-256 nguồn: `0c6e571556d1cf387a4cefcf5eb67f5f4fa63084c753447d5fb9aebf16206b6c`.
  `data/processed/raw_text/HDLD008.txt`: 2.978 code point;
  SHA-256 `224bf16ce6d48935a72ece5852345b57bfb0c2555827ba42b6d841af3f93e135`.
- HDLD009 / SRC004 / SIM_G: `data/raw/contracts/HDLD009.docx`, 8 trang.
  SHA-256 nguồn: `9c290967389d6e27bcf968673182bf7fde4499e59e1d0a2af026adcb9e7fde4c`.
  `data/processed/raw_text/HDLD009.txt`: 13.669 code point;
  SHA-256 `8d08ad89f3932853ce6ec0cf657e0148b98d2826eabbe4d71ef7f565c5cb3cd2`.

Text được trích qua Microsoft Word read-only, cùng phép chuyển paragraph,
table marker, whitespace và UTF-8/LF như script hiện có; không chạy lại hay
ghi đè HDLD001–007. Word báo số trang theo môi trường máy hiện tại.
Tính lại đúng phép containment đối xứng hiện có: giao 5-gram chia tập nhỏ
hơn (giữ dấu tiếng Việt, lowercase, bỏ dấu câu), so với tất cả HDLD001–009:
HDLD008 tối đa **0.1541** với HDLD007; HDLD009 tối đa **0.0807** với HDLD008.
Đây là phép đo khác các tỷ lệ sàng lọc ban đầu trong bảng phía trên.

Metadata đăng ký cả hai là `TO_ANNOTATE`, clause_count và dataset_version
để trống. Bốn file nội dung được Git ignore như HDLD007. Nguồn chính nằm
trong `docs/data_sources.md`; intake receipt vẫn truy vết bản tải gốc.

### Nhật ký thực hiện kế hoạch Data Lead

- [x] Đọc schema, metadata, data_sources, quy trình raw text và source-intake tests.
- [x] Nhận HDLD008/009 theo ID, thư mục và trạng thái hiện có.
- [x] Trích text, ghi hash, số trang, so trùng bằng cùng phương pháp.
- [x] Kiểm kê sơ bộ D1: xem `D1_DATA_INVENTORY_2026-10-19.md`.
- [ ] Nhóm chốt D1 4 hay 5 hợp đồng; người thứ hai review PII và nhãn.
- [ ] MS-1: freeze guideline và chính sách single-label/đa nhãn cùng AI Leads.
- [ ] Thu T1 >=10 hợp đồng gốc độc lập có quyền sử dụng và đã ẩn danh.

Ruling: làm trực tiếp trong repo ổ D và nhánh hiện có theo yêu cầu người dùng;
không tạo checkout khác. Chỉ dùng intake cho nguồn chưa nhận; sổ chính vẫn
là metadata và data_sources. Nếu quyết định nhận mẫu dev cần đổi sau review,
có thể chuyển trạng thái metadata mà không sửa snapshot lịch sử.

Kiểm chứng: `python -m unittest discover -s tests -v` — 21/21 pass.
Metadata HDLD001–007 giữ nguyên; bản sao raw HDLD008/009 khớp byte với nguồn
intake; Git bỏ qua cả bốn file nội dung mới. Clause CSV lịch sử không có diff;
khi so Git blob với checkout Windows cần xét CRLF/LF trước khi kết luận hash.

## Dọn và tích hợp file — 19/10/2026

- Đối chiếu byte/hash, chuyển 2 bản tải LTV Law/LegalZone trùng HDLD008/009
  vào Recycle Bin; giữ nguyên raw. Manifest cập nhật sang đường dẫn raw và
  trạng thái/nhóm khớp metadata. KTBK chưa nhận nên trả nhóm về unknown,
  tránh nhầm tên SIM_F đã dùng cho HDLD008.
- Chuyển DOCX Thiện Tín hỏng và 2 ảnh contact-sheet sinh từ PDF vào Recycle
  Bin. Giữ URL/hash/dung lượng cũ trong receipt; row bị loại có local_path
  rỗng và REMOVED_INVALID_DOCX. PDF nguồn vẫn ở restricted.
- Xóa 23 file cache .pyc có thể sinh lại. Tổng 28 file được dọn,
  2.731.273 byte; 5 file nội dung có thể khôi phục từ Recycle Bin.
- Tích hợp hướng dẫn backend/server vào backend/README.md vốn đang rỗng;
  migrations/README chỉ giữ hướng dẫn migration. Sửa code fence hỏng và cập
  nhật quy trình Git/dataset/test trong CONTRIBUTING.md. Gộp các đoạn mô tả
  nguồn bị lặp; metadata và data_sources vẫn là sổ chính.
- Giữ các clauses_v01–v06, taxonomy v01–v03, splits v05/v06, báo cáo lịch sử,
  bản nguồn và Python package/stub. File rỗng không tự động là file dư.

Codex Security đã hoàn thành scan snapshot 402e662, ID
dfd7a2f3-9a19-411f-af87-dda5006f50d6: một CWE-400 mức medium tại backend
upload. Báo cáo gốc do plugin quản lý; xem đường dẫn báo cáo trong chat.
Đợt dọn file không sửa API hay tuyên bố đã khắc phục phát hiện này.

Kiểm tra sau dọn: 21/21 unittest pass; 9 nguồn còn lưu khớp hash/dung lượng,
1 receipt ghi rõ đã bỏ binary; mappings HDLD008/009 khớp metadata; không còn
cache .pyc/contact-sheet; raw và snapshots/splits lịch sử không có diff.
