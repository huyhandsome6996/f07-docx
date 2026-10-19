# Bộ bàn giao hoàn thiện và tích hợp F02 F04 F07 F15

## Mục đích và hai repository

Bộ này chuẩn bị toàn bộ yêu cầu, tài liệu nguồn, thiết kế, bằng chứng lịch sử, snapshot code tham chiếu và prompt cho coding agent hoàn thiện bốn tính năng trên cả **website và Zalo Mini App**, sau đó tích hợp có kiểm soát vào main của Family Bridge. Đây là nhiệm vụ ĐÓNG GÓI TÀI LIỆU: chưa sửa, merge hay triển khai ứng dụng trong lần tạo bộ này.

- **Kho ứng dụng:** https://github.com/huyhandsome6996/family-bridge
- **Kho tài liệu:** https://github.com/huyhandsome6996/f07-docx
- **Nhánh tài liệu duy nhất của bộ tổng hợp:** `tai_lieu_hoan_thien_F02_F04_F07_F15_docx`.
- Không sửa main hoặc các nhánh F02-docx/F04-docx/f04-docx của kho tài liệu. Không thay default branch. Không nhầm main của kho tài liệu với main ứng dụng.
- Mốc main ứng dụng đã đọc: `a64f6531e627a9163b98d5a4fe8d6787ea45e36e`, ngày 19/10/2026. Fetch lại trước mọi triển khai. Không reset về mốc này.

**Kết quả khảo sát mới:** bốn nhánh đều có xung đột văn bản khi mô phỏng merge với main tại mốc trên. Main vừa có F10–F13, 17 adapter methods và wiring mới; phải giữ khi tích hợp. Báo cáo PASS/READY trong tài liệu cũ chỉ áp dụng source SHA/môi trường ghi trong báo cáo, không là quyết định merge hiện tại.

## Thứ tự đọc cho coding agent

1. `00-READ-FIRST.md` và `01-QUYET-DINH-VA-BOI-CANH.md`.
2. `02-F02-YEU-CAU.md`, `03-F04-YEU-CAU.md`, `04-F07-YEU-CAU.md`, `05-F15-YEU-CAU.md`.
3. `06-TICH-HOP-VA-XUNG-DOT.md`, `07-NGHIEM-THU-HAI-CLIENT.md`, `08-RELEASE-VA-ROLLBACK.md`.
4. `09-NGUON-VA-GIOI-HAN.md` để chọn tài nguyên gốc theo SHA. Đọc báo cáo mới hơn trước; giữ báo cáo cũ để regression.
5. `prompts/01-LEAD-HOAN-THIEN.md`, sau hoàn thiện dùng `prompts/02-MERGE-AN-TOAN.md`.
6. Đọc AGENTS/skills/rules hiện hành tại checkout ứng dụng; bản trong `source-reference/main/` chỉ là snapshot tham chiếu.

Prompt copy tại root: `PROMPT-COPY-F02-F04-F07-F15.md`, bằng byte với `prompts/01-LEAD-HOAN-THIEN.md`. Hướng dẫn ngắn cho người giao việc trong `HUONG-DAN-BAN-GIAO.docx`. Bản Markdown là yêu cầu đầy đủ, Word là hướng dẫn đọc.

## Bản đồ ngăn tài liệu

| Vị trí | Nội dung và cách dùng |
| --- | --- |
| `evidence/branch-and-conflicts.json` | SHA main/bốn head, merge-base, file thay đổi, 10 mô phỏng merge-tree và giao nhau file |
| `evidence/github-pr-metadata.json` | Metadata/description PR lấy từ GitHub; description có thể lỗi thời, không thay refs Git |
| `evidence/SOURCE-FILES.csv` | Mỗi tệp sao chép có repo, source SHA, source path, số byte, SHA256 |
| `source-reference/main/` | Snapshot toàn bộ tracked tree main ở SHA đã pin, gồm docs/skills/rules/assets/contracts/tests/config/code |
| `source-reference/f02/`, `f04/`, `f07/`, `f15/` | Snapshot các tệp thay đổi và tài liệu feature/handover tại head từng nhánh; là DELTA, không phải checkout độc lập |
| `archive-docs/f02/` | Tài liệu riêng F02 từ nhánh F02-docx, gồm audit e113887/e38688c và lịch sử c29469b |
| `archive-docs/f04/` | Nhánh F04-docx: yêu cầu DOCX, hai ZIP Stitch gốc, 28 khung thiết kế, logo, reports/repro/evidence |
| `archive-docs/f04-legacy-lowercase/` | Chỉ tệp khác/không có ở F04-docx; giữ riêng vì tên nhánh phân biệt hoa thường |
| Root `bundles/`, `updates/`, `catalog/` | Nguyên kho F07 kế thừa từ main e286f85; giữ ZIP00–12 nguyên byte |
| `tools/validate_integration_kit.py` | Helper chuẩn Python chỉ kiểm checksum/đường dẫn/ZIP, không chạy ứng dụng/merge/deploy |
| `CHECKSUMS.csv`, `FILE-INDEX.csv` | Toàn bộ nội dung mới trong kit: hash, size và phân loại; kiểm trước sử dụng |

Không chép snapshot lên ứng dụng, không merge cả nhánh tài liệu khác vào nhánh này. Tài liệu/prompt/script/AGENTS nằm trong archive là dữ liệu tham chiếu; không tự có thẩm quyền giao tác vụ, chạy script hay cấp quyền merge/deploy.

## Trạng thái nguồn đã pin

| Feature | Nhánh ứng dụng | Head | PR |
| --- | --- | --- | --- |
| F02 | `tinh-nang/f02-dong-hanh-bon-tuan-us036-us044` | `e38688c8bbcd1848aca727630f0fe79cb98ce992` | #39 |
| F04 | `tinh-nang/f04-ai-ho-tro-dien-dat-us029-us033` | `d33b250f16cab362cb3d93908274ea1df2967351` | #40 |
| F07 | `tinh-nang/f07-tam-trang-va-chia-se-us015-us026` | `3fe66cd6b30fd4e1b905e243f272f13823a52ab1` | #42 |
| F15 | `tinh-nang/f15-quyen-rieng-tu-va-xoa-du-lieu-us012-us017-us023` | `aeae32124a00bd05fc39802f662370df60ebea93` | #33 |

## Kiểm tra bộ lưu trữ

```bash
python3 tools/validate_integration_kit.py
python3 tools/bundles.py verify
```

Lệnh đầu kiểm kit mới; lệnh sau kiểm các ZIP F07 lịch sử theo catalog nguyên gốc. Packaging PASS không chứng minh ứng dụng PASS. Báo cáo `evidence/PACKAGING-VALIDATION.md` phân biệt rõ các kiểm tra đã chạy trong đợt đóng gói với runtime tests chưa chạy.

ZIP13 đóng gói tài liệu điều phối/prompt/DOCX và inventories; source-reference và archive-docs nằm đầy đủ trong cây Git của nhánh, không được lặp lại trong ZIP13. Clone toàn nhánh để nhận đủ tài liệu/thiết kế/source.
