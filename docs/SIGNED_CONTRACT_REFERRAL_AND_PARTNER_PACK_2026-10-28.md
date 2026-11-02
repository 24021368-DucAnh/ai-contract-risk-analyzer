# Gói xin giới thiệu nguồn và tuyển đối tác cấp hợp đồng đã ký — 28/10/2026

**Đích nghiệm thu:** 10 hợp đồng lao động thực tế từ **10 họ mẫu độc lập** cho T1; thêm **20 hợp đồng đã ký riêng biệt**, không trùng 10 T1. Dữ liệu tìm được, hợp đồng mẫu, phụ lục, scan chưa xác minh và hợp đồng chưa được phép xử lý đều **không được tính**. Kết quả hiện tại: **0/10 T1; 0/20 bổ sung**.

## Tuyến A — hỏi đúng đơn vị cấp quyền cho 14 nguồn đã giữ an toàn

`data/intake/source_referral_batches_2026-10-28.csv` gom **14 receipt đang HOLD** thành **5 đợt yêu cầu** theo tuyến liên hệ công khai, tránh gửi nhiều thư trùng nhau tới một cơ quan. Từng ứng viên và route đối chiếu qua `source_holder_outreach_queue.csv` và `source_contact_routes_2026-10-28.csv`. Năm đợt gồm: An Giang (1 nguồn), Quảng Ngãi (2), VIMDA/Bộ Y tế (6), Sở Y tế Hải Phòng (4), và Cổng thành phố Hải Phòng (1). Tất cả là **DRAFT_ONLY**; chưa có người phụ trách, thư gửi, bằng chứng cấp quyền hay người xác minh độc lập.

Đối với **cơ quan công bố**, chỉ yêu cầu **đường liên hệ của bên thực sự có thẩm quyền đối với hồ sơ** và điều kiện gửi đề nghị. Không đề nghị cơ quan gửi hợp đồng gốc hoặc tiết lộ thông tin người lao động. Người đăng tải hay cổng lưu trữ không mặc nhiên có quyền chấp thuận sử dụng hợp đồng của các bên ký.

**Thư đề nghị chuyển đúng đầu mối (bản để người phụ trách duyệt trước khi gửi):**

> Kính gửi bộ phận tiếp nhận thông tin,
>
> Nhóm sinh viên thực hiện nghiên cứu về đánh giá điều khoản hợp đồng lao động tiếng Việt. Nhóm đã nhận thấy trên cổng thông tin của đơn vị có một số hồ sơ công bố liên quan đến hợp đồng lao động. Những hồ sơ này **chưa được nghiệm thu làm dữ liệu huấn luyện hay đánh giá** vì cần xác minh nguồn gốc và quyền xử lý dữ liệu cá nhân.
>
> Mong quý đơn vị hướng dẫn cách liên hệ **đơn vị nộp hồ sơ, người sử dụng lao động hoặc bộ phận pháp lý thực sự có thẩm quyền** để nhóm tự xin phép nghiên cứu. Ở bước này nhóm chỉ cần thông tin liên hệ tổ chức và quy trình xin quyền; xin **không gửi bản hợp đồng có chữ ký, số định danh hoặc thông tin cá nhân** qua email thường. Nếu có giới hạn về việc sử dụng lại thông tin từ cổng, mong đơn vị chỉ rõ điều kiện và đầu mối xem xét.
>
> Xin cảm ơn và trân trọng.

Trước khi dùng thư: người phụ trách điền tên nhóm, đơn vị nhận, nguồn công khai phù hợp và kênh phản hồi chính thức. Không đưa URL liên kết tải PDF chứa chữ ký hay thông tin cá nhân vào thư đầu tiên; chỉ dùng mô tả hồ sơ ở cấp tổ chức/năm nếu đủ an toàn. **Không tự đổi** `request_status` sang `SENT` khi chưa thực sự gửi.

## Tuyến B — tìm 30 hợp đồng qua đối tác sẵn sàng đồng ý

Ưu tiên **người sử dụng lao động thực sự** hoặc bên ký/đại diện được ủy quyền có thể cấp phép hợp lệ, thay vì tìm thêm PDF có dữ liệu cá nhân công khai. Gửi lời mời đến các doanh nghiệp/đơn vị **khi có người phụ trách được giao và kênh liên hệ chính thức**, trước tiên hỏi khả năng tham gia, số **hợp đồng thực tế đã giao kết**, niên độ, lĩnh vực, các họ mẫu khác nhau và phạm vi quyền; tuyệt đối chưa yêu cầu bản gốc. Đặt mục tiêu vận động **trên 10 họ mẫu T1** để dự phòng loại trừ và đủ 20 bản ký bổ sung **khác đơn vị hợp đồng**. Nhiều bản ký từ một họ mẫu có thể góp phần vào 20 bản bổ sung sau duyệt, nhưng phải cùng nhóm similarity khi chia split.

