Dataset Schema
1. Mục đích
Tài liệu này mô tả cấu trúc thư mục, schema dữ liệu, constraints, quy ước ID/version và nguyên tắc chia dữ liệu của dataset trong project AI Contract Risk Analyzer.
2. Cấu trúc thư mục
data/
├── raw/
│   ├── contracts/
│   │   ├── HDLD001.doc
│   │   ├── ...
│   │   └── HDLD006.docx
│   └── annotated/
├── processed/
│   ├── clauses_v01.csv
│   ├── clauses_v02.csv
│   ├── clauses_v03.csv
│   ├── clauses_v04.csv
│   └── raw_text/
│       ├── HDLD001.txt
│       └── ... HDLD006.txt
└── contracts_metadata.csv
data/raw/contracts/
Chứa file nguồn gốc.
- không sửa nội dung;
- không overwrite bằng bản clean/normalize;
- filename chuẩn theo contract_id;
- dùng làm ground truth để truy vết annotation.
data/raw/annotated/
Thư mục tùy chọn dành cho bản source có đánh dấu annotation thủ công nếu sau này cần lưu.
Hiện tại không bắt buộc sử dụng vì ground-truth structured đã nằm trong data/processed/clauses_vXX.csv.
Không copy clauses_vXX.csv vào thư mục này.
data/processed/
Chứa dataset clause đã xử lý/annotate. Mỗi version là một snapshot độc lập.
`raw_text/` chứa bản trích UTF-8 từ đúng file gốc trong `data/raw/contracts/`;
xem `data/processed/raw_text/README.md` để biết cách tái tạo. Không thêm
annotation vào raw text nhằm tạo ra một span giả.
3. Schema clauses_vXX.csv
Thứ tự cột bắt buộc:
Column	Type	Required	Ý nghĩa
clause_id	string	Yes	ID duy nhất của clause
contract_id	string	Yes	Contract chứa clause
section_title	string	Yes	Điều/Mục của clause
clause_text	string	Yes	Text dùng làm input/ground truth
clause_type	enum	Yes	Nhãn clause taxonomy
annotation_status	enum	Yes	Trạng thái review
notes	string	No	Giải thích case đặc biệt

Từ `clauses_v04.csv`, thêm hai cột cuối:
Column	Type	Required	Ý nghĩa
start_offset	integer/string rỗng	No	Vị trí ký tự bắt đầu (bao gồm) trong raw_text/<contract_id>.txt
end_offset	integer/string rỗng	No	Vị trí ký tự kết thúc (không bao gồm) trong cùng raw text

Offset dùng chỉ số ký tự Python, không phải chỉ số byte UTF-8. Nếu cả hai cột
có giá trị, `raw_text[start_offset:end_offset]` phải khớp `clause_text` sau khi
chuẩn hóa duy nhất các chuỗi khoảng trắng thành một dấu cách. Vị trí vẫn chỉ
đến đúng đoạn gốc, kể cả khi gốc chứa xuống dòng hoặc non-breaking space.
Nếu annotation tách một câu và lặp ngữ cảnh làm văn bản không còn là một đoạn
liên tục trong nguồn, để trống cả hai cột và ghi `OFFSET_UNVERIFIED` trong
notes. Không suy đoán offset hoặc ghép văn bản không có trong nguồn.


clause_id
Format:
<contract_id>_C<3 chữ số>
Constraints:
- unique toàn file;
- không rỗng;
- prefix phải khớp contract_id.
contract_id
Format:
HDLDxxx
Mọi contract_id trong clauses dataset phải có record tương ứng trong data/contracts_metadata.csv.
section_title
Theo convention hiện tại dùng cấp Điều, ví dụ:
- Điều 1
- Điều 4
clause_text
- không rỗng;
- giữ nguồn tối đa;
- không paraphrase;
- chỉ normalization tối thiểu theo docs/annotation_guideline.md;
- CSV phải quote đúng khi text chứa dấu phẩy;
- encoding UTF-8.
clause_type
Allowed values:
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
Không tự tạo label mới trong CSV trước khi taxonomy được version/update.
annotation_status
Allowed values:
- REVIEWED
- NEEDS_REVIEW
notes
Optional. Dùng cho:
- lý do split/normalization;
- ambiguity/hard case;
- dẫn chiếu tài liệu ngoài;
- source text có lỗi;
- quyết định label cần audit.
4. Schema contracts_metadata.csv
Column	Type	Required	Ý nghĩa
contract_id	string	Yes	ID contract
source_id	string	Yes	ID nguồn trong data_sources.md
original_name	string	No	Tên gốc của tài liệu
file_name	string	Yes	File trong data/raw/contracts/
contract_type	string	Yes	Loại contract dạng machine-friendly
file_format	string	Yes	DOC/DOCX/PDF/...
page_count	integer	No	Số trang file nguồn
similarity_group	string	Yes	Nhóm template/near-duplicate
dataset_status	enum	Yes	Trạng thái sử dụng dữ liệu
clause_count	integer	No	Số clause đã annotate
dataset_version	string	No	Version processed hiện chứa contract
notes	string	No	Ghi chú provenance/QC


