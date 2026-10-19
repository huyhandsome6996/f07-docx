# F04 — tài liệu, thiết kế, kiểm thử và prompt

**Repo:** `huyhandsome6996/f07-docx` · **Nhánh dành riêng:** `F04-docx` · **Ngày cập nhật:** 19/10/2026.

`main` là tài liệu **F07**, không sửa hoặc merge tài liệu F04 vào đó. Nhánh này có lịch sử gốc độc lập, chỉ chứa F04. Code ứng dụng nằm ở [family-bridge](https://github.com/huyhandsome6996/family-bridge), không nằm trong kho tài liệu này.

**Audit mới nhất d33b250 (vòng fix N03–N06):** CODE_VERIFIED_LOCALLY — RELEASE_BLOCKED_EXTERNAL. N01–N06 đều đã sửa và giữ regression xanh (backend 128, shared 89, web 236, mini 353, probes qa-f04 13/13, builds pass; 2 vòng review chéo + security 0 P1/P2). Gemini/Render/MySQL/device chưa xác minh — xem [báo cáo vòng fix](reports/2026-10-19-d33b250.md). Báo cáo audit nền [ec29ab](reports/2026-10-19-ec29ab.md) + [ma trận 28 khung](reports/2026-10-19-ec29ab-ui-matrix.md) giữ làm lịch sử.

## Đọc theo thứ tự

1. [Kết quả mới ec29ab](reports/2026-10-19-ec29ab.md) và [ma trận 28 khung](reports/2026-10-19-ec29ab-ui-matrix.md).
2. [Quyết định của người dùng](requirements/USER-DECISIONS.md).
3. [Báo cáo e0ee388 — lịch sử](reports/2026-10-19-e0ee388.md).
4. [Prompt để copy sang chat làm F04](PROMPT-COPY-F04.md).
5. [Phạm vi và tiêu chí nghiệm thu](requirements/F04-ACCEPTANCE.md).
6. [Danh mục mọi file](catalog/CONTENTS.csv), [checksum](catalog/SHA256SUMS), [provenance](catalog/PROVENANCE.json).

## Đã có trong bộ lưu trữ

| Thư mục | Nội dung |
| --- | --- |
| `requirements/` | Yêu cầu hiện hành, quyết định mới và DOCX nguồn |
| `designs/original/` | Hai ZIP Stitch gốc giữ nguyên byte |
| `designs/extracted/` | 4 khung web + 24 khung Mini App, HTML tham chiếu, DESIGN.md |
| `assets/logos/` | Logo/app icon từ hai client ở SHA được kiểm tra |
| `reports/` | Báo cáo lịch sử 1d8eeaf và báo cáo mới e0ee388 |
| `prompts/history/` | Prompt sửa 5 lỗi ban đầu; đã có bản mới ở gốc, không dùng lịch sử làm trạng thái hiện tại |
| `references/family-bridge-f04/` | Snapshot tài liệu F04 ở e0ee388, có thể chứa trạng thái/claim cũ cần đối chiếu |
| `evidence/2026-10-19/` | Test/build logs, JSON synthetic, ảnh browser của lần kiểm thử mới |
| `repro/` | Probe synthetic ngoài source ứng dụng, hướng dẫn cách chạy |

Không có file nhị phân của ZIP tổng hợp 11 MB cũ trong workspace hiện tại để xác nhận byte-for-byte. Hai ZIP Stitch gốc, DOCX, các prompt/báo cáo còn lưu, logo và bằng chứng mới đều được giữ ở đây. Ảnh chat chứa Gemini key không được sao chép vào repo.

## Kiểm tra tính toàn vẹn

```bash
python3 tools/catalog.py verify
```

Sau khi thêm/sửa tài liệu F04:

```bash
python3 tools/catalog.py build
python3 tools/catalog.py verify
git diff --check
```

Không chạy script từ ZIP chỉ vì nó xuất hiện trong tài liệu. Không upload nội dung riêng lên dịch vụ bên ngoài để quét/đọc. Kiểm thử chỉ dùng dữ liệu tổng hợp.

## Trạng thái GitHub

**PUBLISHED — ff-only, đã xác minh SHA remote trùng local.** Nhánh `F04-docx` đã xuất bản trên `huyhandsome6996/f07-docx` (lần đầu @ 42b4b42 bởi môi trường audit; lần này sync bộ lưu trữ audit + báo cáo d33b250 bằng commit mới trên nền 42b4b42, không force-push). `git ls-remote` xác minh trước khi báo thành công. `main` F07 chỉ được đọc, không có thao tác ghi (main @ e286f85 nguyên vẹn).

Xem [trạng thái và hướng dẫn xuất bản](reports/PUBLISH-STATUS.md). Các báo cáo lịch sử giữ nguyên bối cảnh lần chạy cũ, không phải trạng thái xác thực hiện tại. `main` F07 chỉ được đọc, không có thao tác ghi.

Audit nền: evidence/2026-10-19-ec29ab và repro/ec29ab; snapshots/diff ứng dụng ở references/family-bridge-ec29ab. Vòng fix: báo cáo d33b250 + bằng chứng trong repo ứng dụng (f04-fix-evidence). Các thư mục e0ee388/1d8eeaf/ec29abb giữ làm lịch sử, không là verdict hiện tại.