**Lời mời cho đơn vị chủ động cấp nguồn (bản dự thảo, chưa gửi):**

> Nhóm sinh viên đang xây dựng bộ đánh giá nghiên cứu về hợp đồng lao động tiếng Việt. Nhóm cần các **hợp đồng đã ký thực tế**, ưu tiên những mẫu khác nhau theo doanh nghiệp và thời kỳ; nhóm không tiếp nhận biểu mẫu trống thay cho hợp đồng thực tế.
>
> Xin cho biết liệu đơn vị có thể xem xét **đóng góp hợp pháp** một số hợp đồng cho nghiên cứu trong phạm vi nội bộ hay không. Đề nghị trước mắt **chỉ phản hồi thông tin tổng quan không nhận dạng cá nhân**: khoảng số lượng, số họ mẫu khác nhau, năm ký, người/bộ phận có thẩm quyền giải quyết yêu cầu, giới hạn cho phép lưu trữ, ẩn danh và đánh giá. Nhóm sẽ cung cấp phiếu quyền và quy trình duyệt riêng, thỏa thuận phương thức giao nhận bảo mật, người truy cập, thời hạn lưu/xóa và người kiểm thứ hai trước khi yêu cầu bất kỳ tệp nào.
>
> Đơn vị và các bên ký có quyền từ chối; không yêu cầu gửi hợp đồng, chữ ký hay thông tin nhân viên qua thư đầu tiên.

## Cổng quyết định trước khi nhập một hợp đồng

1. **Pháp lý dữ liệu:** xác nhận bên cấp có thẩm quyền và cơ sở pháp lý cho mục đích xử lý/dẫn xuất/đánh giá; xác minh quyền của các bên ký, lưu bằng chứng vào `data/intake/restricted/`; quy định rõ phạm vi xử lý, truy cập, lưu/xóa và quyền sử dụng bản ẩn danh. Văn bản pháp luật để chuyên gia rà gồm [Luật 91/2025/QH15](https://vanban.chinhphu.vn/?classid=1&docid=214590&pageid=27160) và **[Nghị định 356/2025/NĐ-CP](https://vanban.chinhphu.vn/?classid=1&docid=216387&pageid=27160)**, cùng hiệu lực từ **01/01/2026** theo thông tin công bố chính thức. Đây là mốc tham chiếu để kiểm tra, chưa phải kết luận áp dụng cho từng hồ sơ. Chuyên gia phải xác định quy định chuyển tiếp, thời điểm xử lý và căn cứ áp dụng.
2. **Đơn vị hợp đồng:** người được phép đọc bản gốc đối chiếu hợp đồng đã ký, ranh giới trang, hash, trùng tài liệu, nhóm mẫu và tách T1/D1/D2; scan trích chữ phải so với hình. T1 yêu cầu độc lập về họ mẫu, không từng xuất hiện trong phát triển.
3. **Ẩn danh:** dẫn xuất riêng, kiểm ảnh, text layer/OCR, metadata, bảng, chữ ký/con dấu và định danh gián tiếp; giữ file gốc ngoài Git.
4. **Người thứ hai và pháp lý:** người kiểm độc lập có ngày/quyết định; người có chuyên môn pháp lý kiểm đúng văn bản, điều/khoản/điểm và thời điểm có hiệu lực. Phải kiểm theo ngày ký và thời kỳ thực hiện; không lấy năm của văn bản hợp nhất làm ngày có hiệu lực cho tất cả điều khoản.
5. **Nghiệm thu:** chỉ cập nhật `ACCEPTED_T1` hoặc `ACCEPTED_ADDITIONAL` khi `scripts/validate_intake_gate.py` và bằng chứng thủ công đều đạt. Script xác nhận cấu trúc, không thay chữ ký người duyệt.

**Ưu tiên ngay:** phân công một người liên hệ nguồn và một người duyệt độc lập; gửi yêu cầu giới thiệu đầu mối sau khi rà nội dung thư; song song tiếp cận đối tác có khả năng tự cấp quyền. Không có phép và không có người duyệt thì giữ toàn bộ nguồn `HOLD`. Các bản này chưa được gửi.

**Đối chiếu cấu trúc 28/10/2026:** 14/14 ứng viên trong queue xin quyền xuất hiện đúng một lần ở 5 batch; 14 cặp ứng viên/tuyến liên hệ khớp 17 route đã đăng ký. Tất cả batch còn `DRAFT_ONLY`; cả 14 yêu cầu và 17 route đều `NOT_SENT`/chưa xác minh quyền. Kết quả kiểm tra này chỉ xác nhận bảng định tuyến, không xác nhận chủ thể có quyền hay nội dung hợp đồng đã ký.
