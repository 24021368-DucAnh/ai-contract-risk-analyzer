# Phương pháp dữ liệu và đánh giá của N2

Phiên bản giải thích: 25/11/2026. Phạm vi là hồ sơ kỹ thuật/nghiên cứu đang có, chưa phải nghiệm thu hệ thống cuối.

## 1. Vai trò và luồng dữ liệu

N2 quản lý nguồn luật, corpus, Data Graph/retrieval, dữ liệu tham chiếu và harness đánh giá.
N1 phụ trách Clause AI/provider và Clause Graph; N3 phụ trách Risk, privacy, taxonomy và căn cứ pháp lý;
N4 phụ trách backend/tích hợp/cấu hình/host; N5 phụ trách frontend và đầu mối intake/ẩn danh X-10 được chuyển giao.
Phân công kỹ thuật này không thay cho quyết định pháp lý hoặc bằng chứng quyền dùng dữ liệu.

Luồng thực hiện là: tiếp nhận nguồn và quyền dùng → giữ bản gốc/băm nguồn → chuẩn hóa Unicode
và ghim toàn văn → tách điều khoản với offset trên đúng bản chuẩn hóa → ghi nhãn và hồ sơ duyệt
→ tạo bộ Dev theo lineage → đánh giá từng thành phần → kiểm tra phối hợp toàn hệ thống → khóa cấu hình
→ đánh giá held-out theo protocol riêng.

Offset dùng chỉ số ký tự Unicode của Python, dạng nửa mở `[start_char, end_char)`.
Không ghép offset lấy từ bản raw hoặc từ byte UTF-8 vào một văn bản đã chuẩn hóa khác.
Mỗi tệp nguồn, Gold, cấu hình và kết quả được ghim bằng SHA-256 để biết phép đo thực sự dùng phiên bản nào.

## 2. Nguồn luật và phạm vi corpus

Nguồn ưu tiên là văn bản chính thức có số hiệu, bản đính kèm và thông tin thời điểm.
Ngày ban hành, ngày hiệu lực và ngày hợp nhất là các trường khác nhau. Hệ thống phải chọn quy định
phù hợp với ngày phân tích; một bản hợp nhất có thể chứa thay đổi chưa có hiệu lực tại ngày đang xét.

WP1 RC02 đã được chủ dự án cho dùng nội bộ theo cơ chế opt-in: 30 provisions, 21 mappings.
Đây không phải thay đổi runtime mặc định hoặc nghiệm thu toàn bộ pháp lý.
WP2 hiện là dự thảo 118 mục, 83 cặp mapping ứng viên và 17 cặp HOLD; thêm 7 khoản phụ thuộc đang ở ngoài phạm vi 118 mục.

N2 đã soát 118 mục và 7 mục phụ thuộc với 21 trang PDF Công báo, có băm nội dung và trang nguồn.
Lần rà soát do AI thực hiện theo ủy quyền, không được ghi thành chữ ký người đọc độc lập.
Nghiên cứu hiệu lực có ghi rõ phạm vi, đích sửa đổi đã kiểm và việc cần N3 kết luận.
Chi tiết nằm ở gói WP2 visual/effectivity ngày25/11, không tự biến bằng chứng đối chiếu thành quyết định nhận corpus.

Data Graph nối các căn cứ luật; Clause Graph nối các điều khoản trong hợp đồng. Hai loại graph phục vụ
hai đối tượng khác nhau. Bật Data Graph trong M8 không đồng nghĩa với bật Clause Graph trong M10.

## 3. D1, D2 và D3

D1 là nguồn phát sinh các biến thể D2; không được xem một biến thể là nguồn độc lập để chia train/test.
Manifest Dev hiện ghim 8 toàn văn D1/D2 thuộc 4 nhóm nguồn gốc. Nguồn, biến thể và nhãn có version riêng.

D2 Clause Gold hiện có 250 span/nhãn được chủ dự án duyệt. D2 Risk Gold canonical hiện có 30 injection,
60 quan sát theo hai vai trò. Hai con số này đo hai đối tượng khác nhau, không cộng thành số hợp đồng.
Canonical D1/D2 đang hỗ trợ 6/21 nhãn Risk theo taxonomy cũ; tính tương thích với taxonomy22 nhãn còn cần N3 chốt.
Không ép mỗi nhãn phải có mẫu dương để đạt tỷ lệ bao phủ.

D3 là 20 văn bản tổng hợp, mỗi văn bản có một cặp hai điều khoản: tổng20 cặp thuộc10 family,
gồm10 mâu thuẫn và10 đối chứng có thời gian không giao nhau. Chấm hai vai trò tạo40 quan sát cặp-vai trò,
không tạo thêm nguồn độc lập. D3 chỉ phục vụ Dev, không phải hợp đồng thực hoặc dữ liệu held-out.
Nhãn D3 hiện là tham chiếu do AI tự rà theo ủy quyền; chưa có human-item review hoặc review độc lập.
Tính nhất quán nội bộ không phải kết luận hợp pháp hoặc không còn rủi ro nào khác.

## 4. Đánh giá retrieval M8

Hồ sơ M8 đang được phân tích lại có protocol `m8_dev_2026-11-24_v3_owner_d2_gold`, ngày phân tích cố định
12/11/2026. Retriever trả tối đa8 kết quả, lấy3 seed; chỉ số M8 kiểm căn cứ Gold có nằm trong top5 hay không.
Vì vậy `final_k=8` không biến Recall@5 thành Recall@8. Một căn cứ hạng7 hoặc8 vẫn bị tính trượt tại top5.

