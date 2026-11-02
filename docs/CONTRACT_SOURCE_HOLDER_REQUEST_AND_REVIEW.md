# Xin nguồn hợp đồng đã ký và duyệt độc lập

Mục tiêu: **10 HĐLĐ thực tế, độc lập về mẫu để kiểm thử kín T1** và **20 HĐLĐ đã ký bổ sung, khác nhau**. Văn bản này là phiếu yêu cầu/kiểm tra, **chưa phải giấy phép đã được ký** và không thay thế tư vấn pháp lý. Không đưa bản gốc chứa PII lên Git, issue hoặc chatbot.

`data/intake/source_holder_outreach_queue.csv` theo dõi **14 nguồn PDF**: bốn nguồn gốc có 10 đơn vị được báo cáo là đã ký trong QC lịch sử, cùng 10 PDF khác chờ xác minh tại `data/intake/additional_signed_lead_triage_2026-10-28.csv`. Tổng số nguồn không phải số hợp đồng đã ký được duyệt. Tất cả `NOT_SENT`: nhóm cần xác định đúng bên có thẩm quyền và căn cứ xử lý dữ liệu trước khi liên hệ hoặc tiếp nhận hồ sơ. Nhận được giấy phép vẫn cần kiểm tra quyền của các bên ký và người kiểm thứ hai. Chỉ cập nhật `request_sent_date` khi **người phụ trách thực sự đã gửi**; lưu bằng chứng có thông tin cá nhân trong `data/intake/restricted/` và không ghi đường dẫn công khai.

## Thư đề nghị gửi bên có thẩm quyền cấp nguồn

> Nhóm sinh viên đang phát triển hệ thống nghiên cứu đánh giá rủi ro điều khoản hợp đồng lao động tiếng Việt. Nhóm tìm hợp đồng lao động **đã được giao kết thực tế**; tài liệu phải được cấp theo đúng thẩm quyền và có căn cứ hợp pháp để nhóm lưu, xử lý, ẩn danh và sử dụng trong phạm vi nghiên cứu đã thống nhất.
>
> Trước khi chuyển file, vui lòng cho biết số lượng hợp đồng riêng biệt, loại/ngành/năm ký, độ đa dạng của mẫu, định dạng và phạm vi quyền có thể cấp. Xin chưa gửi file chứa dữ liệu cá nhân khi chưa thống nhất kênh bàn giao bảo mật, người truy cập và điều kiện lưu/xóa. Nhóm chỉ sử dụng bản dẫn xuất đã kiểm tra ẩn danh sau khi có người duyệt độc lập.

## Phiếu xác minh quyền sử dụng (điền cho mỗi nguồn/hồ sơ)

- Tên tổ chức/người cấp, vai trò và **căn cứ có thẩm quyền**: __________
- Căn cứ được chia sẻ dữ liệu của **các bên ký**, cùng bằng chứng: __________
- Số hợp đồng đã ký riêng biệt, khoảng trang, nhóm mẫu: __________
- Cho phép lưu bản gốc bảo mật để truy nguồn: Có / Không / Có điều kiện.
- Cho phép OCR, phân đoạn và tạo bản dẫn xuất ẩn danh: Có / Không / Có điều kiện.
- Cho phép nhóm chia sẻ **nội bộ** bản dẫn xuất: Có / Không / Có điều kiện.
- Cho phép dùng bản dẫn xuất trong bộ đánh giá nghiên cứu: Có / Không / Có điều kiện.
- Cho phép công bố công khai bản dẫn xuất: Có / Không / Có điều kiện (mặc định **không**).
- Giới hạn mục đích, thời gian lưu, xóa/hủy, phương thức bàn giao, người truy cập: __________
- Văn bản xác nhận/ngày/người ký và chứng cứ quyền của họ: __________

Phản hồi đồng ý của một bên cấp nguồn **chưa tự chứng minh** quyền quyết định dữ liệu cá nhân của người lao động; phải được người có chuyên môn kiểm tra căn cứ pháp luật áp dụng trước khi nhập dữ liệu.

## Duyệt từng hợp đồng, không đếm theo tệp PDF

`data/intake/manifest.csv` quản lý nguồn/tệp; `data/intake/contract_unit_review_queue.csv` quản lý từng hợp đồng có trang nguồn. `source_pages` dùng số trang PDF **1-based**. Mười hàng ban đầu lấy từ QC lịch sử: bảy hợp đồng An Giang (chung một nhóm mẫu), một Quảng Ngãi GSP, một Quảng Ngãi Việt Mỹ, một VIMDA Long Châu. `signed_check=QC_REPORTED_SIGNED` chỉ cho biết QC trước đây đã báo hợp đồng có chữ ký; vẫn phải tự kiểm lại. Toàn bộ đang `HOLD`.

Người xử lý phải lưu bản gốc và bằng chứng quyền vào thư mục riêng được Git ignore, ghi SHA-256, tạo bản **dẫn xuất riêng**; kiểm tất cả trang/scan/bảng/hình nhúng/header/footer/chữ ký/con dấu/định danh gián tiếp, rồi thử copy, search, OCR và metadata để chắc dữ liệu gốc không còn lộ. Ghi hash bản dẫn xuất vào queue. `rights_evidence_path` trỏ về bằng chứng cấp quyền tại vùng hạn chế; không commit giấy xác nhận chứa PII.

Người duyệt **thứ hai là người thực**, khác người xử lý; ghi mã người xử lý/người duyệt, ngày ISO và quyết định. Reviewer xác minh bản đã ký, quyền xử lý, tính nguyên vẹn/trang, ẩn danh, trùng mẫu và leakage. Một người không tự ký duyệt hai vai; AI không thay người duyệt. T1 còn phải độc lập về mẫu và không được xuất hiện trong D1/D2, prompt, few-shot hoặc nội dung phát triển hệ thống. Các bản cùng `similarity_group` phải thuộc một split.

Chỉ sau khi có người có chuyên môn rà luật đúng phiên bản và ngày hiệu lực, gắn căn cứ điều/khoản/điểm chính xác, mới xét gold về rủi ro pháp lý.

## Chạy kiểm tra hình thức trước khi ghi nhận đã đạt

```powershell
python -m pip install pypdf  # nếu môi trường chưa có thư viện đọc trang PDF
python scripts/validate_intake_gate.py
python -m unittest discover -s tests -p test_intake_gate.py -v
```

Script kiểm tra liên kết ứng viên, receipt/file/hash, quyền khai báo có chứng cứ, người duyệt và split trước khi đếm `ACCEPTED_T1`/`ACCEPTED_ADDITIONAL`. Script **không đọc hiểu nội dung giấy phép, không duyệt ẩn danh bằng mắt và không đưa ra kết luận pháp lý**. Kết quả chỉ đạt mục tiêu sau khi có 10 T1 độc lập và 20 hợp đồng khác đủ toàn bộ cổng.

Script còn chặn khoảng trang PDF vượt số trang thật, các hàng trong cùng PDF bị chồng trang, bản dẫn xuất trùng bản gốc và phiếu quyền để ở nơi không hạn chế truy cập. Bằng chứng cấp quyền phải lưu trong `data/intake/restricted/` hoặc `data/intake/private/` đã được Git ignore. Khi nhập các hàng mới, kiểm tra bảng `contract_unit_review_queue.csv` để tránh đếm lại cùng tài liệu.
