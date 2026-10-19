# Contributing Guide

## 1. Git workflow

Làm trên nhánh riêng, commit, rồi gửi PR để review khi được phép. Không push
trực tiếp main, không force-push và không tự merge. Nhánh thường dùng:
`data/`, `ai/`, `backend/`, `frontend/`, `docs/`, `fix/`; nhánh trợ lý hiện tại
là `codex/contract-source-intake`.

Theo yêu cầu chủ repo, trợ lý chỉ làm trên thư mục local ở ổ D; phải hỏi trước
khi pull/fetch, push hoặc tạo/cập nhật PR. Local commit được giữ để review.

Trước khi sửa, xem thay đổi hiện có và giữ phần việc của người khác:

```powershell
git status --short --branch
git diff
```

Commit dùng `<type>: <description>`, ví dụ `data: register new contracts`.
Chỉ stage các đường dẫn thuộc task, review danh sách staged trước commit.
Mọi thay đổi vào main cần PR và ít nhất một người review; không merge khi
còn conflict. Ưu tiên squash khi nhóm đã duyệt.

## 2. Cấu trúc dữ liệu đang dùng

- `data/raw/contracts/HDLDxxx.doc[x]`: bản nguồn đã nhận, giữ nguyên nội dung.
- `data/processed/raw_text/HDLDxxx.txt`: text trích từ đúng bản nguồn; offset
  phụ thuộc bản text này, không ghi đè tùy tiện.
- `data/contracts_metadata.csv`: sổ HDLD/SRC/SIM và trạng thái annotation.
- `docs/data_sources.md`: nguồn tải và quy định truy vết.
- `data/processed/clauses_vXX.csv`: snapshot annotation; v06 có 234 clause/5
  hợp đồng. Giữ các version cũ để tái tạo và đối chiếu.
- `data/splits/`: split tạm theo nhóm tương tự, không random từng clause.
- `data/intake/`: receipt/hàng chờ; nếu nguồn đã nhận, manifest trỏ về raw,
  không lưu thêm bản trùng trong intake.
- `scripts/`, `tests/`, `preview/`: xử lý, kiểm thử và highlight.

Đọc `docs/dataset_schema.md`, `docs/annotation_guideline.md` và
`docs/clause_taxonomy_v03.md` trước annotate. Không đổi nhãn hoặc thêm gold
rủi ro pháp lý thiếu căn cứ/review. WEEK2/WEEK3 là snapshot lịch sử, không
phải bằng chứng nghiệm thu kế hoạch 8 tuần mới.

HDLD007–009 và text chỉ lưu local chờ quyền tái phân phối. Intake private/
restricted/ được Git ignore; ignore không thay ẩn danh hoặc quyền truy cập
hệ điều hành. JSON/HTML highlight chứa toàn bộ raw text, cần kiểm trước chia sẻ.

## 3. Kiểm tra trước bàn giao

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -B -m unittest discover -s tests -v
git diff --check
git diff --cached --name-only
```

Kiểm thêm hash, metadata, offsets và nhóm trùng khi thay dataset. Không chạy
lại `extract_raw_text.ps1` toàn bộ tùy tiện: script hiện ghi đè text dẫn xuất,
có thể làm lệch offsets lịch sử.

## 4. Backend local

Xem `backend/README.md` cho luồng đang chạy và cách chạy local;
`backend/migrations/README` chỉ dành cho migration. Đây là mã nền cũ, chưa
phải pipeline AI đầy đủ; đọc giới hạn bảo mật trước mở upload không tin cậy.

Không commit `.env`, API key, mật khẩu hay private key. Giữ `__init__.py`
và stub còn phục vụ cấu trúc package; cùng rỗng không có nghĩa được xóa.
