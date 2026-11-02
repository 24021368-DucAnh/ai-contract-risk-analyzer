# Bắt đầu tìm dữ liệu luật cho tuần 4 — 29/10/2026

Kế hoạch `PROGRESS.md` của repo nhóm ghi tuần 4 là **02–08/11/2026**.
Phần N2 cần kho luật tầng 1 bản đầu, gold nhãn D1 và Data Graph có cạnh
`REFERS_TO/GUIDES` đã kiểm chứng. Trạng thái corpus hiện tại ở repo nhóm vẫn
`DRAFT`; không dùng tài liệu dưới đây để kết luận rủi ro hợp đồng hoặc đo M8.

## Nguồn đã tìm và lưu

Receipt chi tiết (URL, SHA-256, byte, trang, tình trạng text layer) ở
`data/intake/legal_source_receipts_w4_2026-10-29.csv`. Ba PDF được lưu trong
`data/intake/restricted/legal_sources/`, ngoài Git:

1. **P0 — Bộ luật Lao động 45/2019/QH14:** bản gốc trên cổng Chính phủ,
   83 trang, 5.232.503 byte, SHA-256
   `a0c0fcc3b9e040bcdcab70191f0ab95952183be94a6f5bc6424e8d3e85697139`.
2. **P0 — VBHN 18/VBHN-VPQH ngày 12/02/2026:** bản hợp nhất để rà các lần
   sửa đổi, 86 trang, 38.999.953 byte, SHA-256
   `5a01a5b4b778b78c7bc9372e3a7270735bd98c28160604bff95db06bb3345a6f`.
3. **P1 — Nghị định 145/2020/NĐ-CP:** bản gốc trên cổng Chính phủ,
   122 trang, 6.176.759 byte, SHA-256
   `a72a1ff295cc06fbddd335d57257688f5118826968cd8b62d58f50fc1554b230`.

`pypdf` trích được **0 ký tự** từ cả ba PDF: đây là nguồn scan, cần OCR rồi
đối chiếu từng trang với ảnh gốc trước khi chia văn bản–điều–khoản–điểm.
Không lấy `effective_from` của văn bản gốc làm bằng chứng hiệu lực hiện tại
cho mọi điều khoản. Bản hợp nhất hỗ trợ tra cứu, không thay thế việc xác minh
văn bản sửa đổi và thời điểm áp dụng.
Kết quả tìm kiếm theo số Điều cũng trả về Bộ luật Lao động **10/2012/QH13**;
không lấy điều cùng số từ văn bản cũ để điền cho 45/2019/QH14. Mỗi node phải
khóa theo số hiệu văn bản và phiên bản nguồn trước khi trích.

**P1 — Thông tư 10/2020/TT-BLĐTBXH:** đã tìm trang toàn văn tại CSDL văn bản
pháp luật và PDF trên cổng Trung tâm Hỗ trợ phát triển Quan hệ lao động.
Lượt tải PDF từ máy này lỗi 404 ở đường dẫn VBPL và lỗi kết nối ở đường dẫn
Trung tâm; chưa có file local, hash hay số trang. Giữ trạng thái
`SOURCE_FOUND_DOWNLOAD_FAILED` cho tới khi tải được bản gốc và rà lịch sử
hiệu lực.

## Thứ tự xử lý dữ liệu

1. OCR thử một số trang của Bộ luật 45/2019 và VBHN 18/2026, kiểm độ chính
   xác dấu tiếng Việt, số Điều/khoản/điểm và thứ tự cột; không tự đổ OCR vào
   corpus đã duyệt.
2. Lập cây `document → article → clause → point` cho nhóm ưu tiên phục vụ
   label map: Điều 21 trước, sau đó các điều về loại/giao kết và chấm dứt
   hợp đồng. Mỗi node phải có trang nguồn, ID cha, văn bản gốc/bản sửa đổi,
   checksum và trạng thái review.
