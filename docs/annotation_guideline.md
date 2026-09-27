Annotation Guideline v1.0
1. Mục đích
Tài liệu này quy định cách segment, chuẩn hóa tối thiểu, gán clause_type, review và QC dữ liệu hợp đồng lao động cho project AI Contract Risk Analyzer.
Guideline này phải được dùng thống nhất cho mọi contract mới từ HDLD005 trở đi và khi review lại dữ liệu cũ.
2. Đầu vào và đầu ra
Đầu vào
File hợp đồng gốc trong:
data/raw/contracts/
Đầu ra
Các clause đã annotate trong:
data/processed/clauses_vXX.csv
Schema clause chuẩn:
clause_id, contract_id, section_title, clause_text, clause_type, annotation_status, notes
3. Quy trình annotation chuẩn
1. Đọc toàn bộ file gốc trước khi tách clause.
2. Xác định phần hành chính cần bỏ.
3. Xác định cấu trúc Điều/Mục.
4. Segment nội dung thành các semantic clause.
5. Gán clause_type theo taxonomy hiện hành.
6. Ghi notes cho các case đặc biệt.
7. Review toàn bộ contract.
8. Chạy QC cấu trúc và duplicate.
9. Chỉ sau QC mới append vào dataset processed mới.
Không annotate từng dòng một cách máy móc trước khi hiểu cấu trúc toàn hợp đồng.
4. Quy tắc inclusion / exclusion
4.1. Nội dung được annotate
Annotate nội dung có ý nghĩa pháp lý/nghĩa vụ/quyền/lợi ích liên quan đến quan hệ lao động, ví dụ:
- công việc, vị trí, địa điểm;
- thời hạn hợp đồng;
- lương, phụ cấp, thưởng;
- thời giờ làm việc;
- nghỉ;
- bảo hiểm/an toàn;
- điều kiện làm việc;
- đào tạo;
- nghĩa vụ/kỷ luật;
- quyền/nghĩa vụ NSDLĐ;
- chấm dứt;
- điều khoản thi hành/sửa đổi.
4.2. Nội dung không annotate
Không đưa vào clause dataset:
- quốc hiệu, tiêu ngữ;
- tên biểu mẫu;
- phần căn cứ pháp lý/preamble nếu không tạo quyền/nghĩa vụ trực tiếp giữa các bên;
- tên, ngày sinh, CCCD, địa chỉ, điện thoại, email;
- thông tin tài khoản;
- chữ ký;
- tên người làm chứng;
- dòng chỉ chứa dấu chấm/chỗ trống;
- heading không có nội dung;
- hướng dẫn điền mẫu/footnote dành cho người soạn, nếu không phải nội dung hợp đồng.
5. Quy tắc segmentation
Rule S1 — Một clause = một ý nghĩa chính
Một sample nên mang một semantic topic chính.
Nếu một câu/bullet chứa nhiều topic độc lập và các topic thuộc các clause_type khác nhau, ưu tiên split.
Rule S2 — Không mặc định một Điều = một clause
Một Điều có thể tạo ra nhiều clauses, kể cả nhiều clause_type.
Rule S3 — Bullet độc lập có thể tách riêng
Ví dụ trong cùng Điều về tiền lương:
- mức lương;
- phụ cấp;
- hình thức trả lương;
- kỳ hạn trả lương;
có thể là các clauses độc lập dù cùng label COMPENSATION_BENEFITS.
Rule S4 — Clause sau split phải đứng độc lập
Không tạo fragment không đủ ngữ cảnh như:
- trang bị bảo hộ lao động;
- và có hiệu lực từ ngày...
Nếu split làm mất chủ ngữ/vị ngữ/ngữ cảnh chung, được phép lặp lại phần ngữ cảnh tối thiểu từ chính câu nguồn để sample có thể đứng độc lập.
Ví dụ:
Nguồn:
- Về bố trí chỗ ăn, ở; trang bị bảo hộ lao động; bồi thường thiệt hại theo thỏa thuận trong hợp đồng lao động: ...
Có thể tách thành:
- - Về bố trí chỗ ăn, ở theo thỏa thuận trong hợp đồng lao động: ...
- - Về trang bị bảo hộ lao động theo thỏa thuận trong hợp đồng lao động: ...
- - Về bồi thường thiệt hại theo thỏa thuận trong hợp đồng lao động: ...
Mọi trường hợp lặp ngữ cảnh phải ghi rõ trong notes.
Rule S5 — Không paraphrase
Không được tự viết lại ý nghĩa theo cách khác.
Chỉ cho phép:
- nối các dòng bị ngắt do formatting;
- chuẩn hóa xuống dòng thành một chuỗi;
- lặp ngữ cảnh tối thiểu khi split theo Rule S4.
Không được bổ sung nghĩa mới mà nguồn không có.
Rule S6 — Heading lưu ở section_title
Ví dụ:
- section_title = Điều 4
- nội dung bên dưới mới nằm trong clause_text.
6. Quy tắc gán label
Taxonomy hiện hành gồm 12 class:
- JOB_INFO
- CONTRACT_TERM
- COMPENSATION_BENEFITS
- WORKING_TIME
- LEAVE
- INSURANCE_SAFETY
- WORKING_CONDITIONS
- TRAINING
- EMPLOYEE_OBLIGATIONS_DISCIPLINE
- EMPLOYER_RIGHTS_OBLIGATIONS
- TERMINATION
- OTHER
Chi tiết định nghĩa xem docs/clause_taxonomy_v03.md.
7. Quy tắc cho các class dễ nhầm
7.1. WORKING_TIME vs LEAVE
WORKING_TIME:
- giờ làm;
- lịch làm/ca làm;
- làm thêm;
- thời gian nghỉ trong ngày/giữa ca.
LEAVE:
- nghỉ hàng tuần;
- nghỉ phép năm;
- nghỉ lễ/Tết;
- nghỉ bù;
- các loại ngày nghỉ khác.
7.2. WORKING_CONDITIONS vs INSURANCE_SAFETY
WORKING_CONDITIONS:
- công cụ;
- thiết bị;
- phương tiện;
- chỗ ăn/ở;
- điều kiện vật chất phục vụ công việc.
INSURANCE_SAFETY:
- BHXH/BHYT/BHTN;
- mức đóng bảo hiểm;
- an toàn/vệ sinh lao động;
- bảo hộ lao động;
- phòng ngừa rủi ro an toàn khi đây là topic chính.
7.3. COMPENSATION_BENEFITS vs EMPLOYER_RIGHTS_OBLIGATIONS
Dùng COMPENSATION_BENEFITS khi clause định nghĩa bản thân quyền lợi tài chính, ví dụ:
- mức lương;
- phụ cấp;
- thưởng;
- hình thức/kỳ hạn trả lương;
- chế độ nâng lương;
- trợ cấp/quyền lợi.
Dùng EMPLOYER_RIGHTS_OBLIGATIONS khi clause chủ yếu phát biểu nghĩa vụ của NSDLĐ phải thực hiện/đảm bảo/thanh toán các quyền lợi đã thỏa thuận.
7.4. EMPLOYER_RIGHTS_OBLIGATIONS vs TERMINATION
Dùng EMPLOYER_RIGHTS_OBLIGATIONS nếu chấm dứt chỉ là một phần trong danh sách quyền quản lý tổng quát.
Dùng TERMINATION khi trọng tâm trực tiếp là:
- căn cứ chấm dứt;
- quyền đơn phương chấm dứt;
- điều kiện;
- sa thải/chấm dứt;
- thời hạn báo trước;
- nghĩa vụ/quyền lợi phát sinh do chấm dứt.
7.5. Bồi thường thiệt hại
- NLĐ phải bồi thường/chịu trách nhiệm vật chất → EMPLOYEE_OBLIGATIONS_DISCIPLINE.
- NSDLĐ có quyền yêu cầu bồi thường → EMPLOYER_RIGHTS_OBLIGATIONS.
- NSDLĐ phải bồi thường cho NLĐ → EMPLOYER_RIGHTS_OBLIGATIONS.
- Quyền chung của NLĐ được bồi thường nhưng không có class chuyên biệt phù hợp → OTHER, đồng thời ghi notes.
8. Clause ID
Định dạng mặc định:
<contract_id>_C<3 chữ số>
Ví dụ:
HDLD005_C001
ID phải:
- unique toàn dataset;
- tăng theo thứ tự xuất hiện trong contract;
- không tái sử dụng ID đã xóa.
Nếu phải split một clause của dataset đã phát hành mà renumber gây ảnh hưởng lớn, có thể dùng hậu tố chữ cái như HDLD003_C018A.
9. Annotation status
Cho phép:
- REVIEWED
- NEEDS_REVIEW
REVIEWED
Chỉ dùng khi:
- segmentation rõ;
- label rõ theo taxonomy;
- text đã đối chiếu nguồn;
- không còn tranh luận đáng kể.
NEEDS_REVIEW
Dùng khi:
- clause có nhiều topic khó tách;
- ranh giới class chưa rõ;
- text nguồn bị lỗi/thiếu;
- cần đối chiếu thêm guideline/taxonomy.
Không được ép case chưa rõ thành REVIEWED chỉ để đạt 0 pending.
10. Quy tắc notes
notes để trống với case thông thường.
Bắt buộc ghi notes khi:
- lặp ngữ cảnh sau split;
- clause là hard case;
- label dựa trên rule phân biệt dễ nhầm;
- nguồn dẫn chiếu nội quy/tài liệu ngoài;
- source text có lỗi nhưng vẫn giữ nguyên;
- có nguy cơ risk/evaluation đặc biệt;
- quyết định annotation khác trực giác nhưng cần giữ consistency.
11. Duplicate và data leakage
11.1. Không tự động xóa duplicate
Exact duplicate/near-duplicate vẫn có thể có giá trị để phản ánh các mẫu hợp đồng thực tế.
Không xóa chỉ vì text giống nhau nếu chưa có quyết định dataset-level.
11.2. Bắt buộc dùng similarity_group
contracts_metadata.csv lưu similarity_group.
Ví dụ hiện tại:
- HDLD001, HDLD002 → SIM_A
- HDLD005, HDLD006 → SIM_D
11.3. Không split theo clause ngẫu nhiên
Khi tạo train/dev/test:
- không random toàn bộ clause rồi chia;
- phải group theo similarity_group;
- mọi contract trong cùng similarity_group phải nằm cùng một split.
Mục tiêu: tránh một câu/template xuất hiện ở train và gần như y hệt ở test, làm F1 bị inflate.
12. QC checklist trước khi merge dataset
Mỗi batch mới phải đạt:
- [ ] đúng schema 7 cột;
- [ ] không duplicate clause_id;
- [ ] không thiếu contract_id;
- [ ] không thiếu section_title;
- [ ] không có clause_text rỗng;
- [ ] clause_type nằm trong taxonomy;
- [ ] annotation_status hợp lệ;
- [ ] ID theo đúng thứ tự;
- [ ] clause đã đối chiếu file raw;
- [ ] multi-topic đã xử lý đúng;
- [ ] fragment đã được làm standalone nếu cần;
- [ ] notes đủ cho case đặc biệt;
- [ ] contracts_metadata.csv đã cập nhật;
- [ ] data_sources.md đã cập nhật nếu có source/contract mới;
- [ ] đã kiểm tra exact duplicate/near-duplicate;
- [ ] đã gán similarity_group.
13. Quy trình version
Không sửa ngược dataset version đã coi là archived.
Ví dụ:
- clauses_v01.csv → archived
- clauses_v02.csv → archived
- clauses_v03.csv → current
Khi append một batch contract mới đã QC xong, tạo version processed mới (v04, v05, ...), sau đó cập nhật metadata/docs tương ứng.