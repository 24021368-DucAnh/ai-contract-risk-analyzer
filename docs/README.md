# Tài liệu Data Lead — bắt đầu ở đây

Điểm vào của tài liệu trong repo dữ liệu local. Cập nhật 19/10/2026.
Các báo cáo theo mốc nằm trong archive để không lẫn với hướng dẫn đang dùng.

## Đọc tài liệu nào?

- [data_sources.md](data_sources.md): nguồn hợp đồng, ID HDLD/SRC/SIM và trạng thái nhận dữ liệu.
- [dataset_schema.md](dataset_schema.md): cấu trúc thư mục, schema CSV, version và split.
- [annotation_guideline.md](annotation_guideline.md): quy tắc tách/gán nhãn, cần đọc trước annotate.
- [clause_taxonomy_v03.md](clause_taxonomy_v03.md): định nghĩa 12 nhãn đang dùng.
- [HIGHLIGHT_HANDOFF.md](HIGHLIGHT_HANDOFF.md): offset, EXACT/CONTEXT và bàn giao highlight.

Taxonomy v03 được giới thiệu với dataset v03 và tiếp tục dùng trong v06;
số phiên bản taxonomy không bắt buộc trùng phiên bản dataset. Không đọc câu
"snapshot hiện tại" trong tài liệu cũ như trạng thái mới của toàn repo.

## Trạng thái và việc đang làm

- Metadata là sổ trạng thái từng hợp đồng: 9 raw local; 5 hợp đồng đã annotate
  trong [clauses_v06.csv](../data/processed/clauses_v06.csv), tổng 234 clause,
  225 EXACT và 9 CONTEXT. HDLD006 hold near-duplicate; HDLD007–009 chờ annotate.
- [provisional_v06.json](../data/splits/provisional_v06.json) là split tạm;
  không phải benchmark giữ kín. Nội dung HDLD007–009 chỉ lưu local chờ quyền
  tái phân phối, dù metadata/nguồn vẫn được quản lý bằng Git.
- Theo kế hoạch 8 tuần mới của nhóm, 19/10 là đầu W2, MS-1 ngày 25/10.
  Các tên WEEK2/WEEK3 trong archive thuộc lịch cũ.
- Việc cần chốt: D1 gồm HDLD001–004 hay thêm HDLD005; review PII thủ công và
  nguồn HDLD001–003; guideline và chính sách đa nhãn cùng Clause/Risk Leads.
  Kiểm kê sơ bộ chưa thay cho nghiệm thu gold/privacy.
- T1 cần >=10 hợp đồng gốc độc lập có quyền dùng và đã ẩn danh. Các mẫu dev
  và PDF còn PII trong intake chưa được tính vào T1.

Kế hoạch/kiến trúc toàn nhóm nằm ở repo pipeline. Bản local này không tự
đồng bộ GitHub; không coi trạng thái báo cáo cũ là trạng thái nhánh remote.

## Lịch sử và bằng chứng

Các file dưới đây giữ nguyên nội dung snapshot. Quyết định hiện hành xem
metadata, data_sources và phần trạng thái ở trên.

- [Taxonomy v01](archive/taxonomy/clause_taxonomy_v01.md), [v02](archive/taxonomy/clause_taxonomy_v02.md): định nghĩa đã dùng cho dữ liệu cũ.
- [Bàn giao v05 / lịch tuần 2 cũ](archive/reports/WEEK2_DATA_HANDOFF.md).
- [Tiến độ v06 / lịch tuần 3 cũ](archive/reports/WEEK3_DATA_PROGRESS.md).
- QC nguồn ngày [05/10](archive/reports/CONTRACT_INTAKE_QC_2026-10-05.md), [13/10](archive/reports/CONTRACT_INTAKE_QC_2026-10-13.md), [19/10](archive/reports/CONTRACT_INTAKE_QC_2026-10-19.md).
- [Kiểm kê D1 ngày 19/10](archive/reports/D1_DATA_INVENTORY_2026-10-19.md).

## Quy tắc giữ cấu trúc gọn

Hướng dẫn hiện hành giữ một bản tại docs/. Báo cáo đóng theo ngày/mốc đặt
trong archive/reports/; taxonomy cũ đặt trong archive/taxonomy/. Cập nhật
trạng thái ngắn tại đây, không nhân bản guideline/schema vào từng báo cáo.

Giữ các clauses_v01–v06 và splits v05/v06 tại đường dẫn hiện có vì script/test
dùng để tái tạo lịch sử. data/raw/annotated/ là thư mục tùy chọn cho source
đánh dấu thủ công; không copy CSV processed vào đó. Không xóa raw chỉ vì
cùng họ mẫu: metadata phải thể hiện ANNOTATED/TO_ANNOTATE/HOLD/EXCLUDED.

Quy trình Git và kiểm thử: [CONTRIBUTING.md](../CONTRIBUTING.md).
