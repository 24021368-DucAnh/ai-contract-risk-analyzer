# N2 — phân tích lại lỗi M8 Dev ngày25/11/2026

Đã đối soát toàn bộ74 dòng xếp hạng của hai báo cáo đã lưu. Đây là phân tích lại bằng chứng lịch sử,
không phải chạy model mới hoặc nghiệm thu corpus/runtime. Không đọc T1/T2.

## Kết quả chính

| Đại lượng | RC01 reference | Mapping candidate |
|---|---:|---:|
| Primary graph off, đúng top5 | 58/74 (78,38%) | 64/74 (86,49%) |
| Primary graph on, đúng top5 | 55/74 (74,32%) | 62/74 (83,78%) |
| Oracle graph off | 60/74 | 66/74 |
| Oracle graph on | 59/74 | 66/74 |
| Trượt ở ít nhất một chế độ Primary | 19 lượt | 12 lượt |
| Nhóm truy vấn/căn cứ bị trượt | 13 | 6 |
| Graph cứu được / làm mất kết quả đúng | 0 / 3 lượt | 0 / 2 lượt |

Trong cùng74 quan sát, candidate tăng6 lượt ở graph off (+8,11 điểm phần trăm) và7 ở graph on (+9,46 điểm phần trăm),
không có lượt đang đúng của reference bị candidate làm trượt trong từng chế độ.
Tất cả lượt tăng thuộc D1; D2 không đổi (50/60 graph off,48/60 graph on).
Vì vậy không diễn giải mức tăng tổng thành cải thiện đã chứng minh trên D2 hoặc trên nguồn mới.

74 lượt không độc lập: có44 nhóm truy vấn/căn cứ thuộc4 nhóm nguồn gốc;
12 lượt lỗi của candidate gom thành6 nhóm, mỗi nhóm bị lặp theo hai vai trò D2.
Mức giảm khi bật graph ở candidate là2/74, tương ứng2,70 điểm phần trăm, xuất phát từ một nhóm truy vấn.

## Điểm dễ bỏ sót đã xử lý

Trường `primary_missed_cases` của báo cáo lịch sử chỉ chứa các lượt graph off trượt.
Candidate có10 lượt như vậy, nhưng còn2 lượt graph off đúng ở hạng5 rồi graph on đẩy xuống hạng7.
Phân tích chỉ đọc trường đó sẽ không thấy nhóm hồi quy này. Công cụ sidecar mới đọc toàn bộ
`dev_case_details` và lấy hợp của lỗi hai chế độ, giữ nguyên báo cáo gốc.
Metric vẫn là top5 dù pool có tối đa8 kết quả; không tính hạng7–8 là đúng.

## Bằng chứng và hướng xử lý cho6 nhóm lỗi

- Một nhóm: graph đổi hạng5 thành7. Đây là hồi quy thứ hạng quan sát được; cần kiểm tra admission,
  ứng viên được thêm và cách xếp hạng trước khi khẳng định nguyên nhân là graph expansion hay một trọng số cụ thể.
- Hai nhóm: nhãn dự đoán khác nhãn tham chiếu; đổi sang nhãn tham chiếu đưa căn cứ vào hạng2.
  Đây là ưu tiên rà Clause labels với N1/N3, không phải quyền dùng Gold trong inference.
- Một nhóm: nhãn dự đoán và nhãn tham chiếu cùng là EMPLOYER_RIGHTS_OBLIGATIONS nhưng căn cứ có trọng số mapping bằng0,
  vẫn ở hạng8 khi tắt graph và không có trong pool khi bật graph. N3 cần xét tính phù hợp pháp lý của mapping trước khi N2 thêm trọng số.
- Hai nhóm còn lại: thay nhãn vẫn không vào top5. Cần kiểm tra nguồn/căn cứ, truy vấn và admission/ranking sau khi mapping được chốt.

Tất cả12 lượt lỗi có trọng số mapping của căn cứ theo nhãn dự đoán bằng0 và không đi tới được căn cứ từ seed
theo cờ reachability đã lưu. Đây là quan sát, không đủ chứng minh một thay đổi mapping bất kỳ sẽ sửa được lỗi.
Không tự thêm cạnh hoặc mapping để đưa căn cứ Gold vào top5.

