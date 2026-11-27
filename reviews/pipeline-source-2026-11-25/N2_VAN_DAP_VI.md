# N2 — bản giải thích và trả lời vấn đáp

Ngày 25/11/2026. Dùng cùng phương pháp và bằng chứng trong PR Data 26; đây là tài liệu chuẩn bị,
không phải xác nhận người học đã nắm kiến thức hoặc hệ thống đã được nghiệm thu.

## Bản giải thích ngắn

Phần N2 của nhóm quản lý nguồn luật, corpus và Data Graph/retrieval, dữ liệu tham chiếu cùng công cụ đánh giá.
Mục đích là bảo đảm kết quả truy xuất và phép đo có thể quay lại đúng nguồn, đúng phiên bản và đúng thời điểm.

Với hợp đồng, nhóm giữ nguồn và băm, chuẩn hóa Unicode, rồi tách điều khoản với offset trên đúng bản đã chuẩn hóa.
Nhãn chỉ được xuất thành dữ liệu tham chiếu theo hồ sơ duyệt tương ứng. Các bản D2 phát sinh từ D1 phải giữ lineage,
vì chúng có tương quan và không được coi là những hợp đồng độc lập khi chia tập hoặc tính độ chắc chắn.

Với luật, N2 giữ số hiệu, bản chính thức, nội dung và khoảng hiệu lực. Ngày hợp nhất không thay ngày hiệu lực.
Việc đối chiếu nguyên văn hoặc CI thành công không tự chứng minh một mapping luật phù hợp với mọi tình huống.
Những kết luận đó được chuyển N3 review trước khi nhận vào corpus sử dụng.

Đánh giá được tách theo thành phần. M8 đo căn cứ đúng có nằm trong top 5 retrieval hay không;
M10 đo phát hiện liên hệ mâu thuẫn giữa các điều khoản theo tham chiếu đã định nghĩa. Gold không được đưa vào đầu vào model.
Dev dùng để phân tích và sửa, T1/T2 giữ lại cho đánh giá cuối sau khi khóa cấu hình.

Kết quả hiện có cần trình bày đúng giới hạn: M8 đã có báo cáo Dev in-sample với 64/74 khi tắt graph,
62/74 khi bật graph trên corpus ứng viên; D2 chưa cải thiện so với reference. Một nhóm bị graph đẩy căn cứ từ hạng 5 xuống 7
đã được tái hiện bằng code và nguồn đóng băng. Đây là bằng chứng để review chính sách retrieval, chưa phải hiệu năng trên dữ liệu mới.
D3 đã có 20 cặp tổng hợp và được AI rà nội dung theo ủy quyền; M10 chưa đo do chưa có đủ đầu ra model thật.

## Câu hỏi và cách trả lời

### 1. N2 làm gì, khác N1 và N3 ở đâu?

N2 quản lý nguồn/dữ liệu tham chiếu, corpus luật, Data Graph/retrieval và harness đánh giá.
N1 phụ trách Clause AI/provider và Clause Graph. N3 phụ trách Risk, privacy, taxonomy và căn cứ pháp lý.
N4 tích hợp backend/host, N5 làm frontend và đầu mối intake/ẩn danh X-10.
Một người viết được công cụ không có nghĩa họ đã thay thế quyết định chuyên môn của các phần còn lại.

### 2. Vì sao không đưa cả bộ luật và hợp đồng vào model rồi hỏi?

Đưa toàn văn vào model chưa giải quyết được việc chọn đúng phiên bản, thời điểm, căn cứ và kiểm chứng câu trả lời.
Retrieval đưa các căn cứ có định danh và nguồn vào một quy trình có thể kiểm tra lại.
Nhóm vẫn phải đánh giá retrieval và model; kiến trúc này không tự bảo đảm kết luận đúng.

### 3. Vì sao cần chuẩn hóa trước khi tạo offset?

Cùng chữ tiếng Việt có thể có cách biểu diễn Unicode khác nhau. Nếu offset lấy trên một bản còn quote lấy trên bản khác,
vị trí và nội dung có thể không khớp. Nhóm ghim toàn văn chuẩn hóa bằng SHA-256 và dùng offset ký tự Unicode nửa mở.
Ví dụ `[10,20)` lấy ký tự từ 10 đến trước 20, không phải 10byte UTF-8.

