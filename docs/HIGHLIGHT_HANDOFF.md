# Bàn giao raw text và offset để highlight

## Dữ liệu cần dùng

- `data/processed/raw_text/<contract_id>.txt`: đúng văn bản UTF-8 đã dùng để tính offset.
- `data/processed/clauses_v06.csv`: 234 clause của `HDLD001`–`HDLD005`, mỗi row có
  `contract_id`, `clause_id`, `clause_text`, `start_offset`, `end_offset`,
  `offset_quality`. `HDLD006` giữ để kiểm tra near-duplicate; `HDLD007` có raw text
  nhưng chưa annotate.
- `start_offset` là vị trí đầu **bao gồm**, `end_offset` là vị trí cuối **không bao gồm**.
  Cả hai là chỉ số ký tự Python (Unicode code point), tính trên đúng file `.txt` này.

Ví dụ: `HDLD003_C018` bôi `raw_text[2453:2470]` = `các loại bảo hiểm`;
`HDLD003_C018A` bôi `raw_text[2472:2486]` = `các khoản thuế`. Hai annotation
được tách từ một bullet, nên `clause_text` của chúng có thêm ngữ cảnh chung.

## Quy tắc hiển thị

1. Hiển thị đúng nội dung `.txt`; đừng thay bằng text trích lại từ Word/PDF,
   trim, normalize khoảng trắng, hoặc đổi newline trước khi áp offset.
2. Bôi đoạn `[start_offset, end_offset)`; giữ `offset_quality` trong payload.
3. `EXACT` (225 row): đoạn bôi khớp `clause_text` sau chuẩn hóa khoảng trắng.
   Có thể dùng làm nhãn span chuẩn khi đánh giá.
4. `CONTEXT` (9 row): đoạn bôi là cụm từ gốc liên quan, không nhất thiết là
   toàn bộ `clause_text`. Có thể dùng để điều hướng và highlight; không dùng
   làm trích dẫn nguyên văn hoặc nhãn exact-span khi đánh giá.
5. Nếu hệ thống phân tích một hợp đồng mới và không tìm được span trong raw text,
   trả về `null`/cần review; không đoán offset.

Frontend JavaScript cần nhớ `.slice()` đếm UTF-16 code units, còn CSV đếm Unicode
code points. Để dùng đúng cả khi tài liệu tương lai có emoji, có thể tạo
`const chars = Array.from(rawText)` một lần, rồi lấy
`chars.slice(startOffset, endOffset).join("")`. Bảy raw text hiện tại không chứa
ký tự ngoài BMP, nhưng không nên dựa vào điều đó cho hợp đồng mới.

## Scripts và kiểm tra

- `scripts/extract_raw_text.ps1`: quy tắc trích text DOC/DOCX bằng Microsoft Word;
  xem `data/processed/raw_text/README.md` trước khi chạy lại vì offset phụ thuộc
  đúng snapshot `.txt`.
- `scripts/build_offsets.py`: tạo v04, chỉ nhận span khớp nội dung.
- `scripts/build_context_offsets.py`: tạo v05 và chọn cụm từ nguồn cho 9 case
  không khớp nguyên văn.
- `scripts/export_highlight_payload.py HDLD003`: xuất JSON ra stdout gồm raw text,
  61 clauses của HDLD003, offset, `offset_quality` và `highlight_text` đã kiểm tra.
  Có thể đổi ID thành HDLD001–HDLD005 và chuyển hướng stdout vào file `.json`.
  Script báo lỗi nếu span `EXACT` lệch khỏi raw text hoặc ID chưa được annotate.
- `python -m unittest discover -s tests -v`: kiểm tra offset, chất lượng span,
  khả năng tái tạo v05 và metadata. Trên máy này dùng Python bundled của Codex
  nếu lệnh `python` chưa có trên PATH.

Pipeline có thể đọc `clauses_v06.csv` và raw `.txt` qua data submodule hoặc
biến `CONTRACT_DATA_DIR`. `ai_pipeline/eval/fixtures/build_golden_v0_3.py` chỉ
xuất snapshot cũ 174 row `EXACT`; muốn đánh giá v06 cần cập nhật nguồn fixture.
UI muốn hiển thị cả 234 row cần đọc v06 trực tiếp và giữ `offset_quality`.