similarity_group
Format gợi ý:
SIM_A, SIM_B, ...
- cùng group = cùng template family hoặc near-duplicate đáng kể;
- dùng để chống leakage khi split;
- không phải feature đầu vào cho model.
dataset_status
Allowed values:
- ANNOTATED
- TO_ANNOTATE
- HOLD_NEAR_DUPLICATE
- EXCLUDED
clause_count
Chỉ điền khi contract đã annotate/review.
Phải bằng số row có contract_id tương ứng trong processed dataset.
5. Quan hệ giữa các file
docs/data_sources.md
      │ source_id
      ▼
data/contracts_metadata.csv
      │ contract_id
      ▼
data/processed/clauses_vXX.csv
Constraints:
1. Mỗi contract_id trong clauses phải tồn tại trong metadata.
2. Mỗi source_id trong metadata phải tồn tại trong data_sources.md.
3. clause_count phải khớp số row thực tế.
4. File raw phải tồn tại ở data/raw/contracts/<file_name>.
6. Versioning
Processed dataset
Tên:
- clauses_v01.csv
- clauses_v02.csv
- clauses_v03.csv
- clauses_v04.csv
Quy tắc:
- version cũ đã archived không chỉnh lại;
- append/relabel đáng kể tạo version mới;
- chỉ một version được coi là current trong workflow.
Taxonomy
Tên:
- clause_taxonomy_v01.md
- clause_taxonomy_v02.md
- clause_taxonomy_v03.md
Không overwrite taxonomy cũ sau khi đã dùng cho một dataset snapshot.
Annotation guideline
Guideline là tài liệu sống nhưng heading phải có version khi rule segmentation thay đổi đáng kể.
7. Dataset split
Không chia train/dev/test bằng random clause-level split trên toàn dataset.
Quy trình:
1. Group contract theo similarity_group.
2. Gán cả group vào một split.
3. Không để cùng template family xuất hiện ở nhiều split.
4. Sau split, kiểm exact duplicate/near-duplicate giữa train/dev/test.
5. Nếu có leakage, sửa split trước evaluation.
8. QC bắt buộc
Structural QC
- tên/thứ tự cột đúng;
- không duplicate clause_id;
- required fields không rỗng;
- enum hợp lệ;
- encoding UTF-8.
Annotation QC
- source text đã đối chiếu raw;
- segmentation theo guideline;
- label theo taxonomy;
- NEEDS_REVIEW được xử lý hoặc thống kê rõ;
- notes có ở hard case.
Dataset QC
- class distribution;
- clause count theo contract;
- exact duplicate count;
- near-duplicate/template groups;
- leakage theo similarity_group.
9. Snapshot hiện tại — v04
data/processed/clauses_v04.csv giữ nguyên 183 annotation và 12 nhãn của v03,
thêm raw text và offset. Các thống kê phân phối bên dưới vẫn là thống kê v03/v04.
Contract	Clauses	Similarity group
HDLD001	39	SIM_A
HDLD002	40	SIM_A
HDLD003	61	SIM_B
HDLD004	43	SIM_C
Total	183	


Class distribution:
Clause type	Count
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
Total	183


Current structural checks:
- duplicate clause_id: 0
- missing required fields: 0
- invalid clause labels: 0
- non-REVIEWED: 0
Offset QC:
- 174/183 clause có span đã xác minh theo quy tắc khoảng trắng ở trên.
- 9 clause để trống offset và có `OFFSET_UNVERIFIED` trong notes:
  HDLD001_C014 (nguồn có ký tự `S` sau `hàng tuần`),
  HDLD003_C018, HDLD003_C018A (tách câu đa chủ đề),
  HDLD004_C023–C027 (tách bullet đa chủ đề và lặp ngữ cảnh),
  HDLD004_C043 (lặp chủ ngữ khi tách câu).
- HDLD005–HDLD006 đã có raw text, nhưng chưa được annotate trong snapshot này.
Exact duplicate clause texts có thể vẫn tồn tại giữa các template và được xử lý bằng similarity_group/split policy, không tự động xóa.