### 4. Gold khác nhãn AI đề xuất thế nào?

Nhãn AI đề xuất là một ứng viên. Dữ liệu tham chiếu phải có phạm vi và hồ sơ quyết định, tác giả/reviewer thực tế,
nguồn và version để biết ai đã nhận nhãn nào trong điều kiện nào. Chủ dự án cho phép AI tự rà phải được ghi là AI tự rà,
không ghi thành một người đã trực tiếp annotation hoặc một lần review độc lập.

### 5. D2 có bao nhiêu mẫu?

Phải nói rõ đang đếm gì: D2 Clause Gold có 250 span/nhãn; Risk Gold canonical có 30 injection và 60 quan sát theo hai vai trò.
Đó không phải 310hợp đồng hoặc 60 nguồn độc lập. Manifest toàn văn D1/D2 hiện có 8 biến thể thuộc 4 nguồn gốc.

### 6. Vì sao không chia ngẫu nhiên mọi dòng dữ liệu?

Các dòng và biến thể cùng nguồn có thể chia sẻ nhiều nội dung. Nếu một phần xuất hiện ở train còn phần gần như giống ở test,
phép đo có thể được hưởng thông tin từ nguồn đã gặp. Nhóm giữ family/lineage và gom thống kê theo nguồn gốc;
không coi việc tăng số dòng là tăng số nguồn độc lập.

### 7. M8 đang đo Recall@5 hay Recall@8?

Recall@5. Retriever trả pool tối đa 8 kết quả và chọn 3 seed cho graph, nhưng một quan sát chỉ đúng khi căn cứ Gold ở hạng 1 đến 5.
Căn cứ ở hạng 7hoặc 8 vẫn bị tính trượt ở M8top 5.

### 8. M8 tăng từ 58/74 lên 64/74 có chứng minh corpus tốt hơn trên mọi dữ liệu không?

Không đủ để kết luận rộng như vậy. Đó là so sánh có kiểm soát trên chính Dev đã lưu, với nguồn/predictor/Gold/tham số giữ nguyên.
Mức tăng graph off là 6 lượt và graph on là 7 lượt, toàn bộ thuộc D1; D2 vẫn 50/60 và 48/60.
Model Clause đã học D1, các biến thể D2 có tương quan và chỉ có 4 nhóm nguồn gốc.
Vì vậy cần gọi đúng là chẩn đoán Dev in-sample, không phải kết quả held-out hoặc độ chính xác pháp lý của sản phẩm.

### 9. Vì sao bật graph lại giảm từ 64 xuống 62?

Hai lượt theo vai trò của một truy vấn bị tụt căn cứ đúng từ hạng 5 xuống 7. Replay giữ nguồn/code/corpus và nhãn đã lưu
cho thấy hai ứng viên graph nhận điểm lớn hơn rồi được chèn trước các backup. Điều này giải thích cơ chế tụt hạng quan sát được.
Nó chưa chứng minh mọi graph đều có hại; cũng chưa đủ để chọn trọng số mới chỉ nhằm sửa đúng một nhóm Dev.

### 10. Oracle có phải điểm trần của hệ thống không?

Không phải cận trên bảo đảm cho từng truy vấn. Oracle ở đây thay nhãn Clause dự đoán bằng nhãn tham chiếu để chẩn đoán.
Ở candidate graph off, nó cứu 4 lượt nhưng làm mất 2 lượt đang đúng, nên chỉ tăng ròng 2.
Nhãn thay đổi làm điểm và thứ hạng đổi; không được đưa Gold vào inference rồi gọi đó là chất lượng triển khai.

### 11. Vì sao 12 lỗi lại chỉ còn 6 nhóm?

Các quan sát D2 theo hai vai trò dùng lại cùng truy vấn/căn cứ.12 lượt lỗi gom thành 6 nhóm truy vấn/căn cứ,
không phải 12 lỗi độc lập. Toàn bộ 74 quan sát M8 có 44 nhóm truy vấn/căn cứ và 4 nguồn gốc.
Nhóm báo cả số lượt và cấu trúc tương quan để tránh phóng đại kích thước mẫu.