M8 bằng số quan sát có căn cứ đúng trong top5 chia cho tổng số quan sát có căn cứ tham chiếu.
Hồ sơ này gồm14 quan sát D1 và60 quan sát D2, tổng74; có44 nhóm truy vấn/căn cứ và chỉ4 nhóm nguồn gốc.
Các bản sao theo vai trò ở D2 có tương quan. Bootstrap phải gom theo nguồn D1 gốc, không theo tên biến thể.
Chỉ4 nhóm nguồn là quá ít để suy rộng độ chính xác ngoài Dev hoặc diễn giải khoảng tin cậy như bằng chứng chắc chắn.

Primary dùng nhãn Clause do bộ dự đoán đóng băng tạo ra; bộ đó đã học trên D1 nên phép đo D1/D2 này là in-sample/derivative Dev.
Oracle thay nhãn dự đoán bằng nhãn Clause tham chiếu để chẩn đoán. Oracle không phải cấu hình triển khai
và không bảo đảm tốt hơn trên từng truy vấn; thay nhãn có thể đổi thứ hạng theo hướng xấu đi.

| Corpus trong báo cáo đã lưu | Primary graph off | Primary graph on | Oracle graph off | Oracle graph on |
|---|---:|---:|---:|---:|
| RC01 reference | 58/74 | 55/74 | 60/74 | 59/74 |
| Mapping candidate | 64/74 | 62/74 | 66/74 | 66/74 |

So sánh giữ nguyên nguồn, Gold, predictor, ngày phân tích và tham số graph/retrieval.
Mức tăng Primary là6 quan sát ở graph off và7 ở graph on, toàn bộ thuộc D1; D2 vẫn50/60 và48/60.
Kết quả này hỗ trợ việc mô tả thay đổi trên chính Dev đã đo, chưa chứng minh cải thiện tổng quát trên D2 hoặc dữ liệu mới.

Phân tích ngày25/11 chỉ tái tính từ báo cáo đã lưu, không chạy model mới, không tạo lại khoảng tin cậy,
không đổi Gold và không dùng Oracle để huấn luyện/tune Primary.
Nguồn Gold Risk của hồ sơ M8 được ghim trong `input_sha256` của chính báo cáo;
không tự gọi hồ sơ lịch sử này là phép đo mới trên Risk Gold canonical v02 hoặc taxonomy22.

## 5. Đánh giá Risk và mâu thuẫn M10

Risk cần phân biệt bỏ sót, báo sai, căn cứ không hợp lệ và nhãn ngoài phạm vi annotation.
Nếu Gold chỉ bao phủ một số nhãn, dự đoán nhãn khác phải báo riêng, không tự coi tất cả là false positive.
Chẩn đoán rule cố định hoặc fixture test không phải chất lượng của model chạy trên toàn văn.

M10 cần4 lần chạy thật: EMPLOYEE/EMPLOYER × graph off/on, giữ cùng model/prompt/corpus/taxonomy,
ngày phân tích và giới hạn calls/tokens. Chỉ thay cách dùng Clause Graph; danh tính văn bản, cặp và graph phải được ghim.
Đầu vào inference chỉ chứa document ID, toàn văn, băm, clauses và graph; loại nhãn, family, topic, pair ID và lý do tham chiếu.

Một cặp được phát hiện khi đầu ra có liên kết `related_clause_ids` giữa hai điều khoản theo metric đã đóng băng;
phép đo chính dùng `require_ambiguous=False`. Báo recall trên nhóm mâu thuẫn và tỷ lệ báo nhầm trên nhóm đối chứng,
tách theo vai trò/chế độ. Không dùng số link đúng để kết luận mọi rủi ro khác đều đã được phát hiện.
Thiếu hoặc lỗi một run/document thì ghi chưa hoàn chỉnh; NOT_RUN không được coi là dự đoán âm.
Khoảng tin cậy theo document hiện có không được gọi là khoảng tin cậy gom theo family.
M10 hiện vẫn NOT_MEASURED, vì chưa có đủ đầu ra thực tế và hồ sơ chạy được chấp nhận.

## 6. Khóa đánh giá và giới hạn công bố

T1/T2 giữ lại cho đánh giá cuối. Chỉ dùng Dev để phân tích/sửa; không xem lỗi held-out để chỉnh rule,
prompt, mapping hoặc tạo nhãn nhằm nâng điểm. Trước lần đánh giá cuối phải khóa model/prompt/corpus,
taxonomy/rubric, Gold và version code, rồi đăng ký protocol và quyền dùng nguồn tương ứng.

Test tự động xác minh công cụ, schema, băm và các điều kiện; CI xanh không thay review pháp lý,
quyền dùng hợp đồng, chất lượng dự đoán hoặc kiểm chứng host đầy đủ.
N2 đang chờ N1/N3 cung cấp cấu hình và đầu ra Dev; N3 chốt mapping/rubric; N4 kiểm tra tích hợp và mở PR Pipeline thật;
N5 bàn giao intake/quyền dùng/ẩn danh. Chưa tuyên bố hoàn thành toàn bộ Data Lead hoặc release.
