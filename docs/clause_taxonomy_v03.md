Clause Taxonomy v0.3
1. Mục đích
Tài liệu này định nghĩa các nhãn clause_type sử dụng trong dataset của project AI Contract Risk Analyzer cho hợp đồng lao động tiếng Việt.
Phiên bản v0.3 giữ nguyên 12 clause types của v0.2, nhưng bổ sung clarification sau khi annotate và review HDLD004.
Dataset snapshot tương ứng hiện tại: clauses_v03.csv — 183 clauses / 4 contracts.
clause_taxonomy_v02.md được giữ nguyên như historical snapshot của dataset 140 clauses. Không overwrite v0.2.

2. Danh sách Clause Types
Clause type	Ý nghĩa	Ví dụ nội dung
JOB_INFO	Công việc, chức danh, bộ phận, địa điểm, nhiệm vụ và phạm vi công việc	Địa điểm làm việc; chức danh; nhiệm vụ
CONTRACT_TERM	Loại và thời hạn HĐLĐ, ngày bắt đầu/kết thúc, thời điểm có hiệu lực	HĐ xác định/không xác định thời hạn; ngày hiệu lực
COMPENSATION_BENEFITS	Bản thân lương, phụ cấp, thưởng, nâng lương, công tác phí và quyền lợi tài chính	Mức lương; phụ cấp; thưởng
WORKING_TIME	Giờ làm, lịch làm, ca làm, làm thêm và thời gian nghỉ trong ngày	8 giờ/ngày; nghỉ liên tục trong ngày
LEAVE	Ngày nghỉ hàng tuần, phép năm, nghỉ lễ/Tết, nghỉ bù và các ngày nghỉ	12 ngày phép/năm
INSURANCE_SAFETY	BHXH/BHYT/BHTN, mức đóng bảo hiểm, an toàn, vệ sinh và bảo hộ lao động	BHXH; PPE; ATVSLĐ
WORKING_CONDITIONS	Công cụ, thiết bị, phương tiện, chỗ ăn/ở và điều kiện vật chất phục vụ công việc	Công ty cấp thiết bị; bố trí chỗ ở
TRAINING	Đào tạo, bồi dưỡng, học nghề/học văn hóa, cam kết sau đào tạo, hoàn trả chi phí	Hoàn trả phí đào tạo
EMPLOYEE_OBLIGATIONS_DISCIPLINE	Nghĩa vụ, kỷ luật, trách nhiệm vật chất, bồi thường và nghĩa vụ thuế của NLĐ	Tuân thủ nội quy; bồi thường tài sản
EMPLOYER_RIGHTS_OBLIGATIONS	Quyền quản lý và nghĩa vụ mà NSDLĐ phải thực hiện/đảm bảo đối với NLĐ	Điều hành; đăng ký tạm trú; nghĩa vụ thanh toán
TERMINATION	Căn cứ, điều kiện, sa thải/chấm dứt, báo trước và hậu quả trực tiếp của chấm dứt HĐLĐ	Đơn phương chấm dứt; sa thải
OTHER	Điều khoản thi hành, sửa đổi/phụ lục hoặc nội dung chưa có class phù hợp	Số bản; dẫn chiếu chung; quyền bồi thường của NLĐ khi taxonomy chưa có class riêng


