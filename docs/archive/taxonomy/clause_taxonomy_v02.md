# Clause Taxonomy v0.2

## 1. Mục đích

Tài liệu này định nghĩa các nhãn `clause_type` sử dụng trong dataset của project **AI Contract Risk Analyzer** cho hợp đồng lao động tiếng Việt.

Phiên bản v0.2 được chốt sau khi segment và review 3 hợp đồng pilot (`HDLD001`–`HDLD003`), tổng cộng **140 clauses**.

## 2. Danh sách Clause Types

| Clause type | Ý nghĩa | Ví dụ nội dung |
|---|---|---|
| `JOB_INFO` | Công việc, chức danh, bộ phận, địa điểm, nhiệm vụ và phạm vi công việc | Địa điểm làm việc; chức danh; nhiệm vụ |
| `CONTRACT_TERM` | Loại và thời hạn HĐLĐ, ngày bắt đầu/kết thúc | HĐ xác định/không xác định thời hạn |
| `COMPENSATION_BENEFITS` | Lương, phụ cấp, thưởng, nâng lương, công tác phí và các chế độ/quyền lợi tài chính | Mức lương; phụ cấp; trợ cấp |
| `WORKING_TIME` | Giờ làm, lịch làm, ca làm, làm thêm giờ/tăng ca | 8 giờ/ngày; lịch Thứ 2–Thứ 7 |
| `LEAVE` | Nghỉ hàng tuần, phép năm, nghỉ lễ/Tết, nghỉ bù | 12 ngày phép/năm |
| `INSURANCE_SAFETY` | BHXH/BHYT/BHTN, an toàn và vệ sinh lao động | BHXH; điều kiện ATVSLĐ |
| `WORKING_CONDITIONS` | Công cụ, thiết bị, phương tiện và điều kiện vật chất phục vụ công việc | Công ty cấp công cụ/thiết bị |
| `TRAINING` | Đào tạo, bồi dưỡng, cam kết sau đào tạo và hoàn trả chi phí đào tạo | Hoàn trả phí đào tạo |
| `EMPLOYEE_OBLIGATIONS_DISCIPLINE` | Nghĩa vụ, kỷ luật, trách nhiệm vật chất, bồi thường và nghĩa vụ thuế của NLĐ | Tuân thủ nội quy; nộp thuế |
| `EMPLOYER_RIGHTS_OBLIGATIONS` | Quyền và nghĩa vụ quản lý, điều hành của NSDLĐ | Điều chuyển, quản lý, yêu cầu bồi thường |
| `TERMINATION` | Căn cứ, điều kiện, thủ tục, báo trước và hậu quả của việc chấm dứt HĐLĐ | Đơn phương chấm dứt; thời hạn báo trước |
| `OTHER` | Điều khoản thi hành, sửa đổi/phụ lục và các nội dung không phù hợp các nhóm trên | Hiệu lực; số bản; phụ lục |

## 3. Quy tắc segmentation

### Rule 1 — Một clause nên biểu diễn một ý nghĩa chính

Nếu một câu chứa hai chủ đề độc lập, ưu tiên tách thành hai clauses.

Ví dụ câu chứa cả bảo hiểm và thuế được tách thành:

- `INSURANCE_SAFETY`
- `EMPLOYEE_OBLIGATIONS_DISCIPLINE`

Khi hai chủ đề dùng chung một vị ngữ, được phép lặp phần vị ngữ chung tối thiểu để mỗi clause sau khi tách có thể đứng độc lập. Trường hợp này phải ghi rõ trong `notes`.

### Rule 2 — Một Điều không mặc định bằng một clause

Một Điều có thể chứa nhiều clause types khác nhau. Ví dụ Điều về thời giờ làm việc có thể đồng thời chứa `WORKING_TIME`, `LEAVE` và `INSURANCE_SAFETY`.

### Rule 3 — Giữ nguyên nội dung nguồn tối đa

Không diễn giải hoặc rút gọn `clause_text` theo ý người annotate. Chỉ cho phép tái cấu trúc tối thiểu khi tách một câu multi-topic theo Rule 1 và phải ghi chú.

### Rule 4 — Các bullet độc lập có thể là các clauses riêng

