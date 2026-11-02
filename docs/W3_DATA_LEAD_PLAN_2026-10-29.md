# Công việc Data Lead tuần 3 (26/10–01/11/2026)

Nguồn lịch: `PROGRESS.md` của repo nhóm, mục Tuần 3; phạm vi thực hiện tại
repo dữ liệu này. Tuần 3 tập trung tiền xử lý cục bộ trên D1. Mốc MS-1
25/10 còn mục danh mục kho luật tầng 1 và guideline cần nhóm chốt; không coi
bản nháp hoặc checklist này là phê duyệt thay nhóm.

## Thứ tự thực hiện

1. **D1 / X-04 — bắt đầu gold segmentation.** Giữ D1 baseline là
   HDLD001–004 (183 dòng); HDLD005 là phần bổ sung v06 cho tới khi nhóm đổi
   phạm vi. Adapter `scripts/build_d1_clause_candidates.py` đã xuất nhãn
   reviewed v06 sang `data/intake/private/d1_clause_label_candidates_v06.json`
   ngày 29/10. File chỉ chứa ID, nhãn, offset và nguồn phiên bản; 9 dòng
   `CONTEXT` có `span=null` và `source_reference_span` riêng. Hàng chờ
   `data/intake/private/d1_segmentation_review_queue_v06.csv` đã tạo đủ
   183 mục, xếp 9 mục `CONTEXT` trước; mọi mục đều chờ review thủ công.
   **Còn phải làm:**
   người gán nhãn sửa tay ranh giới theo canonical text, ghi người gán/người
   kiểm, giải quyết khác biệt và tạo `seg.json` có thể dùng cho M1.
2. **X-03 / C-12 — kho luật tầng 1.** Đối chiếu danh mục P0/P1 với văn bản
   chính thức, kiểm đúng cấu trúc văn bản–điều–khoản–điểm, hiệu lực theo
   thời gian, nguồn dẫn và quyền sử dụng. Chỉ đưa provision vào corpus đã duyệt
   sau khi có bằng chứng; bản DRAFT không dùng làm chuẩn pháp lý hoặc số đo M8.
   Phần này thuộc repo pipeline và cần đồng bộ có kiểm soát từ repo dữ liệu.
3. **QC v07 cục bộ.** Bộ `scripts.audit_preview_dataset` cho biết 234 dòng v06
   được giữ nguyên, 72 dòng mới đều `NEEDS_REVIEW`, 0 lỗi cấu trúc/offset và
   78 chướng ngại phát hành. HDLD010 chưa xác minh nguồn; HDLD012/013 liên
   kết được với candidate HOLD nhưng chưa đủ quyền dùng, ẩn danh và review.
   Giữ v07 ngoài release và T1.
4. **D1 privacy cùng N3.** Rà trực quan nguồn và lớp text, lập gold privacy
   cùng span cần giữ; đo recall theo nhóm và preserve rate sau khi có người
   kiểm độc lập. Kiểm regex đơn lẻ không hoàn tất mục này.
5. **Cổng tuần 3 của nhóm.** Chạy PDF → canonical → mask → segment cục bộ
   trên D1 và kiểm INV-01/02/03. Cổng này thuộc nhiều role; repo dữ liệu
   cung cấp D1, adapter và QC, không tự tuyên bố pipeline nhóm đã chạy.

## Tình trạng ngày 29/10

- Đã làm trong repo dữ liệu: kiểm kê D1/v07, QC v07, đối chiếu nguồn cục bộ,
  adapter nhãn D1 và file ứng viên private.
- Chưa nghiệm thu: gold segmentation M1, gold privacy, corpus luật tầng 1,
  72 dòng v07, 10 T1 và 20 hợp đồng bổ sung.
- Tiếp theo: người kiểm dữ liệu xử lý hàng chờ ranh giới D1, ưu tiên 9 mục
  `CONTEXT`; sau đó chốt guideline/đồng thuận nhãn với nhóm và tạo gold M1.
