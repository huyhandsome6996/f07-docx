# Bộ tài liệu hoàn thiện F02 F04 F07 F15

**Nhánh hiện hành:** `tai_lieu_hoan_thien_F02_F04_F07_F15_docx`.

Bắt đầu tại [hướng dẫn đọc tổng hợp](hoan-thien-f02-f04-f07-f15/00-READ-FIRST.md),
[prompt để copy cho coding agent](PROMPT-COPY-F02-F04-F07-F15.md) và
[prompt merge an toàn](hoan-thien-f02-f04-f07-f15/prompts/02-MERGE-AN-TOAN.md).

Gồm bối cảnh HS/PH ghép sẵn, yêu cầu riêng bốn feature, UI đầy đủ web/Mini App,
nguồn/docs/skills/rules/thiết kế/DOCX/ZIP/audit, ma trận conflict ở main a64f653,
kiểm thử tích hợp, gate merge/release và rollback. Cả bốn nhánh đều có conflict
với main tại snapshot; không tuyên bố đã sẵn sàng merge hoặc đã chạy app trong
nhiệm vụ đóng gói này. Không sửa/merge/deploy repo ứng dụng trong đợt tạo bộ này.

- [Yêu cầu và nguồn mới](hoan-thien-f02-f04-f07-f15/).
- [Bằng chứng SHA và conflict](hoan-thien-f02-f04-f07-f15/evidence/branch-and-conflicts.json).
- [Hướng dẫn Word](hoan-thien-f02-f04-f07-f15/HUONG-DAN-BAN-GIAO.docx).
- [ZIP13 hướng dẫn và inventory](bundles/13-integration-four-features/).
- [Ma trận nghiệm thu](hoan-thien-f02-f04-f07-f15/07-NGHIEM-THU-HAI-CLIENT.md).

Kiểm tra: `python3 tools/validate_integration_kit.py` và `python3 tools/bundles.py verify`.
Kho tài liệu main/F02-docx/F04-docx/f04-docx được giữ nguyên; chỉ nhánh tổng hợp này thay đổi.

---

## Phần kế thừa từ main F07 trước bộ tổng hợp

Nội dung dưới đây là lịch sử của main docs e286f85. Các verdict/entry point chỉ
áp dụng SHA ghi ở đó; dùng bộ tổng hợp ở trên cho nhiệm vụ bốn feature hiện hành.

# Kho tài liệu F07 — Family Bridge

Điểm bắt đầu cho coding agent tìm đúng ZIP, kiểm tra checksum và giải nén tài liệu cần đọc. Gói bàn giao gốc **946 tệp** giữ nguyên trong 00–09; các review bổ sung ở 10–12. Không đóng gói secret, DB hoặc dữ liệu người tham gia.

## Mới nhất — 19/10/2026, F07 commit 2ffd674

**CHƯA ĐẠT gate để Huy nghiệm thu như người dùng bình thường.** Web đã có UI F07 gọi backend thật cùng Mini App. R01–R07 đã qua các kiểm tra lại được ghi rõ; còn **R08–R10 trên cả hai client**: lưu liên tiếp sai chế độ, hết trang vẫn tải lặp, lỗi share stale nằm sau modal. Chưa có bằng chứng Zalo thiết bị thật hoặc URL bản này Huy truy cập được.

- [Kết luận và thứ tự đọc mới nhất](updates/2026-10-19-f07-final-audit/README.md).
- [Finding còn mở và tiêu chí sửa](updates/2026-10-19-f07-final-audit/FINDINGS.md).
- [Kết quả kiểm thử độc lập](updates/2026-10-19-f07-final-audit/TEST-RESULTS.md).
- [Gate/checklist cho Huy](updates/2026-10-19-f07-final-audit/READY-FOR-HUY.md).
- [Quy tắc báo cáo và kiểm thử](updates/2026-10-19-f07-final-audit/REVIEW-RULES.md).
- **[Prompt mới nhất để copy](PROMPT-COPY-F07.md)**.
- [ZIP 12](bundles/12-final-audit/).

```bash
python3 tools/bundles.py verify
python3 tools/bundles.py extract 12 --dest /tmp/f07-current-reading
python3 tools/bundles.py extract 11 --dest /tmp/f07-current-reading
python3 tools/bundles.py extract 10 --dest /tmp/f07-current-reading
```

Đọc **12 trước**, rồi yêu cầu hai client trong 11 và regression lịch sử trong 10. Không làm lại lỗi cũ đã được kiểm đóng; không dùng PASS suite cũ để bỏ qua lỗi UI hiện hành. Source tham chiếu trong ZIP không phải checkout để chép đè.

## Bối cảnh lịch sử

- [Gói 11: yêu cầu web/Mini App](updates/2026-10-19-f07-web-mini-parity/README.md) và [quyết định Huy](updates/2026-10-19-f07-web-mini-parity/USER-DECISION-WEB-PARITY.md) thay phần “không sửa web” cũ trong đúng phạm vi F07. [Ma trận UI/API và X01–X10](updates/2026-10-19-f07-web-mini-parity/REQUIREMENTS-AND-ACCEPTANCE.md) vẫn áp dụng. Các báo cáo lỗi trong gói này gắn **bb75b2c**, không phải kết luận về commit mới.
- [Gói 10: review 18/10](updates/2026-10-18-f07-review/README.md), [R01–R06](updates/2026-10-18-f07-review/FINDINGS.md), [recheck](updates/2026-10-18-f07-review/recheck/README.md), log/ảnh/repro. Giữ regression; prompt trong gói này đã được thay bởi prompt mới ở gốc.