Các bullet như mức lương, phụ cấp, hình thức trả lương, thời hạn trả lương có thể được tách riêng dù cùng thuộc `COMPENSATION_BENEFITS`.

### Rule 5 — Không annotate phần hành chính

Không đưa quốc hiệu, tiêu ngữ, tên công ty, thông tin định danh hai bên, CCCD, địa chỉ và chữ ký vào clause dataset.

### Rule 6 — Heading không phải clause

Tên Điều/Mục được lưu ở `section_title`; nội dung bên dưới mới là `clause_text`.

## 4. Quy tắc phân biệt các class dễ nhầm

### `WORKING_CONDITIONS` vs `INSURANCE_SAFETY`

- `WORKING_CONDITIONS`: công cụ, thiết bị, phương tiện hoặc điều kiện vật chất phục vụ công việc.
- `INSURANCE_SAFETY`: bảo hiểm bắt buộc, an toàn lao động, vệ sinh lao động và điều kiện bảo hộ/an toàn.

### `EMPLOYEE_OBLIGATIONS_DISCIPLINE` vs `COMPENSATION_BENEFITS`

- Nghĩa vụ thuế của NLĐ → `EMPLOYEE_OBLIGATIONS_DISCIPLINE`.
- Khoản tiền/quyền lợi NLĐ được hưởng → `COMPENSATION_BENEFITS`.

### `EMPLOYER_RIGHTS_OBLIGATIONS` vs `TERMINATION`

Dùng `EMPLOYER_RIGHTS_OBLIGATIONS` khi clause mô tả **quyền quản lý tổng quát của NSDLĐ**, kể cả khi danh sách có nhắc tới tạm hoãn, chấm dứt hoặc kỷ luật.

Dùng `TERMINATION` khi nội dung chính trực tiếp quy định:

- căn cứ chấm dứt;
- quyền đơn phương chấm dứt;
- điều kiện chấm dứt;
- thời hạn báo trước;
- nghĩa vụ hoặc quyền lợi phát sinh khi chấm dứt.

## 5. Quy tắc Clause ID

Định dạng chuẩn:

`<contract_id>_C<3 chữ số>`

Ví dụ: `HDLD001_C001`.

Đối với clause phát sinh do tách một clause đã có ID trong pilot dataset, có thể dùng hậu tố chữ cái để tránh renumber toàn bộ dữ liệu, ví dụ `HDLD003_C018A`.

## 6. Trạng thái annotation

- `REVIEWED`: clause đã được review và có thể dùng trong pilot dataset.
- `NEEDS_REVIEW`: clause còn tranh luận về segmentation hoặc taxonomy.

Sau review v0.2:

- `REVIEWED = 140`
- `NEEDS_REVIEW = 0`

## 7. Phân bố dataset v0.2

| Clause type | Số lượng |
|---|---:|
| `COMPENSATION_BENEFITS` | 24 |
| `CONTRACT_TERM` | 3 |
| `EMPLOYEE_OBLIGATIONS_DISCIPLINE` | 20 |
| `EMPLOYER_RIGHTS_OBLIGATIONS` | 16 |
| `INSURANCE_SAFETY` | 7 |
| `JOB_INFO` | 15 |
| `LEAVE` | 9 |
| `OTHER` | 12 |
| `TERMINATION` | 15 |
| `TRAINING` | 9 |
| `WORKING_CONDITIONS` | 3 |
| `WORKING_TIME` | 7 |
| **Tổng** | **140** |

## 8. Thay đổi chính từ v0.1 → v0.2

1. Đồng bộ tên label trong taxonomy với label thực tế đang dùng trong CSV.
2. Thêm `WORKING_CONDITIONS`.
3. Chuyển các clause về thuế TNCN sang `EMPLOYEE_OBLIGATIONS_DISCIPLINE`.
4. Tách `HDLD003_C018` thành bảo hiểm và thuế.
5. Chốt rule phân biệt `EMPLOYER_RIGHTS_OBLIGATIONS` với `TERMINATION`.
6. Review toàn bộ 11 clauses `NEEDS_REVIEW`; dataset hiện không còn clause chờ review.