3. Chỉ tạo `REFERS_TO`/`GUIDES` khi cả hai đầu cạnh và căn cứ dẫn chiếu đã
   được reviewer xác minh; trước đó để ở queue gợi ý, không nạp graph thật.
4. Đồng bộ corpus sang repo pipeline bằng review riêng, chạy validator và
   checksum; chỉ đổi `release_status` sau sign-off N2/N3 và người kiểm pháp lý.

Nguồn luật có thể thu thập và kiểm cấu trúc bằng kỹ thuật; nguồn hợp đồng
đã ký cho T1 vẫn cần quyền xử lý, ẩn danh và nghiệm thu độc lập. Không lấy
PDF công khai có PII làm hợp đồng được nhận chỉ vì tải được.

## OCR và cây cấu trúc ứng viên — 31/10/2026

Đã chạy thử OCR tiếng Việt trên trang PDF 8–12 của bản gốc 45/2019 và bản
hợp nhất 18/2026 (10 trang). File ảnh và text OCR nằm trong thư mục
`data/intake/restricted/legal_sources/`, ngoài Git. Dùng Tesseract 5.4 với
model `vie` từ `tessdata_best`, SHA-256 model
`b6b49293d95d0b6dbd8780174627e82c75be957b6f4ed9862155540d6b00bb45`.
Trang 10 bản gốc, thử với RapidOCR mặc định, không nhận đúng tiêu đề Điều;
Tesseract `vie` nhận được 5 tiêu đề Điều 23–27 trên chính trang đó. Đây là
so sánh một trang, không phải phép đo độ chính xác toàn văn.

`data/intake/legal_structure_candidates_w4_2026-10-31.csv` ghi 77 node
ứng viên: 2 văn bản, 27 Điều, 18 khoản và 30 điểm. Khoản/điểm thuộc Điều
20–22 của hai bản. Ảnh trang 8–10 bản gốc và trang 9–11 bản hợp nhất đã
được đối chiếu trực quan để xác nhận **cấu trúc** ba Điều này.
Các Điều khác mới là tiêu đề do OCR gợi ý, trừ tiêu đề Điều 22 trên hai
trang đã xem và Điều 28 ở trang 11 bản gốc. OCR đã bỏ sót tiêu đề Điều 28;
node này được thêm sau khi xem ảnh trang. Mỗi node có ID cha, số trang PDF
và checksum của file nguồn.
`HEADING_VISUALLY_CHECKED`/`STRUCTURE_VISUALLY_CHECKED` chỉ xác nhận vị trí
và số thứ tự; mọi node vẫn là `PENDING_LEGAL_REVIEW`. Chưa chép text OCR vào
corpus, chưa xác minh từng chữ, hiệu lực, sửa đổi hoặc cạnh graph.

Kiểm chất lượng receipt ở cấp **một nguồn ứng viên mỗi dòng**: 4 nguồn, 3/4
PDF đã tải; 3/3 file có hash, byte và số trang khớp receipt; 0/3 có text
layer. TT10 còn thiếu file nguồn. Đây là mức sẵn sàng cho chuẩn bị OCR,
không đủ để đo Recall@5 hoặc suy luận rủi ro pháp lý. Việc tiếp theo là
đối chiếu OCR từng điều/khoản/điểm với ảnh, kiểm văn bản sửa đổi và thời điểm
áp dụng, rồi mới chuyển node sang corpus đã duyệt.

## Chép nháp Điều 21 theo node — 31/10/2026