### Đã tái hiện cơ chế hồi quy của graph

Sau phần đối soát báo cáo, N2 chạy lại riêng một truy vấn bằng nhãn đã lưu, code retrieval đóng băng,
ngày12/11/2026 và ba tệp nội dung corpus có băm khớp RC02. Không gọi bộ dự đoán nhãn hoặc provider,
không ghi toàn văn/quote truy vấn vào kết quả và không sửa runtime.

Căn cứ mục tiêu có điểm baseline khoảng0,229298, ở hạng5 khi tắt graph. Khi bật graph, hai ứng viên
`BLLD2019:art14:cl2` và `BLLD2019:art20:cl1` nhận điểm xếp hạng graph lần lượt0,53 và khoảng0,293491,
đều cao hơn điểm của căn cứ mục tiêu. Sau3 seed cố định, hai ứng viên này đứng trước các backup,
làm căn cứ mục tiêu xuống hạng7. Không xảy ra fallback. Cả hai thứ hạng khớp báo cáo đã lưu.

Đây là bằng chứng thực thi của cơ chế chèn/xếp hạng, không phải bằng chứng rằng hai căn cứ graph vô giá trị
về pháp lý hoặc rằng thuật toán vi phạm đặc tả. Không có thay đổi trọng số, quy tắc bảo vệ top5 hay cạnh/mapping mới.
N2 đã hoàn tất chẩn đoán nhóm này; thay chính sách xếp hạng cần một thay đổi thiết kế được review và đánh giá Dev phù hợp.
Trace chỉ chứa IDs, băm và điểm trong `GRAPH_LOSS_REPLAY.json` của gói nội bộ.

Ở graph off, Oracle cứu4 lượt nhưng làm mất2 lượt Primary đang đúng, nên số tăng ròng chỉ2.
Ở graph on, Oracle cứu4 lượt và không làm mất lượt đang đúng. Oracle không phải cận trên bảo đảm cho từng truy vấn.

## Hành động sau đối soát

1. N2 đã lập backlog6 nhóm với case IDs, băm nguồn, hạng, flags và role phụ trách trong gói nội bộ.
2. N1/N3 rà nhóm nhãn Clause; N3 quyết định các mapping có căn cứ pháp lý. Không đổi Gold để hợp dự đoán.
3. N2 chỉ triển khai thay đổi retrieval sau khi có quyết định về phạm vi và mapping; đo lại trên Dev với version mới,
   giữ graph off/on song song và giữ nguyên protocol so sánh.
4. N4 tích hợp trên Pipeline qua PR thật và chạy kiểm chứng host. Data PR26 hiện vẫn là hồ sơ chuyển giao.

## Khả năng tái lập và giới hạn

Đã kiểm bằng nhau: `input_sha256`, predictor, Gold Clause D2, ngày phân tích, k/final_k/seed_k,
graph version, nguồn gốc và từng case/query/Gold giữa hai báo cáo. Chỉ đọc báo cáo cũ, không gọi provider.

Nguồn báo cáo:

- `rc01_reference.json`: SHA-256 `1bddbc2d80cb80a248bd3da7a647385bf130e42a5824430107d24e0c5e73ba13`.
- `owner_mapping_candidate.json`: SHA-256 `2c7249644fede6e45848f6f9528c1ab777f72d59bcc5baa34db694815d02e511`.

Công cụ phân tích mới đã đi qua10 test RED→GREEN, gồm lỗi hợp graph off/on, ngưỡng top5,
gom quan sát theo truy vấn/nguồn và từ chối hồ sơ không đủ hoặc sai metric.
Test dùng fixture tổng hợp để kiểm công cụ, không phải điểm model.
Kiểm tra băm666 tệp đóng băng cho thấy không đổi. Tự review của tác giả, chưa phải review độc lập.
Các kết quả in-sample trên4 nguồn không chứng minh độ chính xác pháp lý hoặc khả năng khái quát.
