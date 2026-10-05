# Kiểm tra nguồn hợp đồng mới — 05/10/2026

Mục tiêu: bổ sung **hợp đồng lao động tiếng Việt**, có đủ điều khoản, truy vết
được file gốc, không có dữ liệu cá nhân đã điền và không gần trùng với nhóm
đã có. Mẫu hợp đồng chỉ là **đầu vào** để phân tích; ghi nhãn clause không chứng
minh tính hợp pháp hay độ chính xác của citation trong mẫu.

## Kết quả nhận dữ liệu

| ID | Nguồn | Quyết định | Bằng chứng QC |
|---|---|---|---|
| `HDLD007` | [HrOnline, mẫu HĐLĐ 2026](https://hronline.vn/mau-hop-dong-lao-dong-2026-chuan-bo-luat-lao-dong-tai-mien-phi-wordpdf) | **Nhận raw, chờ annotate** | Trang ghi rõ mẫu Word miễn phí để tải và dùng tham khảo. File DOCX mở được, 4 trang, 9 điều, các trường tên/CCCD/địa chỉ còn trống. Văn bản Việt; 5-gram containment tối đa với `HDLD001`–`HDLD006` là **0.092**, thấp hơn nhiều so với ngưỡng nghi ngờ near-duplicate 0.5. Gán `SIM_E`. |

File gốc: `data/raw/contracts/HDLD007.docx`.
URL file: https://docs.google.com/document/d/11B6vwNm9BiPURKvpxtySNNa6NAJawRi2/edit?usp=sharing

SHA-256 DOCX: `07fb706f647f7dec581fcd251751a1ece54c035a24c41c230fe129449f9b325a`

SHA-256 raw text: `1a3a6d57b3c22aed5d0fcefe7d3bed4bd1fbac3cbf11becd2d336e5ac1eeab33`

`HDLD007.txt` được trích bằng Microsoft Word ở chế độ chỉ đọc, cùng quy tắc
với 6 file trước. Chưa đưa HDLD007 vào `clauses_v06.csv` hoặc split đánh giá.
Các số liệu và trích dẫn luật trong mẫu cần được Legal Citation Validation
kiểm tra riêng; tên bài viết “chuẩn” không được coi là xác nhận pháp lý.
Trang cho tải/dùng mẫu miễn phí, nhưng chưa thấy điều khoản cho phép tái phân
phối file gốc trong một kho Git công khai. Trước khi push raw DOCX lên kho
công khai, cần xác nhận quyền đó hoặc chỉ công bố URL, hash và annotation
được phép chia sẻ. Bản này hiện chỉ lưu local theo yêu cầu người dùng.

## Ứng viên không nhận

| Nguồn | Quyết định | Lý do |
|---|---|---|
| [Phụ lục V Nghị định 145/2020/NĐ-CP](https://vbpl.vn/bolaodong/Pages/vbpq-toanvan.aspx?ItemID=152668&dvid=318) | Không nhận bản mới | Mẫu HĐLĐ giúp việc gia đình cùng template với `HDLD004` (`SIM_C`); thêm bản nữa sẽ tăng trùng lặp. Văn bản nền đã bị sửa đổi một phần, không dùng bản này để kết luận tình trạng hiệu lực của từng điều khoản. |
| [VAFT, ba mẫu HĐLĐ 2024](https://vaft.edu.vn/chi-tiet-tin/mau-hop-dong-lao-dong-2024-moi-nhat-173764.html) | Không nhận | Mẫu điền tên, ngày sinh, số CCCD và địa chỉ cá nhân; các mẫu trên cùng trang cũng gần cùng cấu trúc. Không đưa PII vào raw repo. |
| [CCCC, mẫu HĐLĐ song ngữ](https://cccc.org.vn/wp-content/uploads/2024/11/II.2-MAU-HOP-DONG-LAO-DONG-TEMPLATE-OF-LABOUR-CONTRACT.pdf) | Chưa nhận | Nội dung khá khác biệt và không có PII đã điền, nhưng tài liệu có watermark và website ghi bản quyền thuộc CCCC. Cần quyền tái phân phối trước khi thêm vào repo có thể đẩy lên GitHub. File kiểm tra tạm không thuộc dataset. |
| [Thế Giới Luật, mẫu 02](https://thegioiluat.vn/van-ban/hop-dong-lao-dong/) | Không nhận làm mẫu chính | Có một số nội dung biểu mẫu đáng nghi/lỗi thời (ví dụ nhánh “không xác định thời hạn” vẫn có ngày kết thúc); cần legal review riêng nếu muốn dùng làm case lỗi, không coi là mẫu hiện hành chuẩn. |
| [Bộ Tư pháp, mẫu HĐLĐ](https://htpldn.moj.gov.vn/Pages/chi-tiet-tin.aspx?ItemID=18&l=Phobienphapluatkinh) | Không nhận | Một số nội dung trùng sát mẫu `HDLD003`; lợi ích đa dạng thấp. |

## Cách so trùng

Với mỗi cặp văn bản, chuyển chữ về chữ thường, bỏ dấu câu, gom khoảng trắng,
lấy tập 5 từ liên tiếp. Điểm là số 5-gram chung chia cho kích thước tập nhỏ
hơn. Điểm `HDLD007` so với `HDLD001`–`HDLD006` lần lượt là
`0.048, 0.048, 0.054, 0.063, 0.092, 0.092`. Đây là kiểm tra template-level;
khi annotate vẫn phải kiểm tra exact/near-duplicate ở clause-level trước split.