`data/intake/legal_article21_transcription_candidates_w4_2026-10-31.csv`
chứa 32 dòng: mỗi nguồn có 1 tiêu đề Điều, 5 khoản và 10 điểm của khoản 1.
Text được sửa thủ công từ ảnh trang 9 (45/2019/QH14) và trang 10
(18/VBHN-VPQH), rồi liên kết với node trong cây ứng viên. Các lỗi OCR thấy
rõ gồm `Nội đung`, nhãn `9)`/`ï)` thay cho `e)`/`i)`, dấu `:` thay cho `;`
và một số chữ có dấu. Hai bản chép nháp hiện khớp nhau ở 16 segment sau khi
chuẩn hóa khoảng trắng; kết quả này chỉ áp dụng cho Điều 21 trên hai trang
đã xem, không xác nhận rằng điều không bị sửa đổi hay có hiệu lực ở mọi
thời điểm. Tất cả dòng giữ `PENDING_LEGAL_REVIEW`, chưa nhập corpus phục vụ
retrieval hoặc đánh giá rủi ro.

## Chép nháp Điều 20 theo node — 31/10/2026

`data/intake/legal_article20_transcription_candidates_w4_2026-10-31.csv`
chứa 16 dòng: mỗi nguồn có 1 tiêu đề Điều, 2 khoản và 5 điểm. Bản gốc
trải từ trang PDF 8 sang 9; bản hợp nhất nằm ở trang 9. OCR bản gốc làm
sai nhãn `a)` thành `8)`, sai dấu câu và bỏ chữ ở chỗ ngắt trang; bản chép
nháp đã đối chiếu ảnh hai trang. Hai bản nháp khớp ở 8 segment của Điều 20.
Các dẫn chiếu Điều 149, 151 và 177 ở điểm c khoản 2 chỉ là text nguồn;
chưa kiểm đích dẫn chiếu hoặc tạo cạnh `REFERS_TO`. Mọi dòng vẫn
`PENDING_LEGAL_REVIEW`.

## Mở rộng OCR và cây cấu trúc — 02/11/2026

Đã chạy OCR UTF-8 toàn văn cho hai PDF scan đã có trong restricted:

- Bộ luật Lao động 45/2019/QH14: 83/83 trang có nội dung OCR; hash nguồn
  khớp receipt. Sau khi siết nhận diện heading để bỏ dòng dẫn chiếu Điều,
  index có 993 node: 1 văn bản, 220 Điều, 551 khoản, 221 điểm; 15 Điều là
  placeholder cần tìm thủ công. Index cũ dùng regex rộng được giữ tên
  `_broad_heading_v1.csv`, không dùng làm review queue hiện hành.
