# Nghiên cứu tuyến liên hệ nguồn hợp đồng — 2026-10-28

Mục tiêu: chuẩn bị xin phép xử lý 10 hợp đồng được QC lịch sử ghi nhận trong 4 hồ sơ PDF, để tiến tới **10 hợp đồng T1 độc lập về mẫu + 20 hợp đồng đã ký bổ sung khác nhau**. Đây là **thông tin liên hệ công khai**, **không phải** xác nhận thẩm quyền cấp phép hoặc chấp thuận xử lý dữ liệu cá nhân. Không liên hệ hoặc xin nhận tệp nhạy cảm nếu chưa có người chịu trách nhiệm và quy trình bảo mật; tất cả yêu cầu hiện **NOT_SENT**.

## Đầu mối tìm được từ các trang công khai

| Receipt | Tuyến xác minh ban đầu | Bằng chứng công khai | Điều còn cần xác nhận |
| --- | --- | --- | --- |
| `CAND-AG-HEALTH-2025` (7 hợp đồng chung một mẫu) | Văn phòng Sở Y tế An Giang, điện thoại chung **0297.3862023** | [Cổng Sở Y tế An Giang](https://syt.angiang.gov.vn/), chân trang ghi địa chỉ mới **01 Trần Hưng Đạo, phường Rạch Giá** | Ai là người sử dụng lao động và ai có quyền quyết định chia sẻ/xử lý ở từng hợp đồng? Không suy diễn từ cơ quan đăng tải. |
| `CAND-QN-GSP-2025` | Sở Y tế Quảng Ngãi: **syt@quangngai.gov.vn**; đơn vị có tên trong hồ sơ: **Công ty TNHH MTV Vắc xin FVC** | [Liên hệ Sở Y tế](https://syt.quangngai.gov.vn/lien-he); [PDF nguồn](https://syt.quangngai.gov.vn/upload/2006968/20250507/GSP-FVC_CN_Binh_Chanh_065cf.pdf) | Xác minh pháp nhân/người có thẩm quyền của FVC qua kênh chính thức trước; chưa có kênh FVC chính thức độc lập được xác nhận. |
| `CAND-QN-VIETMY-2025` | Sở Y tế Quảng Ngãi: **syt@quangngai.gov.vn**; phòng khám Việt Mỹ: **sales@phongkhamvietmy.com** (kênh chung) | [Liên hệ Sở Y tế](https://syt.quangngai.gov.vn/lien-he); [Liên hệ Việt Mỹ](https://phongkhamvietmy.com/contact/) | Kênh phòng khám chỉ để hỏi chuyển đến bộ phận pháp lý/nhân sự; chưa xác minh pháp nhân ký và quyền được sử dụng hợp đồng. |
| `CAND-MOH-LONGCHAU-2021` | Cục Hạ tầng và Thiết bị y tế / VIMDA: **dmec@moh.gov.vn**; tuyến nhân sự Long Châu **longchau.hr@fpt.com.vn** chỉ là đầu mối giả thuyết | [VIMDA - liên hệ nghiệp vụ](https://vimda.moh.gov.vn/); [Tuyển dụng FPT Long Châu - liên hệ](https://vieclam.nhathuoclongchau.com.vn/lien-he) | Cần xác định pháp nhân ký hợp đồng năm 2021 có thực sự thuộc FPT Long Châu và ai có thẩm quyền xử lý. Cơ quan lưu hồ sơ không tự cấp quyền của các bên ký. |

Chi tiết từng tuyến đã ghi trong `data/intake/source_contact_routes_2026-10-28.csv`; một receipt có thể có nhiều kênh. Bảng gồm bảy tuyến nghiên cứu ban đầu cho bốn nguồn ở trên và **10 tuyến bổ sung** cho các nguồn khác trong `docs/ADDITIONAL_SIGNED_LEAD_TRIAGE_2026-10-28.md`: năm VIMDA, bốn Sở Y tế Hải Phòng, một Cổng thông tin thành phố Hải Phòng dành riêng cho PDF trên CDN. Tổng cộng **17 tuyến cho 14 nguồn**; một cơ quan/email có thể lặp lại do đối chiếu theo ứng viên. Tất cả các tuyến ở trạng thái `holder_authority_status=UNVERIFIED`, `request_status=NOT_SENT`. Địa chỉ liên hệ Sở Y tế An Giang phải theo website **hiện hành** vì thông tin địa chỉ từ trang cũ trước thay đổi hành chính có thể lỗi thời. Không sử dụng số điện thoại cá nhân của cán bộ, danh tính người lao động, nội dung hợp đồng hoặc thông tin chữ ký trong bảng nghiên cứu này.

## Công việc tiếp theo cho người được phân công

1. Gắn người phụ trách thực cho từng receipt trong `source_holder_outreach_queue.csv`, xác minh bộ phận/pháp nhân có quyền xử lý của cả bên tuyển dụng lẫn người lao động, và lấy phép phù hợp trước khi tiếp nhận thêm tài liệu nhạy cảm. Chỉ sau khi **thực sự gửi** mới đổi trạng thái `NOT_SENT`, kèm chứng cứ riêng tư.
2. Xin xác nhận ban đầu **chỉ về số lượng, năm, ngành, loại mẫu, cơ sở pháp lý và quyền chia sẻ**, tuyệt đối chưa đề nghị đính kèm hợp đồng gốc vào thư thường. Sau đó thống nhất kênh giao nhận an toàn, giới hạn lưu trữ/xóa và phạm vi bản đã ẩn danh theo `docs/CONTRACT_SOURCE_HOLDER_REQUEST_AND_REVIEW.md`.
3. Đối chiếu từng hợp đồng có chữ ký, giới hạn trang, mối quan hệ cùng mẫu, quyền lưu/xử lý, ẩn danh các lớp ảnh/text/metadata và chữ ký; phải có người thứ hai độc lập kiểm tra. Mọi hồ sơ hiện tại tiếp tục `HOLD`.
4. Song song vận động ít nhất **6 họ mẫu mới độc lập** để đủ T1 trong kịch bản thuận lợi nhất và ít nhất **20 hợp đồng đã ký bổ sung**. Tất cả phải là thỏa thuận thực tế riêng, không dùng mẫu trống hay phụ lục để tăng số đếm. Kiểm điều luật/ngày hiệu lực chỉ sau khi chứng cứ nguồn và quyền được chấp nhận và có người có chuyên môn duyệt.

**Trạng thái kết quả:** chưa xác minh được ai có quyền cấp phép; 0/10 T1 và 0/20 bổ sung được chấp nhận. Nghiên cứu này chỉ giải quyết thiếu **tuyến tiếp cận công khai**, không tự chuyển trạng thái quyền hay đánh giá pháp lý.
