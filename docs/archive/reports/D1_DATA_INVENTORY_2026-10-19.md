# Kiểm kê D1 cho kế hoạch mới — 19/10/2026

## Đối chiếu lại tại repo này ngày 28/10/2026

**Đính chính về snapshot hiện tại:** repo local có 13 file hợp đồng gốc
`HDLD001`–`HDLD013` và 13 bản raw text tương ứng. Phiên bản clauses mới
nhất tại máy là `data/processed/clauses_v07.csv`, hiện bị bỏ qua bởi
`.git/info/exclude`, nên không xuất hiện trong `git status`. V07 có **306
clause trên 8 hợp đồng**: HDLD001 39, HDLD002 40, HDLD003 61, HDLD004 43,
HDLD005 51, HDLD010 23, HDLD012 36, HDLD013 13. Trong đó 234 dòng
`REVIEWED`, 72 dòng `NEEDS_REVIEW`; 289 offset `EXACT`, 17 `CONTEXT`.
HDLD006–009 và HDLD011 có file local nhưng chưa có clause trong v07.
**13 file gốc không đồng nghĩa 13 hợp đồng đã annotate hoặc được nhận vào T1.**
Manifest intake vẫn có 22 candidate, tất cả `t1_eligible=no`.

Đoạn v06 bên dưới là snapshot lịch sử để đối chiếu BRD, không phải tình
trạng mới nhất của repo.

Đếm trực tiếp `data/processed/clauses_v06.csv` ở working tree hiện tại:
HDLD001 39, HDLD002 40, HDLD003 61, HDLD004 43, HDLD005 51.
**HDLD001–004 cộng đúng 183 clause trên 4 hợp đồng**, khớp số liệu D1
trong BRD §8.2. HDLD005 là phần bổ sung v06 ngoài D1 baseline; chưa có
quyết định thêm vào D1. Toàn bộ v06 có 234 row (225 `EXACT`, 9 `CONTEXT`),
và `provisional_v06.json` vẫn ghi `PROVISIONAL`. Kiểm kê số lượng không thay
thế kiểm tra PII, quyền sử dụng, hoặc gold ranh giới ký tự.

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

## Bổ sung kiểm kê và phạm vi D1 — 02/11/2026

- Giữ **D1 baseline = HDLD001–004**, đúng BRD §8.2: 4 hợp đồng, 183
  clause. Phân bổ v06 là 39 + 40 + 61 + 43. Không sửa BRD.
- HDLD005 có 51 clause trong v06, là dữ liệu bổ sung ngoài D1 baseline;
  không đưa vào D1 hoặc benchmark M1 cho tới khi có quyết định đổi phạm vi.
- Kiểm lại canonical text ở repo dữ liệu: HDLD001–004 lần lượt có 7.214,
  6.823, 9.004 và 10.991 code point; regex chỉ báo cáo số lượng, không lưu
  giá trị, với 0 email, 0 chuỗi 9–12 chữ số liên tiếp và 0 mẫu điện thoại.
- **Trạng thái privacy: chưa xác minh đã khử định danh.** Raw DOC/DOCX vẫn
  còn trong nguồn cục bộ; tên, địa chỉ, ảnh/chữ ký, metadata và định danh
  gián tiếp chưa được rà trực quan/độc lập. Kết quả regex bằng 0 không chứng
  minh không còn PII. Không nhận dữ liệu này làm gold privacy hoặc T1.

Đầu việc kiểm kê và chốt phạm vi vận hành được hoàn tất; privacy review,
quyền sử dụng, gold segmentation và gold privacy vẫn là các cổng riêng, còn
mở.