- Nghị định 145/2020/NĐ-CP: 122/122 trang có nội dung OCR; hash nguồn
  khớp receipt. Index có 821 node: 1 văn bản, 115 Điều, 355 khoản, 350 điểm;
  8 Điều là placeholder cần tìm thủ công. Thông tin công bố của
  Chính phủ mô tả Nghị định gồm 11 chương, 115 Điều ([nguồn chính thức](https://vanban.chinhphu.vn/thong-cao-bao-chi-vbqppl-do-chinh-phu-thu-tuong-chinh-phu-ban-hanh/thong-cao-bao-chi-thang-12-nam-2020-10061095)).

Candidate SHA-256 lần lượt là
`879fd98f8aca581eec79e1139797089a6baf838f5d1bd341ea90de2455587f04` và
`b4995a0776aa46c2e22834fbfb671564b47612690737dfd7c28214302b1a9481`.
Nghị định 283/2026/NĐ-CP: 100/100 trang có nội dung OCR; index metadata có
1.046 node (1 văn bản, 68 Điều, 312 khoản, 665 điểm), với Điều 33 là
placeholder do heading chưa được OCR nhận diện. Candidate SHA-256 là
`ca401ddb6a846be08da5684a9e905c2bf71792c714b998049f75cba3c3b1fbb6`.
Số 68 Điều được đối chiếu với thông tin của cơ quan nhà nước địa phương
([nguồn](https://iamo.gialai.gov.vn/tin-tuc/tuyen-truyen-pho-bien-noi-dung-co-ban-cua-nghi-dinh-so-283-2026-nd-cp-cua-chinh-phu.html));
index cũ với regex heading rộng được giữ riêng dưới hậu tố
`_broad_heading_v1.csv`.

Receipts hiện ghi sáu OCR candidates tại
`data/intake/legal_ocr_candidate_receipts_2026-11-02.csv`. Các CSV index chỉ
nằm trong ignored `data/intake/restricted/legal_sources/`;
mọi node vẫn `PENDING_LEGAL_REVIEW`. Bao phủ trang và nhận diện đủ số Điều
không chứng minh OCR chính xác, lịch sử sửa đổi, hiệu lực, quyền sử dụng hay
đủ căn cứ để nhập corpus. Chưa tạo edge hoặc chép text vào corpus.

## Chép nháp Điều 22 theo node — 31/10/2026

`data/intake/legal_article22_transcription_candidates_w4_2026-10-31.csv`
chứa 6 dòng: tiêu đề và hai khoản cho mỗi nguồn. Khoản 2 kéo sang trang
PDF tiếp theo ở cả hai nguồn; ba đoạn văn được giữ chung trong một node
khoản 2. Ảnh trang 9–10 bản gốc và 10–11 bản hợp nhất đã được xem để sửa
lỗi OCR. Bản OCR chưa soát riêng vẫn ở
`data/intake/legal_article22_ocr_candidates_w4_2026-10-31.csv` để truy vết.
Text nháp chưa được người kiểm pháp lý duyệt và không đưa vào corpus phát hành.

## Cập nhật hiệu lực văn bản xử phạt — 02/11/2026

Tra cứu lại Cổng Chính phủ cho thấy Nghị định 283/2026/NĐ-CP được ban hành
15/07/2026, có hiệu lực 10/09/2026 và có PDF ký số đính kèm ([hồ sơ chính
thức](https://vanban.chinhphu.vn/?docid=218871&pageid=27160&typegroupid=4)).
Báo Điện tử Chính phủ ghi Nghị định 12/2022/NĐ-CP hết hiệu lực từ 10/09/2026
và dẫn quy định của Nghị định 283/2026 cho giai đoạn mới ([nguồn Chính phủ](https://baochinhphu.vn/lao-dong-nuoc-ngoai-duoc-tra-them-1-tien-luong-thay-bao-hiem-that-nghiep-10226101211144485.htm)).
Do đó 12/2022 được giữ như candidate lịch sử/chuyển tiếp, không phải nguồn
xử phạt hiện hành mặc định. PDF 283 đã được tải vào restricted intake, OCR
100/100 trang và lập metadata-only index với 1.046 node; Điều 33 còn cần dò.
Mọi provision/interval vẫn chờ đối chiếu điều khoản chuyển tiếp, amendment
map và người kiểm pháp lý. Corpus chưa thay đổi.

### Cập nhật 02/11 — VBHN 18/VBHN-VPQH 2026 OCR receipt

Tải lại tệp PDF 18/VBHN-VPQH qua liên kết đính kèm trên trang Cổng TTĐT Chính phủ; SHA-256 vẫn khớp source receipt đã có. Tạo lượt OCR page-marked mới 86/86 trang trong restricted storage (`VBHN_18_2026_ocr_candidate.txt`), SHA-256/byte count ghi tại `data/intake/legal_ocr_candidate_receipts_2026-11-02.csv`. Mục lục metadata nghiêm ngặt có 1.082 hàng (220 điều dự kiến, 610 khoản, 251 điểm; tiêu đề OCR chưa phát hiện: 76, 77, 78, 79, 166), receipt hash nằm ở `data/intake/legal_ocr_structure_index_receipts_2026-11-02.csv`. Đây chỉ là OCR/index ứng viên; không có nguyên văn trong receipt, không chứng minh cấu trúc hoặc hiệu lực, toàn bộ vẫn `PENDING_LEGAL_REVIEW`; không thay đổi `provisions.jsonl`, `edges.jsonl`, `label_map.yaml`, không tăng số mục checklist hoàn tất.
