# Kiểm kê D1 cho kế hoạch mới — 19/10/2026

Đối chiếu kế hoạch W1/W2 trong PROGRESS.md của repo nhóm với dữ liệu đang
có trong repo ổ D. Đây là kiểm kê nguồn và kiểm tra PII sơ bộ, chưa phải
nghiệm thu gold hoặc quyết định thay D1 của BRD.

## Dữ liệu hiện có

- D1 baseline 4 hợp đồng/183 annotation trong BRD tương ứng HDLD001–004:
  39 + 40 + 61 + 43 clause. SIM_A chứa 001/002; SIM_B chứa 003; SIM_C chứa 004.
- Snapshot v06 có thêm HDLD005/SIM_D với 51 clause, tổng 234 clause/5 hợp đồng.
  Nhóm cần chốt có mở rộng D1 sang HDLD005 không. Không tự đổi BRD hoặc split.
- HDLD006: HOLD_NEAR_DUPLICATE với 005; HDLD007–009: TO_ANNOTATE.
  Chưa dùng các file này làm gold D1/T1.
- Chưa có gold segmentation theo canonical partition hoặc gold privacy
  theo thiết kế mới. Annotation nhãn clause hiện có không tự thay thế hai gold đó.

## PII sơ bộ trên raw text

Đã kiểm cả 9 bản text: không thấy chuỗi số liền 9–12 chữ số hoặc email;
tất cả dùng LF và không có newline cuối. Đây chỉ là kiểm tra định dạng,
không chứng minh đã ẩn danh: tên, địa chỉ, số có khoảng trắng/chữ ký/ảnh
và nội dung trong hình của DOC/DOCX vẫn cần người rà soát từ nguồn gốc.

Số code point từng bản: HDLD001 7.214; 002 6.823; 003 9.004; 004 10.991;
005 14.402; 006 13.095; 007 5.871; 008 2.978; 009 13.669.

Các PDF mới ở hàng chờ có PII nhìn thấy khi kiểm scan; chưa nhập raw,
chưa có canonical text đáng tin cậy, chưa đưa vào D1 hoặc T1.

## Việc tiếp theo và phụ thuộc

1. Data Lead và nhóm xác nhận danh sách D1 (4 hay 5 hợp đồng).
2. Rà soát nguồn gốc từng hợp đồng; bổ sung URL gốc HDLD001–003 còn thiếu.
3. Hai người kiểm source/PII và lập gold privacy; ghi reviewer, ngày, quyết định.
4. Trước MS-1 25/10: chốt guideline, chính sách đa nhãn cùng Clause/Risk Leads.
5. Sau khi canonical schema được chốt, tạo gold segmentation sửa tay và adapter
   nhãn; 9 CONTEXT không được chuyển thành exact-span gold.

Chưa tick hoàn thành W1 D1 privacy audit vì chưa có review thủ công đầy đủ.
Không suy ra nhãn rủi ro pháp lý từ taxonomy hoặc tên website công bố mẫu.
