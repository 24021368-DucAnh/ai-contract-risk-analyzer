# Sàng lọc nguồn hợp đồng đã ký còn nằm trong manifest — 28/10/2026

**Phạm vi:** tiếp tục Task 2 của kế hoạch Superpowers để tìm **10 hợp đồng T1 độc lập về khuôn/mẫu và 20 hợp đồng đã ký bổ sung khác nhau**. Bảng 'data/intake/additional_signed_lead_triage_2026-10-28.csv' phân loại **10 PDF đang có sẵn trong manifest hiện hành**, ngoài 4 PDF đã tạo hàng chờ 10 hợp đồng riêng. Đây là 10 **hồ sơ nguồn**; một hồ sơ có thể chứa 0, 1 hoặc nhiều hợp đồng thực tế. Không cộng số hồ sơ, trang PDF hoặc nhận định từ tìm kiếm thành hợp đồng được chấp nhận.

## Kết quả rà soát metadata an toàn

- Tất cả 10 tệp PDF còn tồn tại trong 'data/intake/restricted/' và đọc được cấu trúc trang. Số trang lần lượt là **6, 8, 7, 37, 26, 34, 12, 44, 7, 4** (theo thứ tự bảng). Không trích xuất, in ra hoặc xuất bản thông tin cá nhân, hợp đồng, chữ ký hay ảnh trang.
- **3 hồ sơ ưu tiên cao từ VIMDA:** Pharmetech 2015 (dấu hiệu bản điền và phần giao kết, cần xét luật tại thời điểm ký), Hasukito 2024 (dấu hiệu giao kết trên scan), Cosvia 2025 (bản điền trên scan). Đây là mô tả từ QC/manifest trước đó; chưa xác minh lại chữ ký.
- **Hồ sơ bệnh viện Hải Phòng 2025:** lịch sử ghi ít nhất một hợp đồng ở trang 23–24 và khả năng có bản thứ hai phía sau. Chưa xác nhận ranh giới và việc đây là hai văn bản đã ký khác nhau; với hồ sơ bệnh viện 2023 phải so trùng nhóm khuôn trước khi xét T1.
- **5 nguồn ưu tiên vừa/thấp khác** cần xác nhận đúng loại văn bản, chủ thể ký, trang hợp đồng và độc lập mẫu. Riêng hồ sơ 44 trang chứa nhiều loại giấy tờ và phụ lục, không được tính từng trang/phụ lục như hợp đồng.
- Cả **10 nguồn** có 'verified_executed_units=0', nghĩa là **chưa có đơn vị hợp đồng nào được xác minh độc lập trong lượt sàng lọc này**, không khẳng định các PDF không chứa hợp đồng thật. Tất cả giữ 'HOLD'; không tạo hàng chờ unit dựa trên suy đoán.

## Tuyến xin xác minh nguồn

| Nhóm nguồn | Đầu mối công khai hiện hành | Phạm vi yêu cầu ban đầu |
| --- | --- | --- |
| 5 hồ sơ trên cổng VIMDA/Bộ Y tế | [Cổng hiện hành](https://vimda.moh.gov.vn/) của Cục Hạ tầng và Thiết bị y tế: **dmec@moh.gov.vn**, **02462732272**; [thông báo tên miền cũ](https://imda.moh.gov.vn/) xác nhận chuyển từ 01/04/2026, chạy song song đến 30/09/2026 | Hỏi hồ sơ do ai tải lên, đầu mối pháp nhân/người có thẩm quyền, điều kiện xin phép nghiên cứu. Cổng lưu trữ không chứng minh quyền cấp phép của người ký. |
| 4 hồ sơ công bố trên Sở Y tế Hải Phòng | [Cổng Sở Y tế Hải Phòng](https://soyte.haiphong.gov.vn/): **soyte@haiphong.gov.vn**, **0225.3738969** | Hỏi đơn vị đã nộp hồ sơ và đường liên hệ pháp lý/chủ quản phù hợp; xác nhận từng bản đã ký và điều kiện sử dụng chỉ sau khi được cấp quyền. |
| 1 PDF lưu trên CDN thành phố Hải Phòng | [Cổng Thông tin điện tử thành phố](https://haiphong.gov.vn/): **congthongtindientu@haiphong.gov.vn** | Tìm trang công bố gốc và đơn vị cung cấp tệp. Chỉ biết CDN lưu tệp, chưa xác định cơ quan phát hành hay chủ thể có quyền cấp phép. |

Nguồn số điện thoại/email: chân trang cổng cơ quan chính thức, tra cứu ngày 28/10/2026. Cổng thành phố Hải Phòng còn ghi yêu cầu có **văn bản cho phép khai thác** với việc phát hành lại thông tin từ cổng; điều này không phải giấy phép sử dụng hợp đồng riêng của các bên ký. **Chỉ nghiên cứu tuyến liên hệ; chưa gửi thư hay nhận thêm tài liệu.** Phải xác minh bên cấp quyền hợp pháp và cơ sở xử lý dữ liệu của các bên ký trước khi bất kỳ tệp có PII nào được dùng làm dataset.

Đã đưa đủ 10 candidate ID vào 'data/intake/source_holder_outreach_queue.csv' (cùng 4 hồ sơ đã xếp hàng từ trước). Các tuyến công khai, gồm tuyến CDN riêng, được đối chiếu theo từng ID trong 'data/intake/source_contact_routes_2026-10-28.csv'. Tất cả yêu cầu hiện vẫn 'NOT_SENT'; không có người xử lý được giao hoặc quyền nào được chấp thuận.

## Tiếp tục theo thứ tự

1. Giao một người thật phụ trách xin xác minh thẩm quyền bên nộp hồ sơ/doanh nghiệp và người thứ hai có khả năng kiểm độc lập. Bắt đầu bằng thông tin mô tả không có PII; giữ yêu cầu và chứng cứ trong khu vực hạn chế.
2. Sau khi có giấy phép và cơ sở hợp pháp, xác định số **hợp đồng riêng đã ký** trong từng PDF, ranh giới 1-based, scan/ảnh/chữ, thông tin trùng lặp theo mẫu và độc lập với D1/D2.
3. Tạo **bản dẫn xuất ẩn danh** riêng, kiểm tra ảnh/text/metadata/chữ ký và khóa cùng nhóm similarity vào một split. Ghi phê duyệt của người kiểm thứ hai và bằng chứng hash/quyền rồi mới xem xét 'ACCEPTED_T1' hoặc 'ACCEPTED_ADDITIONAL'.
4. Đối với gold pháp lý, kiểm từng mệnh đề và quy định tại **ngày ký/hiệu lực thực tế** qua văn bản quy phạm gốc; chỉ người có chuyên môn pháp lý đủ thẩm quyền mới phê duyệt. Các nguồn năm 2015/2023/2024/2025 không tự mặc định cùng phiên bản luật.

**Trạng thái nghiệm thu chung vẫn là 0/10 T1 và 0/20 hợp đồng bổ sung.** Các nguồn này đều có mặt trong 'manifest.csv'; **không tăng** tổng số 22 ứng viên của manifest, và không thay đổi trạng thái tiếp nhận. Xem thêm 'docs/CONTRACT_SOURCE_HOLDER_REQUEST_AND_REVIEW.md' và 'docs/SOURCE_HOLDER_CONTACT_RESEARCH_2026-10-28.md'.
