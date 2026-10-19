# Kiểm tra nguồn hợp đồng bổ sung — 19/10/2026

Phạm vi: chỉ sàng lọc nguồn để xây dựng dữ liệu dự án. Tệp tải về nằm tại
`data/intake/private/` hoặc `data/intake/restricted/` trên máy của Data Lead;
hai thư mục này được Git ignore. `data/intake/manifest.csv` ghi URL trực tiếp,
dung lượng và SHA-256 từng bản gốc. Không thay đổi dataset v06, nhãn, split,
release candidate hoặc `data/raw/contracts/`.

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
