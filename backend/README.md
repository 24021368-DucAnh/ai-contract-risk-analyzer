# Backend local — snapshot nền

Backend hiện chạy FastAPI upload PDF -> PyMuPDF trích text -> SQLAlchemy lưu
PostgreSQL. Clause/Risk/Explanation AI là stub rỗng, chưa gọi trong upload.

## Chạy để phát triển trên máy

Từ thư mục backend/, cài môi trường riêng, tạo .env từ .env.example và đặt
DATABASE_URL cho database phát triển. Không commit .env.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --reload
```

Swagger: http://127.0.0.1:8000/docs . Migration: xem migrations/README;
kiểm đúng DATABASE_URL trước thay đổi database.

## Giới hạn đã kiểm ngày 19/10/2026

Codex Security xác nhận CWE-400 mức medium: upload đọc toàn bộ tệp, trích
toàn bộ trang đồng bộ trong async handler và lưu text mà chưa có ngân sách
byte/page/text/time/concurrency/storage. Chưa kiểm runtime hay triển khai.
Chỉ giữ phục vụ phát triển local, chưa mở cho input không tin cậy.
Scan ID: dfd7a2f3-9a19-411f-af87-dda5006f50d6; snapshot 402e662.

Đợt dọn file không sửa API. Cần giới hạn admission/parser/storage hoặc ngừng
dùng backend nền khi nhóm hoàn tất chuyển sang repo pipeline.
