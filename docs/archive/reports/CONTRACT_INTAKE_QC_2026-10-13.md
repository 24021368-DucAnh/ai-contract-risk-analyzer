# Kiểm tra nguồn hợp đồng trên repo ổ D — 13/10/2026

Thư mục được người dùng chỉ định: `D:\DHCN\Nam3_Ky1\CVDKHMT\ai-contract-risk-analyzer\data\raw\contracts`.
Đã kiểm tra trước khi chép: `HDLD007.docx` **đã tồn tại** và có SHA-256
`07fb706f647f7dec581fcd251751a1ece54c035a24c41c230fe129449f9b325a`,
đúng hồ sơ QC ngày 05/10. Không ghi đè. Raw text hiện có cũng giữ nguyên,
SHA-256 `1a3a6d57b3c22aed5d0fcefe7d3bed4bd1fbac3cbf11becd2d336e5ac1eeab33`.

## File mới lưu cục bộ

| ID | Đường dẫn trong repo ổ D | QC và quyết định |
|---|---|---|
| `CAND-KTBK-2026` | `data/intake/private/KTBK_2026_bundle.docx` | [Trang nguồn](https://ketoanbachkhoa.vn/mau-hop-dong-lao-dong-2026/) cho tải [DOCX](https://docs.google.com/document/d/18-qsmS7hf8QGrMJE1PwIHYm-37QuEuwy/edit?usp=sharing). ZIP hợp lệ, không có macro; phần hợp đồng 15 điều, khoảng 3.507 từ, không thấy chuỗi số định danh 9–12 chữ số đã điền. Trùng cụm 5 từ tối đa 3,4% với HDLD001–006 và 3,6% với HDLD007. **Giữ intake:** tệp chứa thêm phụ lục, thỏa thuận bảo mật/đào tạo và thuyết minh; chưa phải một hợp đồng độc lập. Quyền tái phân phối chưa xác nhận. |
| `CAND-MOJ-2025` | `data/intake/private/MOJ_2025.doc` | [Nguồn Bộ Tư pháp](https://htpldn.moj.gov.vn/Pages/chi-tiet-tin.aspx?ItemID=18&l=Phobienphapluatkinh). Bản HTML có đoạn trùng liên tiếp 45 từ với HDLD003; hồ sơ QC cũ đã loại do giá trị đa dạng thấp. DOC không thuộc phạm vi upload PDF/DOCX của thiết kế mới. **Loại khỏi corpus**; lưu local để đối chiếu nguồn. |
| `CAND-HP-2026` | `data/intake/restricted/HaiPhong_2026_scan.pdf` | [PDF nguồn](https://cdn.haiphong.gov.vn/gov-hpg/1/tintuc/2026/3/7.hop-dong-lao-dong639099085621662284.pdf) gồm 4 trang, không trích được text. **Giữ hạn chế:** chưa OCR, chưa kiểm PII/trùng lặp và quyền tái sử dụng. |

URL tải, dung lượng và SHA-256 của từng tệp nằm trong
`data/intake/manifest.csv`. Các tệp private/restricted được Git ignore.
Không thay đổi `data/contracts_metadata.csv`, `clauses_v06.csv`, split
hay release. Mẫu công khai không được tự tính là T1 giữ kín và không tự
gán nhãn rủi ro pháp lý. Muốn dùng bộ KTBK để thử pipeline cần tách riêng
phần hợp đồng, giữ nguyên bản gốc, rồi kiểm tra cấu trúc tệp dẫn xuất.