### 12. D3 là 20hay 40 mẫu?

D3 có 20 văn bản tổng hợp; mỗi văn bản có một cặp hai điều khoản, nên là 20 cặp thuộc 10 family.
Chấm cảEMPLOYEE và EMPLOYER tạo 40 quan sát cặp-vai trò; không tạo 40 nguồn độc lập.
Trong phiên bản hiện có có 10 cặp mâu thuẫn và 10đối chứng có thời gian không giao nhau.

### 13. D3 có chứng minh Clause Graph giúp hiểu mâu thuẫn hợp đồng thực không?

Chưa. D3 hiện dùng một khuôn rõ và hẹp: cùng đối tượng/nội dung, hai giá trị khác nhau;
nhóm mâu thuẫn có cùng kỳ, nhóm đối chứng được tách thời gian. Chỉ kiểm giao thời gian đã phân tách được nhãn của bộ này.
Bộ hiện tại có ích cho smoke test về thời gian và quy trình chấm; chưa đủ để chứng minh suy luận graph tổng quát.
Cần ghi hạn chế và đánh giá thật trước khi nêu lợi ích Clause Graph.

### 14. “Nhất quán” có nghĩa là hợp đồng hợp pháp không?

Không. Nhất quán chỉ mô tả hai điều khoản không mâu thuẫn theo phạm vi đã định.
Một cặp nhất quán vẫn có thể có rủi ro pháp lý khác. Rà D3 không thay kiểm lương, thời giờ làm việc,
quyền chấm dứt hoặc các điều kiện pháp lý thực tế.

### 15. Vì sao M10 vẫn chưa đo dù đã có nhãn?

Nhãn tham chiếu không phải dự đoán. M10 cần đầu ra thực tế đủ bốn chế độ vai trò×graph,
đúng nguồn và cùng cấu hình đã khóa, kèm hồ sơ thực thi. Thiếu run hoặc lỗi document phải ghi incomplete.
Fixture test của công cụ và sự đồng thuận giữa hai lần AI tự rà không phải điểm model.

### 16. Vì sao chưa bật corpus WP2?

WP2vẫn có quyết định mapping/phạm vi và hồ sơ chuyên môn chưa chốt. Việc đã so nguyên văn 118 mục,
ghi nguồn/hiệu lực và CI xanh không tự giải quyết hết tính phù hợp của 83mapping ứng viên hoặc 17HOLD.
Nhóm giữ draft và chỉ nhận dữ liệu theo quyết định được ghi nhận, không tăng số lượng bằng cách tự bỏ HOLD.

### 17. Test và CI xanh đã chứng minh những gì?

Chúng hỗ trợ xác minh các hành vi kỹ thuật có trong phạm vi kiểm: schema, băm, chuyển đổi, phép tính và các điều kiện từ chối.
Chúng không tự chứng minh quyền dùng hợp đồng, tính đầy đủ của luật, chất lượng model hoặc một review pháp lý đã diễn ra.
Nói rõ suite nào, commit nào và kết quả nào; không lấy kết quả lịch sử thay lần chạy hiện tại.

### 18. Còn thiếu gì để hoàn tất Data Lead?

N1/N3 cần bàn giao cấu hình và đầu ra Dev đóng băng; N3 chốt mapping/rubric/taxonomy;
N4 kiểm chứng host và mở PR Pipeline thực tế; N5 bàn giao intake/quyền dùng/ẩn danh/chống trùng.
N2 sau đó mới tiếp nhận quyết định được chấp nhận, cập nhật dữ liệu, chạy Dev cuối và khóa phiên bản.
T1/T2 giữ cho đánh giá cuối, M10 hiện chưa đo và chưa công bố release mới.

## Cách dùng tài liệu

Đối chiếu các số với báo cáo đã ghim thay vì học thuộc một con số tách khỏi protocol.
Khi bị hỏi phần chưa có bằng chứng, trả lời đúng trạng thái và đầu vào còn thiếu.
Tài liệu này đã được chuẩn bị; việc người trình bày hiểu và trả lời được vẫn cần chính người đó đọc/thực hành.
