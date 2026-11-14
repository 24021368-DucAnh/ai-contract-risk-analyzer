# Data Lead Data integration review — 14/11/2026

> tôi fix xong hết mới merge lên 1 lần nên hơi boom tí

## Phạm vi

Nhánh này ghép công việc Data Lead đã commit đến `a824795` với `origin/main`
(`d9b393e`). Phần thay đổi gồm metadata nguồn, cổng T1 tương đương, hồ sơ
freeze, tiện ích xuất Gold M2 theo phạm vi kho luật đóng, kiểm thử và tài liệu.
Đây là metadata và công cụ; Gold restricted, văn bản hợp đồng và hồ sơ duyệt
riêng tư vẫn ở ngoài Git.

## Tích hợp và kiểm chứng

- Một xung đột tài liệu tại `docs/LEGAL_SOURCE_DISCOVERY_2026-11-02.md` đã được
  giải quyết bằng cách giữ phần ghi nhận nguồn Circular 10 hiện hành trên `main`.
- Kiểm thử cũ về HDLD007 được chỉnh để xác nhận trạng thái
  `TO_ANNOTATE`/`CANDIDATE_T1_NEEDS_REVIEW` thay vì giả định không có metadata.
  Sự hiện diện của metadata không phải xác nhận quyền chia sẻ văn bản hoặc duyệt Gold.
- Python `.venv`: `pytest -q` đạt 98 passed, 3 skipped.
- Python `.venv`: `ruff check .` đạt 0 lỗi; `git diff --check` sạch.
- Không lấy tệp dirty/untracked từ checkout gốc vào nhánh tích hợp.

## Quan hệ với các PR đang mở

PR #19 và #20 chứa các gói cũ thuộc cùng luồng công việc. Nhánh tích hợp này
được đề nghị review như bản thay thế hợp nhất; chưa đóng hoặc merge hai PR cũ.
Trước khi merge cần reviewer độc lập, CI xanh và kiểm tra lại diff/nhánh đích.
Không dùng bản candidate trong PR #20 làm Gold đã phân xử.
