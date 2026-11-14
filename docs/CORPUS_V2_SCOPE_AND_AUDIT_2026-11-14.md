# Corpus v2: kiểm toán và phạm vi đề nghị — 14/11/2026

**Trạng thái:** gói duyệt phạm vi, chưa phê duyệt provision hoặc kích hoạt runtime. Chỉ xét hợp đồng lao động. Nguồn số liệu là checkout Pipeline tại `c955a7ab` và Data `a4a3b12`; đối chiếu lại khi PR tích hợp Pipeline đổi HEAD. Không dùng nội dung hay dự đoán T1/T2 để chọn luật, cạnh, trọng số hoặc prompt.

## 1. Kết luận kiểm toán v1 và metric

| Nhận xét đang lưu | Phán định tại checkout | Bằng chứng / việc cần làm |
| --- | --- | --- |
| Corpus có 16 provision ở Điều 13–17, 21; bảy ánh xạ nhãn điều khoản và năm cạnh | **Đúng về cấu trúc** | `data/legal_corpus/{provisions.jsonl,label_map.yaml,edges.jsonl}` ở Pipeline `c955a7ab`; năm ánh xạ đầu là điểm Điều 21, hai ánh xạ còn lại là Điều 17. Không suy ra 21 nhãn rủi ro được bao phủ. |
| Corpus v1 đã được duyệt pháp lý vì manifest ghi `APPROVED` | **Không đủ bằng chứng** | Manifest v02 ghi `APPROVED`, ba hash khớp dữ liệu; README vẫn ghi `DRAFT`, 16 dòng thiếu reviewer/review receipt và README nói chờ rà soát hiệu lực. Có ghi nhận chủ dự án duyệt bốn cạnh ở `docs/PR_AND_BRANCH_HANDOFF_2026-11-13.md`, nhưng chưa thấy hồ sơ độc lập cho từng provision/cạnh. Giữ nguyên snapshot; chặn tuyên bố đã duyệt pháp lý cho đến khi N2/N3 xuất trình receipt theo ID, phiên bản và ngày. |
| M1 Dev 0,90656 và T1 0,37175 | **Đúng nhưng khác đơn vị gán nhãn** | `docs/PROJECT_ACCEPTANCE_READOUT_2026-11-13.md` §metric: D2 Dev 228/250 TP; T1 held-out 229/842 TP. Chốt annotation unit trước khi so sánh hoặc đổi segmentation. |
| M2 Dev 0,97077 chứng minh 21 nhãn | **Sai** | D1+D2 Dev chỉ có Gold dương cho 6/21 nhãn; all-21 macro-F1 được báo là 0,27736. T1 read-only 0,33333 chỉ có Gold dương 2/21 nhãn, 3 positive items. Đây là heuristic, không phải phép chứng minh mô hình sản phẩm. |
| T1 M2 v02 gồm 1.494 role rows và 17 ngoại lệ | **Đúng theo manifest restricted; chưa tự xác minh nội dung** | `docs/M2_T1_CLOSED_CORPUS_METADATA_2026-11-13.md`; manifest ignored `data/intake/restricted/T1_m2_risk_gold_v02/manifest.json` được kiểm tra **metadata**: 1.474 âm trong corpus, 3 dương, 17 ngoại lệ. 190 role references CONTEXT là phép chiếu segmentation, không phải dòng M2. N2/reviewer độc lập xét 17 ngoại lệ sau khi khóa v2; không chuyển thành NO_RISK. |
| M5 T2 là 12/30 | **Cũ** | Bản frozen gần nhất trong readout: 26/30; 12/30 là run 06/11. D2 Dev 30/30 là tập khác. |
| M6 D2 Dev 39/40 A/B; M7 D1 0,51062; M8 Dev Off 66/74, On 74/74 | **Đúng trong phạm vi đã báo** | `docs/PROJECT_ACCEPTANCE_READOUT_2026-11-13.md`: M6 còn thiếu held-out; M7 là local baseline; M8 dùng predicted-label primary, D2 oracle chưa có Gold nhãn điều khoản. M3a/M4 chỉ chứng minh hợp lệ cấu trúc trên output đã phát. M8 T2 cũ Off 15/30, On 14/30, không thay bằng điểm Dev. |
| Data PR #21 merge; Pipeline PR #34 đóng chưa merge | **Đúng tại 14/11** | [Data PR #21](https://github.com/24021368-DucAnh/ai-contract-risk-analyzer/pull/21) merge `fe3a07a`; [Pipeline PR #34](https://github.com/sosadsonar/ai-contract-risk-analyzer-pipeline/pull/34) đóng chưa merge. [Pipeline PR #37](https://github.com/sosadsonar/ai-contract-risk-analyzer-pipeline/pull/37) là nhánh tích hợp mới, đang mở; phần mô tả PR tự yêu cầu chưa merge vội vì corpus v02 thiếu hồ sơ duyệt. |
| PR tích hợp mới đã chứa sửa CI D1 `c955a7ab` | **Sai tại HEAD PR #37 `2799d09c`** | So sánh GitHub `c955a7ab...2799d09c` cho kết quả `diverged`, nhánh PR đi sau commit sửa CI một commit. N1/N4 ghép và chạy lại CI trước khi merge; không kéo nhánh W5/W6 vào gói corpus. |

