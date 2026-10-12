# v06 RC1 — candidate để review

Đọc `docs/WEEK5_DATA_QC_REPORT.md` và `docs/WEEK5_AI_EVALUATION_HANDOFF.md`
trước khi dùng. Dataset 234 clause, 225 EXACT + 9 CONTEXT. Hard test gồm
20 ca có nguồn truy vết, chờ independent adjudication. Split vẫn provisional.

`manifest.json` ghi SHA-256 của các file nhận bàn giao. Các file text trong
receipt dùng LF trên mọi hệ điều hành nhờ `.gitattributes`. Không đổi newline
hoặc raw text trước khi kiểm hash/áp offset. Notebook và manifest được pin
bằng commit của PR; manifest không hash chính nó hoặc notebook tạo ra nó.

Từ root repo, kiểm file receipt bằng Python:

```python
import hashlib, json
from pathlib import Path
receipt = json.loads(Path('data/releases/v06-rc1/manifest.json').read_text(encoding='utf-8'))
for path, expected in receipt['files'].items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == expected, path
```

Chạy validator và tests theo hướng dẫn bàn giao. Hash sai nghĩa là đang dùng
file khác; đối chiếu commit/release trước khi chạy model. Không coi candidate
này là benchmark risk pháp lý đã xác nhận.
