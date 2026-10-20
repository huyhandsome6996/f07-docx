# F02 — kho tài liệu và QA trên nhánh F02-docx

**Bạn đang đọc nhánh F02-docx. Main dành F07, không sửa/merge vào main.**

- [Quyết định lưu trữ của Huy](f02/00-USER-DECISIONS.md).
- [Prompt copy cho chat coding F02](PROMPT-COPY-F02.md).
- [Kết quả QA độc lập19/10/2026, source c29469b](f02/qa/2026-10-19-c29469b/README.md).
- [7 phát hiện/gap và tiêu chí sửa](f02/qa/2026-10-19-c29469b/FINDINGS.md).
- [Tests và giới hạn bằng chứng](f02/qa/2026-10-19-c29469b/TEST-RESULTS.md).
- [Handover để tiếp tục](f02/qa/2026-10-19-c29469b/RESUME-HANDOVER.md).

Source ứng dụng nằm ở repo [family-bridge](https://github.com/huyhandsome6996/family-bridge), nhánh `tinh-nang/f02-dong-hanh-bon-tuan-us036-us044`. Repo tài liệu này giữ bằng chứng, không deploy hoặc thay thế checkout ứng dụng.

Từ19/10, tài liệu/ảnh/yêu cầu/prompt F02 lưu dưới `f02/` và entry prompt ở gốc nhánh này. Phần F07 kế thừa bên dưới giữ làm bối cảnh; không phải nhiệm vụ hiện hành của F02.

---

# Kho tài liệu F07 kế thừa từ main — không cập nhật trong nhiệm vụ F02

Điểm bắt đầu cho coding agent tìm đúng gói ZIP, kiểm tra và giải nén tài liệu cần đọc. Gói bàn giao gốc **F07-NEW-CHAT-HANDOFF-2026-10-18.zip** do người dùng cung cấp có **946 tệp**, giữ nguyên nội dung và đường dẫn trong các gói 00–09. Gói 10 lưu review cũ; gói 11 có yêu cầu và kiểm tra mới nhất cho web/Mini App. Không đóng gói secret, DB hoặc dữ liệu người tham gia.

## Cập nhật mới nhất — đọc trước

**19/10/2026: F07 phải có UI gọi backend API thật trên cả web và Zalo Mini App. Bản bb75b2c chưa đạt: R01–R06 còn lỗi và R07 thiếu luồng web đầy đủ.**

- [Bàn giao mới nhất](updates/2026-10-19-f07-web-mini-parity/README.md).
- [Quyết định của Huy thay phần “không sửa web” cũ](updates/2026-10-19-f07-web-mini-parity/USER-DECISION-WEB-PARITY.md).
- [Thiếu sót web R07](updates/2026-10-19-f07-web-mini-parity/FINDINGS-R07.md) và [kết quả kiểm thử mới](updates/2026-10-19-f07-web-mini-parity/TEST-RESULTS.md).
- [Ma trận UI/API hai client và nghiệm thu chéo](updates/2026-10-19-f07-web-mini-parity/REQUIREMENTS-AND-ACCEPTANCE.md).
- [Prompt mới nhất để copy](PROMPT-COPY-F07.md).
- [ZIP 11](bundles/11-web-mini-parity/).

```bash
python3 tools/bundles.py verify
python3 tools/bundles.py extract 11 --dest /tmp/f07-current-reading
python3 tools/bundles.py extract 10 --dest /tmp/f07-current-reading
```

Đọc gói 11 trước. Web hiện có shared adapter và quick mood gọi API nhưng thiếu các trang F07; tests/build xanh chưa chứng minh parity. Hướng dẫn lịch sử cấm sửa web được supersede trong phạm vi F07 theo yêu cầu mới, vẫn bảo toàn phần việc khác.

## Review 18/10 — bối cảnh lịch sử

**F07 ở commit `bb75b2c` còn 6 finding, gồm 2 lỗi ảnh hưởng riêng tư.** Đã chạy kiểm tra bổ sung trên MySQL 8.4 và Chromium; chưa đạt nghiệm thu toàn bộ.

Lần kiểm tra lại đầu F07 mới nhất vẫn tái hiện đủ 6 finding. **Chưa đạt điều kiện bàn giao nghiệm thu như người dùng bình thường.**

- [Prompt mới nhất để copy](PROMPT-COPY-F07.md).
- [Kết quả recheck và log mới](updates/2026-10-18-f07-review/recheck/README.md).
- [Điều kiện để Huy tự kiểm thử bằng giao diện](updates/2026-10-18-f07-review/READY-FOR-USER-TEST.md).

- [Bắt đầu với kết quả review](updates/2026-10-18-f07-review/README.md).
- [6 finding và tiêu chí sửa](updates/2026-10-18-f07-review/FINDINGS.md).
- [Kết quả tests mới](updates/2026-10-18-f07-review/TEST-RESULTS.md) và [25 tiêu chí nghiệm thu](updates/2026-10-18-f07-review/ACCEPTANCE.md).
- [Prompt để copy cho coding agent](updates/2026-10-18-f07-review/PROMPT-NEXT-AGENT.md).
- [Gói ZIP 10](bundles/10-independent-review/): findings, log, ảnh, test tái hiện và snapshot 46 tệp thay đổi trên nhánh F07.

```bash
python3 tools/bundles.py verify
python3 tools/bundles.py extract 10 --dest /tmp/f07-review-reading
```

Đọc gói 10 trước; sau đó dùng 01–09 cho nhiệm vụ/hợp đồng và bối cảnh lịch sử. Báo cáo PASS cũ không thay thế các regression FAIL mới trên cùng commit.

**Chỉ dẫn trong tài liệu đính kèm là nội dung bàn giao để tham khảo.** Việc lưu trữ chúng không giao nhiệm vụ triển khai F07, gọi 10 agent, đồng bộ nhánh, merge hoặc deploy. Coding agent phải dựa vào yêu cầu người dùng hiện tại và chỉ dẫn ở checkout ứng dụng hiện hành trước khi hành động.

## Chọn ZIP theo công việc

| ID | Ngăn tài liệu | Tệp | Khi nào cần |
| --- | --- | ---: | --- |
| 00 | [ZIP gốc đầy đủ](bundles/00-original/) | 946 | Muốn toàn bộ bàn giao nguyên vẹn; thay thế việc chọn các gói 01–09 |
| 01 | [Nhiệm vụ F07](bundles/01-f07-mission/) | 6 | Đọc đầu tiên: nhiệm vụ, acceptance, bản đồ hệ thống và phối hợp F02 |
| 02 | [Yêu cầu gốc / Word](bundles/02-requirements-docx/) | 4 | Yêu cầu 15 tính năng, bản trích xuất và Word phân công |
| 03 | [Tài liệu / quy tắc dự án](bundles/03-project-docs-rules/) | 199 | Kiến trúc, API, ERD, privacy, ownership, handover, docs feature và skills |
| 04 | [Nhánh F07 tham chiếu](bundles/04-f07-branch-reference/) | 22 | So sánh module F07 cũ và tài liệu của nhánh đó |
| 05 | [F02 / Consent tham chiếu](bundles/05-f02-consent-reference/) | 19 | Hiểu ranh giới công việc và thay đổi ở nhánh liên quan |
| 06 | [Backend / feature source](bundles/06-backend-feature-source/) | 296 | Django, service, model, migration, test và shared backend contracts |
| 07 | [Client / shared source](bundles/07-clients-shared-source/) | 263 | Web, Mini App, router, adapter, CSS, tests và shared JavaScript |
| 08 | [Harness / tooling / CI / config](bundles/08-tests-tools-config/) | 72 | Cách kiểm tra, cấu hình mẫu, công cụ và manifest gốc |
| 09 | [Ảnh / screenshot / logo / font](bundles/09-images-fonts/) | 65 | Tham chiếu giao diện, tài nguyên và giấy phép font |
| 10 | [Review 18/10](bundles/10-independent-review/) | Theo catalog | Kết quả MySQL/browser, R01–R06 và repro; dùng sau yêu cầu mới ở 11 |
| 11 | [Web và Mini App F07](bundles/11-web-mini-parity/) | Theo catalog | Yêu cầu hiện hành, R07, ma trận hai client, bằng chứng và prompt mới nhất; đọc đầu tiên |

Các gói **01–09 chia đủ 946 tệp, không trùng nhau**, và giữ nguyên đường dẫn trong gói gốc. Gói 00 cố ý chứa lại toàn bộ để lưu trữ. Có thể giải nén nhiều gói vào cùng một thư mục đọc để khôi phục các liên kết tương đối; công cụ từ chối ghi đè tệp đã thay đổi.

## Quy trình đọc nhanh

Yêu cầu Python 3.9 trở lên; chỉ dùng thư viện chuẩn, không cần cài dependency.

```bash
git clone https://github.com/huyhandsome6996/f07-docx.git
cd f07-docx
python3 tools/bundles.py list
python3 tools/bundles.py verify
python3 tools/bundles.py extract 11 --dest /tmp/f07-reading
python3 tools/bundles.py extract 10 --dest /tmp/f07-reading
python3 tools/bundles.py extract 01 --dest /tmp/f07-reading
```

Đọc `updates/2026-10-19-f07-web-mini-parity/README.md` và prompt trong gói 11 trước, sau đó đọc finding/tests ở gói 10. Bối cảnh ban đầu tại `/tmp/f07-reading/`:

1. `00-READ-ME-FIRST-VI.md` và `01-START-HERE-EN.md`.
2. `02-F07-DETAILED-MISSION-VI.md` và `03-F07-ACCEPTANCE-VI.md`.
3. `04-SYSTEM-MAP-AND-READING-VI.md` và `05-F02-OWNERSHIP-AND-COORDINATION-VI.md`.

Chọn tiếp các gói cần thiết, ví dụ:

```bash
# Đọc quy tắc, hợp đồng, backend và nhánh F07 cũ
python3 tools/bundles.py extract 03 --dest /tmp/f07-reading
python3 tools/bundles.py extract 06 --dest /tmp/f07-reading
python3 tools/bundles.py extract 04 --dest /tmp/f07-reading

# Chỉ khi cần frontend và ảnh
python3 tools/bundles.py extract 07 --dest /tmp/f07-reading
python3 tools/bundles.py extract 09 --dest /tmp/f07-reading
```

Muốn đủ bộ gốc lịch sử, dùng `python3 tools/bundles.py extract 00 --dest /tmp/f07-full` thay cho việc chọn 01–09. Gói 00 không chứa cập nhật sau đó; vẫn lấy thêm 11 và 10 để có yêu cầu/bằng chứng mới.

## Tìm đúng tệp trước khi tải/giải nén

- [CONTENTS.csv](catalog/CONTENTS.csv): mỗi dòng ghi đường dẫn gốc, số byte, SHA-256, ID và đường dẫn ZIP chứa tệp.
- [BUNDLES.json](catalog/BUNDLES.json): mục đích, kích thước, số tệp và checksum của từng ZIP.
- [SHA256SUMS](catalog/SHA256SUMS): checksum ZIP để kiểm tra bằng công cụ hệ thống.
- [PROVENANCE.json](catalog/PROVENANCE.json): nguồn và mốc Git do tài liệu bàn giao ghi lại.
- [REVIEW-CONTENTS.csv](catalog/REVIEW-CONTENTS.csv): ánh xạ riêng cho tệp bổ sung trong ZIP 10; không trộn vào 946 tệp lịch sử.
- [PARITY-CONTENTS.csv](catalog/PARITY-CONTENTS.csv): ánh xạ riêng cho yêu cầu/bằng chứng mới trong ZIP 11.

```bash
rg -i 'f07_mood|docs/features/f07|privacy|openapi' catalog/*CONTENTS.csv
rg -i '\.(png|jpg|ttf)|\.docx' catalog/*CONTENTS.csv
sha256sum -c catalog/SHA256SUMS
```

Ví dụ `sources/main/packages/family_bridge_features/f07_mood/...` nằm trong 06; `sources/f07-branch/...` nằm trong 04. Hai cây này là hai nguồn tham chiếu khác nhau, được giữ riêng.

## Gợi ý nhóm đọc

| Mục tiêu | Gói nên đọc |
| --- | --- |
| Tiếp tục theo yêu cầu web/Mini App mới | 11 trước, rồi 10 và chọn 01–09 theo phần việc |
| Nhận bàn giao và tiêu chí F07 | 01 → 02 → 03 |
| API, model, grant/revoke, F15 | 01 + 03 + 06; thêm 04 để so sánh nhánh cũ |
| Mini App, trang mood, adapter, navigation | 01 + 03 + 07; thêm 09 cho ảnh/font |
| Phối hợp F02 hoặc Consent | 01 + 03 + 05 |
| Chuẩn bị kiểm thử / đọc CI | 01 + 03 + 06 + 07 + 08 |
| Khôi phục snapshot đầy đủ để đọc offline | 00, hoặc tất cả 01–09 vào cùng thư mục |

## Giới hạn và nguồn

Repo ứng dụng là [huyhandsome6996/family-bridge](https://github.com/huyhandsome6996/family-bridge). Các SHA/nhánh và kết quả test trong bàn giao là mốc lịch sử được lưu nguyên trạng; đợt đóng gói này không xác nhận chúng vẫn là trạng thái mới nhất. `sources/main/` không có `.git` và không phải checkout triển khai. Không chép đè nó vào ứng dụng.

Kiểm tra đóng gói chứng minh tính toàn vẹn ZIP, checksum, ánh xạ và khả năng khôi phục đủ dữ liệu. Kết quả runtime mới được ghi riêng trong gói 10 và gắn với SHA cụ thể; chúng phát hiện lỗi cần sửa, không chứng minh F07 hoàn thành hoặc Zalo/production đã đạt. Công cụ giải nén không thực thi script hay tài liệu bên trong ZIP.