Ba SHA-256 tính lại từ **bytes** của v1 khớp manifest: `provisions.jsonl` `f8a3b6b5bd34d0352da1dad05e156b246cd78e470386c5634732073151dfb44b`; `edges.jsonl` `bce0f9dcf457f130493816ff3e3281268abaf2c1b760696cb49452fe91f9e098`; `label_map.yaml` `e9b652af68e25ea55f2d7bf32599256aea9a2d1cf4afda416ef880f2a4dc89ad`. Hash xác nhận tính toàn vẹn snapshot, không xác nhận nội dung đúng hay đã duyệt.

## 2. Nguồn luật và quyết định phạm vi sơ bộ

`B` = [Bộ luật Lao động 45/2019/QH14](https://vanban.chinhphu.vn/?classid=1&docid=198540&orggroupid=1&pageid=27160), hiệu lực gốc 01/01/2021. [VBHN 18/VBHN-VPQH](https://vanban.chinhphu.vn/?classid=0&docid=217002&pageid=27160) ban hành 12/02/2026 là bản đối chiếu; không thay thế lịch sử sửa đổi theo khoản/điểm. `N145` = [NĐ 145/2020/NĐ-CP](https://vanban.chinhphu.vn/?docid=201967&pageid=27160), hiệu lực gốc 01/02/2021. `N293` = [NĐ 293/2025/NĐ-CP](https://vanban.chinhphu.vn/?docid=215832&pageid=27160), hiệu lực 01/01/2026. `N399` = [NĐ 399/2026/NĐ-CP](https://vanban.chinhphu.vn/?docid=220166&orggroupid=2&pageid=27160), ban hành 02/11/2026 và hiệu lực **01/01/2027**. `N283` = [NĐ 283/2026/NĐ-CP](https://vanban.chinhphu.vn/?docid=218871&pageid=27160&typegroupid=4), hiệu lực 10/09/2026. Các ngày ở đây là **metadata văn bản**, chưa xác định hiệu lực từng provision hay điều khoản chuyển tiếp.

Điểm mới so với kế hoạch cục bộ: N399 đã được ban hành; vì vậy không ghim N293 vô thời hạn. N2 kiểm PDF ký, bảng địa bàn/vùng, điều khoản chuyển tiếp và văn bản bị thay thế; chỉ sau đó mới đóng `effective_to` của N293 và tạo version N399 cho ngày phân tích từ 2027. Không nhập số tiền hoặc bảng vùng từ OCR chưa soát. N283 là ứng viên **P1 cho provenance/hiệu lực**, không lấy mức phạt làm căn cứ rủi ro mặc định. N145 và [Thông tư 10/2020/TT-BLĐTBXH](https://vbpl.vn/botuphap/Pages/vbpq-toanvan.aspx?ItemID=146696) là hai nguồn hướng dẫn cần N2/N3 chốt; file ký của Thông tư 10 chưa có receipt/hash theo `docs/LEGAL_SOURCE_DISCOVERY_2026-11-02.md`, nên chưa được nhập. Các luật ngoài BLLĐ trong taxonomy là ứng viên P1/P2, không mặc nhiên là một trong “hai nghị định” cần thêm.

### Ma trận 21 nhãn rủi ro ↔ căn cứ ứng viên

Ma trận lấy **cột căn cứ ứng viên** từ `docs/RISK_TAXONOMY_v0.1.md`, không xác nhận một điều khoản cụ thể đã đủ căn cứ kết luận pháp lý. `Hiện có` là node/label-map v1; `—` nghĩa là chưa thấy node trực tiếp. Mọi hàng đều **PENDING_SCOPE_AND_SOURCE_REVIEW**; N2 kiểm nguồn/hiệu lực, N3 kiểm semantics nhãn và N1 kiểm tác động annotation. P0/P1 là thứ tự xét, không là quyền nhập runtime.

| Risk label | Clause label tham khảo | Hiện có v1 | Căn cứ ứng viên và thiếu hụt | Ưu tiên |
| --- | --- | --- | --- | --- |
| CONTRACT_TERM_TYPE | CONTRACT_TERM | Điều 21.1.d (nội dung thời hạn), chưa có Điều 20 | B Điều 20; thiếu loại và gia hạn HĐ | P0 |
| PROBATION | CONTRACT_TERM | — | B Điều 24–27; Điều 25 cần bốn ngưỡng theo loại công việc | P0 |
| WAGE_AMOUNT_COMPONENTS | COMPENSATION_BENEFITS | Điều 21.1.đ (nội dung lương) | B Điều 98; N293 theo vùng/ngày, N399 từ 2027; lương và làm thêm cần tách căn cứ; BHXH/thuế là review riêng | P0 |
| BONUS_BENEFITS | COMPENSATION_BENEFITS | Điều 21.1.đ | B Điều 104; thiếu quy chế thưởng và phạm vi áp dụng | P1 |
| PAYMENT_TIMING_METHOD | COMPENSATION_BENEFITS | Điều 21.1.đ | B Điều 94–97; kỳ hạn/phương thức | P0 |
| WORKING_HOURS_OVERTIME | WORKING_TIME | Điều 21.1.g (nội dung giờ làm) | B Điều 105, 107; N145 hướng dẫn cần xét theo ngày/ca | P0 |
| REST_AND_LEAVE | LEAVE | — | B Điều 109–115; N145 hướng dẫn phép/nghỉ | P0 |
| SOCIAL_INSURANCE | INSURANCE_SAFETY | Điều 21.1.i (nội dung bảo hiểm) | Luật BHXH 41/2024/QH15 và văn bản hướng dẫn; tách BHYT/BHTN, xét N283 chỉ nếu cần | P1 |
| OSH_OBLIGATION | INSURANCE_SAFETY | Điều 21.1.i không đủ cho an toàn | Luật ATVSLĐ 2015; cần source register riêng | P1 |
| UNILATERAL_CHANGE | JOB_INFO; EMPLOYER_RIGHTS_OBLIGATIONS | Điều 21.1.c (công việc/địa điểm) | B Điều 29, 33; thiếu quy trình/giới hạn thay đổi | P0 |
| PENALTY_DEDUCTION_DAMAGES | EMPLOYEE_OBLIGATIONS_DISCIPLINE | — | B Điều 40, 101, 129; phân biệt bồi thường và khấu trừ | P0 |
| DISCIPLINE_OBLIGATION | EMPLOYEE_OBLIGATIONS_DISCIPLINE | — | B Điều 36.1.a và chương kỷ luật; xác định khoản/điểm trước nhập | P1 |
| POST_EMPLOYMENT_RESTRICTION | EMPLOYEE_OBLIGATIONS_DISCIPLINE | — | B Điều 5, 21.2; Luật SHTT và tính hợp lệ hạn chế cần review độc lập | P1 |
| DEPOSIT_DOCUMENT_HELD | WORKING_CONDITIONS; EMPLOYEE_OBLIGATIONS_DISCIPLINE | Điều 17.1–3 | Đã có ba node nhưng hiệu lực/reviewer chưa chứng minh; rà lại v1 trước mở rộng | P0 |
| DISCRIMINATION_PROTECTED_GROUPS | WORKING_CONDITIONS | — | B Điều 8, 137, 138; cần rà trường hợp được bảo vệ | P1 |
| TRAINING_COMMITMENT | TRAINING | — | B Điều 61, 62; chi phí đào tạo/hoàn trả | P1 |
| TERMINATION_GROUNDS_NOTICE | TERMINATION | — | B Điều 35, 36, 41; rủi ro theo hai vai trò | P0 |
| TERMINATION_SETTLEMENT | TERMINATION | — | B Điều 46–48 và Điều 49 nếu ca BRD cần; xác định khác biệt trợ cấp | P0 |
| WAIVER_RIGHTS_DISPUTE | OTHER | — | B Điều 5, 49.1 trong taxonomy; N2/N3 phải xác nhận 49.1 liên quan đúng hành vi, tránh citation sai | P1 |
| PERSONAL_DATA_PRIVACY | OTHER | — | Luật Bảo vệ dữ liệu cá nhân 2025/NĐ 356/2025 là ứng viên; kiểm phạm vi ngoài BLLĐ | P1 |
| CONTRACT_FORM_RULES | OTHER | Điều 14.1–2 | B Điều 14, 118–121; NĐ 337/2025 về HĐ điện tử cần kiểm điều khoản chuyển tiếp | P1 |

**Danh sách provision P0 để N2/N3 duyệt:** B Điều 20; 24–27; 29; 33; 35–36; 40–41; 46–48; 94–98; 101; 105; 107; 109–115; N293 các điều/bảng vùng liên quan, và N399 cho khoảng tương lai. Đây là **article shortlist**, không phải ước lượng số node. Các điểm v1 ở Điều 13–17/21 giữ nguyên để so sánh; muốn chấp thuận v2 phải có receipt riêng. P1 chỉ đi tiếp khi P0 đã được đối chiếu và nhu cầu Dev/annotation chứng minh. Con số “~30 điều” trong X-24 không phải chỉ tiêu nhập liệu.

**17 ngoại lệ T1:** metadata manifest cho thấy 17 role unit thuộc 5 hợp đồng, nhưng không tiết lộ nhãn chủ đề. Chúng là hàng chờ phân xử phạm vi ưu tiên của **reviewer độc lập sau khi khóa corpus v2**; người sửa corpus chỉ nhận thống kê thiếu hụt tổng hợp từ taxonomy/Dev trước khi freeze. Không xem câu chữ, nhãn hoặc dự đoán held-out để chọn P0/P1. Reviewer có thể quyết định v2 bao phủ thêm hay vẫn `CORPUS_SCOPE_EXCEPTION`, ghi nguồn và receipt; tuyệt đối không mặc định `NO_RISK` hoặc tạo Gold dương để đủ support.

## 3. Các PR nhỏ và cổng duyệt

| Thứ tự | Gói/đầu ra | Người làm và duyệt | Điều kiện xong |
| --- | --- | --- | --- |
| 1 | **Audit + scope** (tài liệu này), không đổi v1 | Data Lead; N2/N3 và chủ dự án duyệt | Đối chiếu PR #37 HEAD, xác nhận receipt v1 hoặc ghi thiếu; chốt shortlist P0, N145/TT10, N293/N399 và phạm vi ngoài BLLĐ. |
| 2 | **Source register + receipt schema**, riêng Data repo; restricted worksheet giữ ngoài Git | N2 thu nguồn; N3 và người kiểm nội dung độc lập | Mỗi candidate có official URL, `document_id`, SHA-256 bytes, ngày truy cập, trang/Điều/Khoản/Điểm, nguyên văn đối chiếu từ ảnh, lịch sử sửa đổi, `effective_from/to`, reviewer/date/decision; OCR chỉ là ứng viên. Không có dữ liệu hợp đồng riêng tư trong PR. |
| 3 | **Validator + v2 staging** riêng Pipeline, giữ v1 bất biến | N2 code; N1/N3 review | RED→GREEN cho duplicate ID, checksum, NFC/nonempty, interval overlap, parent/edge endpoint, point citation, date boundary và `INSUFFICIENT_EVIDENCE`; staging chỉ nhận item có receipt; manifest mới vẫn `DRAFT` cho đến cổng duyệt. |
| 4 | **P0 provisions** chia theo chủ đề (giao kết/thử việc; lương/giờ/nghỉ; chấm dứt), mỗi nhóm một PR | N2 soát nguồn; N3 + reviewer độc lập xác nhận pháp lý | Mỗi khoản/điểm có receipt và hiệu lực; N2/N3 ký; hash và test xanh; không sửa snapshot v1, không tự đổi runtime pin. |
| 5 | **Mapping + graph** version mới, Dev only | N2/N3; N1 review tác động | Mapping có note theo từng cạnh/nhãn; chỉ `REFERS_TO/GUIDES` đã chứng minh; M8 Graph Off/On cùng retriever/`final_k`, D1 oracle tách riêng. M3b relevance do người xem. |
| 6 | **Dev Gold + annotation unit** | N1/N2 phân xử, N3 kiểm độc lập | D2 clause-label Gold có span/hash; M1 unit thống nhất D1/D2 trước sửa segmenter; báo support từng nhãn, không gán dương theo quota. |
| 7 | **Release pin + evaluation** | Chủ dự án, N2/N3, reviewer độc lập | Khóa v2/model trên Dev, green CI/pytest/Ruff/diff, phê duyệt nguồn và rights, giữ rollback v1; reviewer held-out phân xử phạm vi T1/T2 rồi chạy **một** run mới có version/hash, báo song song baseline. Không dùng kết quả để tune tiếp. |

## 4. Ghi chú triển khai và điểm mở

- TDD §14.2 nêu node cấp khoản, điểm dài mới tách; v1 hiện có điểm Điều 21 riêng. PR validator phải hỗ trợ ID v1 trong bản cũ, và quy ước v2 rõ trước khi tạo ID mới. Không đổi ID v1 tại chỗ.
- `effective_to` v1 được README mô tả là **bao gồm**; tests phải khóa ranh giới này và kiểm khoảng liên tiếp không chồng lấn. N293/N399 cần xác minh điều thay thế trong PDF ký trước khi đặt ngày kết thúc.
- M1 Gold D1/D2/T1 đang khác độ mịn. N1/N2 cần quyết định unit, `CONTEXT` và offset rồi version Gold; không sửa Gold lịch sử. M8 D2 oracle còn thiếu Gold clause label.
- Chưa có receipt độc lập cho 16 provision v1 hoặc full sign-off pháp lý/rights trong hồ sơ đã đọc; trạng thái release thực chất **chưa chứng minh** dù loader cho `APPROVED`. Không công bố chất lượng pháp lý từ checksum, M3a hoặc M4.

**Kiểm thử tại hai checkout ngày 14/11:** bằng Python bắt buộc của Pipeline, Data full `pytest -q`: **98 passed, 3 skipped**; Pipeline full `pytest -q`: **exit 0**, focused legal corpus/Data Graph/baseline retriever: **60 passed**; Ruff `check .` đạt ở cả hai repo. `git diff --check` sẽ chạy lại trên gói đã stage trước commit. Các phép thử này kiểm tính hợp lệ kỹ thuật của mã hiện có; không kiểm nguồn luật mới, metric held-out mới hoặc sign-off con người.