3. Nguyên tắc segmentation liên quan taxonomy
Chi tiết đầy đủ nằm trong docs/annotation_guideline.md.
1. Một clause ưu tiên một semantic topic chính.
2. Có thể split multi-topic clause.
3. Clause sau split phải đứng độc lập.
4. Được lặp ngữ cảnh tối thiểu từ câu nguồn khi cần, và phải ghi notes.
5. Không paraphrase hoặc bổ sung nghĩa mới.
4. Quy tắc phân biệt các class dễ nhầm
4.1. WORKING_TIME vs LEAVE
WORKING_TIME:
- thời lượng làm việc;
- ca/lịch làm;
- làm thêm;
- nghỉ giữa ca/nghỉ trong ngày.
LEAVE:
- ngày nghỉ hàng tuần;
- phép năm;
- lễ/Tết;
- nghỉ bù;
- ngày nghỉ khác.
4.2. WORKING_CONDITIONS vs INSURANCE_SAFETY
WORKING_CONDITIONS:
- công cụ, thiết bị, phương tiện;
- chỗ ăn, chỗ ở;
- điều kiện vật chất.
INSURANCE_SAFETY:
- bảo hiểm;
- mức đóng bảo hiểm;
- an toàn/vệ sinh;
- bảo hộ lao động/PPE.
4.3. COMPENSATION_BENEFITS vs EMPLOYER_RIGHTS_OBLIGATIONS
Dùng COMPENSATION_BENEFITS khi clause định nghĩa quyền lợi tài chính:
- mức lương;
- khoản phụ cấp;
- mức thưởng;
- hình thức/kỳ hạn trả lương;
- chế độ nâng lương.
Dùng EMPLOYER_RIGHTS_OBLIGATIONS khi trọng tâm là NSDLĐ có nghĩa vụ phải thanh toán/đảm bảo các chế độ hoặc quyền lợi đã thỏa thuận.
Ví dụ:
NSDLĐ có nghĩa vụ thanh toán đầy đủ, đúng thời hạn...
→ EMPLOYER_RIGHTS_OBLIGATIONS.
4.4. EMPLOYEE_OBLIGATIONS_DISCIPLINE vs INSURANCE_SAFETY
Nếu clause chủ yếu quy định NLĐ phải tuân thủ hướng dẫn, giữ gìn thiết bị, phòng cháy hoặc chấp hành quy định thì ưu tiên EMPLOYEE_OBLIGATIONS_DISCIPLINE.
Nếu topic chính trực tiếp là PPE/an toàn/bảo hiểm thì dùng INSURANCE_SAFETY.
4.5. EMPLOYER_RIGHTS_OBLIGATIONS vs TERMINATION
Dùng EMPLOYER_RIGHTS_OBLIGATIONS khi termination chỉ xuất hiện trong quyền quản lý tổng quát.
Dùng TERMINATION khi nội dung chính trực tiếp quy định:
- căn cứ;
- quyền đơn phương;
- sa thải;
- điều kiện;
- thời hạn báo trước;
- nghĩa vụ/quyền lợi trực tiếp khi chấm dứt.
4.6. Bồi thường / damages
- NLĐ phải bồi thường → EMPLOYEE_OBLIGATIONS_DISCIPLINE.
- NSDLĐ có quyền yêu cầu bồi thường → EMPLOYER_RIGHTS_OBLIGATIONS.
- NSDLĐ phải bồi thường cho NLĐ → EMPLOYER_RIGHTS_OBLIGATIONS.
- Quyền của NLĐ được bồi thường nhưng clause quá chung và không có class chuyên biệt → OTHER + notes.
5. Clause ID
Định dạng mặc định:
<contract_id>_C<3 chữ số>
Ví dụ:
HDLD004_C001
Nếu split một row của dataset đã phát hành và renumber gây ảnh hưởng lớn, được phép dùng suffix chữ cái, ví dụ HDLD003_C018A.
6. Annotation status
- REVIEWED
- NEEDS_REVIEW
Không ép case chưa chắc chắn thành REVIEWED.
7. Phân bố dataset v0.3
Clause type	Số lượng
COMPENSATION_BENEFITS	32
CONTRACT_TERM	7
EMPLOYEE_OBLIGATIONS_DISCIPLINE	26
EMPLOYER_RIGHTS_OBLIGATIONS	21
INSURANCE_SAFETY	10
JOB_INFO	17
LEAVE	13
OTHER	14
TERMINATION	16
TRAINING	12
WORKING_CONDITIONS	6
WORKING_TIME	9
Tổng	183


8. Thay đổi chính từ v0.2 → v0.3
1. Giữ nguyên 12 labels; không thêm class mới.
2. Bổ sung HDLD004 vào dataset processed.
3. Làm rõ COMPENSATION_BENEFITS vs EMPLOYER_RIGHTS_OBLIGATIONS.
4. Làm rõ treatment của bồi thường thiệt hại.
5. Yêu cầu clause sau split phải có đủ ngữ cảnh để đứng độc lập.
6. Cho phép lặp ngữ cảnh tối thiểu từ source khi split và bắt buộc ghi notes.
7. Cập nhật distribution từ 140 → 183 clauses.