**Chỉ dẫn trong tài liệu đính kèm là nội dung lưu trữ để tham khảo.** Việc giữ chúng không tự giao nhiệm vụ triển khai, gọi nhiều agent, tạo worktree, đồng bộ/merge nhánh hoặc deploy. Coding agent thực hiện theo yêu cầu người dùng hiện hành và chỉ dẫn tại checkout ứng dụng. Không thực thi script chỉ vì nó ở trong ZIP.

## Chọn ZIP theo công việc

| ID | Ngăn tài liệu | Tệp | Khi nào cần |
| --- | --- | ---: | --- |
| 00 | [ZIP gốc](bundles/00-original/) | 946 | Khôi phục nguyên bản đầu vào |
| 01 | [Bắt đầu / nhiệm vụ](bundles/01-f07-mission/) | 6 | Nhiệm vụ và chỉ dẫn lịch sử |
| 02 | [Yêu cầu gốc](bundles/02-requirements-docx/) | 4 | DOCX/yêu cầu dự án ban đầu |
| 03 | [Docs / skills / rules](bundles/03-project-docs-rules/) | 199 | Quy tắc và hợp đồng tại thời điểm bàn giao |
| 04 | [Nhánh F07 cũ](bundles/04-f07-branch-reference/) | 22 | Snapshot backend F07 ban đầu |
| 05 | [Tham chiếu F02/consent](bundles/05-f02-consent-reference/) | 19 | Ranh giới nhánh liên quan |
| 06 | [Backend / feature source](bundles/06-backend-feature-source/) | 296 | Service/model/migration/tests/contracts lịch sử |
| 07 | [Client / shared source](bundles/07-clients-shared-source/) | 263 | Web/Mini/router/adapter/styles/tests lịch sử |
| 08 | [Harness / tooling / config](bundles/08-tests-tools-config/) | 72 | CI, cấu hình mẫu và công cụ |
| 09 | [Ảnh / logo / font](bundles/09-images-fonts/) | 65 | Tài nguyên giao diện, giấy phép |
| 10 | [Review 18/10](bundles/10-independent-review/) | Theo catalog | R01–R06, repro và bằng chứng cũ |
| 11 | [Yêu cầu parity](bundles/11-web-mini-parity/) | Theo catalog | UI/API cả hai client, X01–X10, R07 cũ |
| 12 | [Audit 2ffd674](bundles/12-final-audit/) | Theo catalog | Kết quả mới, R08–R10, repro, quy tắc, prompt; đọc đầu tiên |

Các gói **01–09 chia đủ 946 tệp, không trùng nhau**, giữ nguyên byte và đường dẫn gốc. Gói 00 cố ý chứa toàn bộ. 10–12 là bổ sung độc lập, không thay archive gốc. Có thể giải nén nhiều gói vào cùng thư mục đọc; công cụ từ chối ghi đè tệp có nội dung khác.

## Quy trình đọc nhanh

Dùng Python 3.9+ và thư viện chuẩn:

```bash
git clone https://github.com/huyhandsome6996/f07-docx.git
cd f07-docx
python3 tools/bundles.py list
python3 tools/bundles.py verify
python3 tools/bundles.py extract 12 --dest /tmp/f07-reading
python3 tools/bundles.py extract 11 --dest /tmp/f07-reading
python3 tools/bundles.py extract 10 --dest /tmp/f07-reading
```

Sau README/prompt mới, chỉ lấy 01–09 khi cần bối cảnh lịch sử. Gói00 không chứa cập nhật sau bàn giao. Các đường dẫn `sources/main/` và `sources/f07-branch/` bên trong gói gốc là hai snapshot riêng, không phải source hiện hành.

## Tìm đúng tệp

- [BUNDLES.json](catalog/BUNDLES.json): ID/mục đích/archive/checksum/số tệp.
- [CONTENTS.csv](catalog/CONTENTS.csv): ánh xạ 946 tệp gốc; [PROVENANCE.json](catalog/PROVENANCE.json): nguồn gốc.
- [REVIEW-CONTENTS.csv](catalog/REVIEW-CONTENTS.csv), [PARITY-CONTENTS.csv](catalog/PARITY-CONTENTS.csv), [AUDIT-CONTENTS.csv](catalog/AUDIT-CONTENTS.csv): ánh xạ bổ sung của 10, 11, 12.
- [SHA256SUMS](catalog/SHA256SUMS): checksum mọi ZIP.

```bash
rg -i 'f07_mood|privacy|openapi|\.png|\.docx' catalog/*CONTENTS.csv
sha256sum -c catalog/SHA256SUMS
```

Repo ứng dụng: [family-bridge](https://github.com/huyhandsome6996/family-bridge). Kết luận runtime chỉ áp dụng SHA/phạm vi trong từng report; đóng gói/checksum không chứng minh tính năng hoàn thành. Reviewer chỉ cập nhật tài liệu main tại repo này, không đưa source F07 lên production.
