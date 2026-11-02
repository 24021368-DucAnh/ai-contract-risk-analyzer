**Annotation Guideline v1.0**
#### Trạng thái và phiên bản taxonomy
Tài liệu này mô tả quy trình đang dùng cho dữ liệu lịch sử; phần policy đa nhãn và
các chủ đề còn tranh luận ở §14 chỉ là đề xuất chờ xác nhận, chưa phải freeze MS-1.
Taxonomy dữ liệu hiện hành là `clause_taxonomy_v03` với 12 nhãn. Dataset v06 lịch sử
ghi một nhãn mỗi dòng; không diễn giải ngược thành gold đa nhãn nếu chưa áp dụng
quy tắc chuyển đổi được nhóm phê duyệt. Nguồn đề xuất: `docs/CLAUSE_TAXONOMY_FREEZE.md`
trong pipeline, đối chiếu với `docs/clause_taxonomy_v03.md`.
#### 1. Mục đích
Tài liệu này quy định cách segment, chuẩn hóa tối thiểu, gán clause_type, review và QC dữ liệu hợp đồng lao động cho project AI Contract Risk Analyzer.
Guideline này phải được dùng thống nhất cho mọi contract mới từ HDLD005 trở đi và khi review lại dữ liệu cũ.
#### 2. Đầu vào và đầu ra
##### 2.1 Đầu vào
File hợp đồng gốc trong: **data/raw/contracts/**
##### 2.2 Đầu ra
Các clause đã annotate trong: **data/processed/clauses_vXX.csv**
Schema clause chuẩn:
clause_id, contract_id, section_title, clause_text, clause_type, annotation_status, notes
Từ snapshot v04, có thêm `start_offset,end_offset` ở cuối mỗi row. Chỉ điền
khi đoạn trong raw text khớp `clause_text` sau chuẩn hóa khoảng trắng; xem
`docs/dataset_schema.md`. Clause được tách hoặc lặp ngữ cảnh mà không có
đoạn nguồn liên tục phải để trống offset và ghi `OFFSET_UNVERIFIED`.
Snapshot v05 có thêm `offset_quality`: các row này dùng span `CONTEXT` của
cụm từ nguồn liên quan và ghi `OFFSET_CONTEXT`; chỉ `EXACT` dùng cho đánh giá
span chuẩn. Xem `docs/HIGHLIGHT_HANDOFF.md` khi đưa dữ liệu cho frontend.
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
**Không annotate từng dòng một cách máy móc trước khi hiểu cấu trúc toàn hợp đồng.**
#### 4. Quy tắc inclusion / exclusion
##### 4.1. Nội dung được annotate
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
##### 4.2. Nội dung không annotate
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
#### 5. Quy tắc segmentation
**Rule S1** — Một clause = một ý nghĩa chính
- Một sample nên mang một semantic topic chính.
- Nếu một câu/bullet chứa nhiều topic độc lập và các topic thuộc các clause_type khác nhau, ưu tiên split.

**Rule S2** — Không mặc định một Điều = một clause
- Một Điều có thể tạo ra nhiều clauses, kể cả nhiều clause_type.

**Rule S3** — Bullet độc lập có thể tách riêng
- _Ví dụ_ trong cùng Điều về tiền lương:
    - mức lương;
    - phụ cấp;
    - hình thức trả lương;
    - kỳ hạn trả lương;

có thể là các clauses độc lập dù cùng label COMPENSATION_BENEFITS.

**Rule S4** — Clause sau split phải đứng độc lập
- Không tạo fragment không đủ ngữ cảnh như:
    - trang bị bảo hộ lao động;
    - và có hiệu lực từ ngày...

- Nếu split làm mất chủ ngữ/vị ngữ/ngữ cảnh chung, được phép lặp lại phần ngữ cảnh tối thiểu từ chính câu nguồn để sample có thể đứng độc lập.

_Ví dụ_:
Nguồn:
- Về bố trí chỗ ăn, ở; trang bị bảo hộ lao động; bồi thường thiệt hại theo thỏa thuận trong hợp đồng lao động: ...

Có thể tách thành:
- Về bố trí chỗ ăn, ở theo thỏa thuận trong hợp đồng lao động: ...
- Về trang bị bảo hộ lao động theo thỏa thuận trong hợp đồng lao động: ...
- Về bồi thường thiệt hại theo thỏa thuận trong hợp đồng lao động: ...

Mọi trường hợp lặp ngữ cảnh phải ghi rõ trong notes.

**Rule S5** — Không paraphrase
- Không được tự viết lại ý nghĩa theo cách khác.

Chỉ cho phép:
- nối các dòng bị ngắt do formatting;
- chuẩn hóa xuống dòng thành một chuỗi;
- lặp ngữ cảnh tối thiểu khi split theo Rule S4.

Không được bổ sung nghĩa mới mà nguồn không có.

**Rule S6** — Heading lưu ở section_title
_Ví dụ_:
- section_title = Điều 4
- nội dung bên dưới mới nằm trong clause_text.
#### 6. Quy tắc gán label
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

Chi tiết định nghĩa xem [clause_taxonomy](clause_taxonomy_v03.md).
#### 7. Quy tắc cho các class dễ nhầm
##### 7.1. WORKING_TIME vs LEAVE
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

##### 7.2. WORKING_CONDITIONS vs INSURANCE_SAFETY
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
##### 7.3. COMPENSATION_BENEFITS vs EMPLOYER_RIGHTS_OBLIGATIONS
COMPENSATION_BENEFITS (khi clause định nghĩa bản thân quyền lợi tài chính), e.g:
- mức lương;
- phụ cấp;
- thưởng;
- hình thức/kỳ hạn trả lương;
- chế độ nâng lương;
- trợ cấp/quyền lợi.

EMPLOYER_RIGHTS_OBLIGATIONS (khi clause chủ yếu phát biểu nghĩa vụ của NSDLĐ phải thực hiện/đảm bảo/thanh toán các quyền lợi đã thỏa thuận)
##### 7.4. EMPLOYER_RIGHTS_OBLIGATIONS vs TERMINATION
Dùng EMPLOYER_RIGHTS_OBLIGATIONS nếu chấm dứt chỉ là một phần trong danh sách quyền quản lý tổng quát.
Dùng TERMINATION khi trọng tâm trực tiếp là:
- căn cứ chấm dứt;
- quyền đơn phương chấm dứt;
- điều kiện;
- sa thải/chấm dứt;
- thời hạn báo trước;
- nghĩa vụ/quyền lợi phát sinh do chấm dứt.

##### 7.5. Bồi thường thiệt hại
|Example Case|Class|
|-|-|
|NLĐ phải bồi thường/chịu trách nhiệm vật chất| EMPLOYEE_OBLIGATIONS_DISCIPLINE|
|NSDLĐ có quyền yêu cầu bồi thường|EMPLOYER_RIGHTS_OBLIGATIONS|
|NSDLĐ phải bồi thường cho NLĐ|EMPLOYER_RIGHTS_OBLIGATIONS|
|Quyền chung của NLĐ được bồi thường nhưng không có class chuyên biệt phù hợp|OTHER, đồng thời ghi notes|

#### 8. Clause ID
Định dạng mặc định: ```<contract_id>_C<3 chữ số>```
_Ví dụ_:
HDLD005_C001

ID phải:
- unique toàn dataset;
- tăng theo thứ tự xuất hiện trong contract;
- không tái sử dụng ID đã xóa.
Nếu phải split một clause của dataset đã phát hành mà renumber gây ảnh hưởng lớn, có thể dùng hậu tố chữ cái như HDLD003_C018A.
#### 9. Annotation status
Cho phép:
- REVIEWED
- NEEDS_REVIEW

REVIEWED khi:
- segmentation rõ;
- label rõ theo taxonomy;
- text đã đối chiếu nguồn;
- không còn tranh luận đáng kể.

NEEDS_REVIEW khi:
- clause có nhiều topic khó tách;
- ranh giới class chưa rõ;
- text nguồn bị lỗi/thiếu;
- cần đối chiếu thêm guideline/taxonomy.

Không được ép case chưa rõ thành REVIEWED chỉ để đạt 0 pending.
#### 10. Quy tắc notes
notes để trống với case thông thường.
Bắt buộc ghi notes khi:
- lặp ngữ cảnh sau split;
- clause là hard case;
- label dựa trên rule phân biệt dễ nhầm;
- nguồn dẫn chiếu nội quy/tài liệu ngoài;
- source text có lỗi nhưng vẫn giữ nguyên;
- có nguy cơ risk/evaluation đặc biệt;
- quyết định annotation khác trực giác nhưng cần giữ consistency.
#### 11. Duplicate và data leakage
##### 11.1. Không tự động xóa duplicate
- Exact duplicate/near-duplicate vẫn có thể có giá trị để phản ánh các mẫu hợp đồng thực tế.
- Không xóa chỉ vì text giống nhau nếu chưa có quyết định dataset-level.
##### 11.2. Bắt buộc dùng similarity_group
[contracts_metadata.csv](../data/contracts_metadata.csv) lưu similarity_group.
Ví dụ hiện tại:
- HDLD001, HDLD002 → SIM_A
- HDLD005, HDLD006 → SIM_D
##### 11.3. Không split theo clause ngẫu nhiên
Khi tạo train/dev/test:
- không random toàn bộ clause rồi chia;
- phải group theo similarity_group;
- mọi contract trong cùng similarity_group phải nằm cùng một split.

Mục tiêu: tránh một câu/template xuất hiện ở train và gần như y hệt ở test, làm F1 bị inflate.
#### 12. QC checklist trước khi merge dataset
Mỗi batch mới phải đạt:
- [ ] đúng schema của version (v01–v03: 7 cột; v04: 9 cột; v05–v06: 10 cột);
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
#### 13. Quy trình version
Không sửa ngược dataset version đã coi là archived.
Ví dụ:
- clauses_v01.csv → archived
- clauses_v02.csv → archived
- clauses_v03.csv → archived
- clauses_v04.csv → archived
- clauses_v05.csv → archived
- clauses_v06.csv → current
Khi append một batch contract mới đã QC xong, tạo version processed mới (v04, v05, ...), sau đó cập nhật metadata/docs tương ứng.

#### 14. Chính sách đa nhãn và chủ đề chờ xác nhận (đề xuất OI-10)
**Trạng thái: ĐỀ XUẤT — CHƯA ĐƯỢC DÙNG LÀM QUY TẮC GOLD/FREEZE.** Nội dung dưới
đây chép theo đề xuất trong hồ sơ freeze để N2/N3 xem xét; khi chưa có sign-off,
quy trình gán gold tiếp tục theo policy đã được nhóm xác nhận riêng.

##### 14.1. Đề xuất số nhãn và nhãn chính
- Mặc định một nhãn; chỉ thêm nhãn phụ nếu clause có một câu/mệnh đề trọn vẹn
  mang chủ đề độc lập thuộc nhãn khác. Từ khóa được nhắc thoáng qua không đủ.
- Tối đa ba nhãn, không trùng; nhãn đầu là nhãn chính theo chủ đề chiếm nhiều
  nội dung nhất. Nếu hòa, chọn chủ đề xuất hiện trước trong clause.
- Đề xuất `OTHER` chỉ đứng một mình khi không có nhãn cụ thể phù hợp. Quy tắc này
  chưa được thực thi trong code và cần N1/N2/N3 xác nhận trước khi thay validator.
- Clause chỉ có heading vẫn nhận nhãn theo chủ đề heading nếu được đưa vào tập.
  Không nhận role trong quá trình phân loại.

##### 14.2. Dữ liệu lịch sử một nhãn và phép đo
`clauses_v06.csv` có một nhãn mỗi dòng và không tạo partition đầy đủ của
`canonical_text`. Đề xuất cho M7: với clause dự đoán, tập nhãn vàng là hợp các nhãn
của dòng `EXACT` có span giao nhau; bỏ `CONTEXT` khỏi chấm span; chấm theo cặp
(clause, label), đồng thời báo riêng độ đúng nhãn chính và số nhãn trung bình.
Quy tắc chuyển đổi này vẫn cần N2 xác nhận và không biến v06 thành gold segmentation
hay gold đa nhãn đã adjudicate.

##### 14.3. Ba chủ đề cần N2/N3 thống nhất
- Bảo mật/không cạnh tranh/SHTT của NLĐ: đề xuất nhãn chính
  `EMPLOYEE_OBLIGATIONS_DISCIPLINE`; thêm `TERMINATION` chỉ khi clause nêu rõ
  hậu quả hoặc điều kiện sau chấm dứt.
- Giải quyết tranh chấp/luật áp dụng: đề xuất `OTHER`.
- Bồi thường cho NLĐ: câu nêu nghĩa vụ NSDLĐ phải bồi thường →
  `EMPLOYER_RIGHTS_OBLIGATIONS`; quyền chung của NLĐ không nêu chủ thể NSDLĐ rõ →
  `OTHER`. Cần xác nhận cùng N3 và kiểm tra mẫu lịch sử.

##### 14.4. Sign-off và lịch sử sửa đổi
| Vai trò | Nội dung | Trạng thái |
|---|---|---|
| N1 | Đề xuất OI-10 và ba ánh xạ chủ đề | Đã đề xuất; không thay cho duyệt |
| N2 | Quy đổi dữ liệu v06/M7 và wording guideline | Chờ xác nhận |
| N3 | Chủ đề bảo mật/không cạnh tranh và giao thoa risk taxonomy | Chờ xác nhận |

Changelog 2026-11-02: thêm liên kết provenance, tách rõ policy đang dùng với
đề xuất OI-10; chưa thay nhãn, dữ liệu, BRD/SRS hay trạng thái MS-1.
