# Kết quả kiểm thử — bản cập nhật e113887 (19/10/2026)

Mọi lệnh chạy từ checkout ứng dụng tại nhánh F02, head `e113887`. SQLite local; không có MySQL/Zalo-host/production trong phiên này (xem phần "Chưa xác minh").

## Kết quả tổng hợp

| Nhóm | Lệnh | Kết quả |
| --- | --- | --- |
| Backend toàn phần (17 feature apps) | `FB_FEATURES="f01_identity,…,admin_core" DJANGO_SETTINGS_MODULE=harness.settings DJANGO_ENV=test python tests/feature-lab/manage.py test family_bridge_features.f01_identity … admin_core -v 1` | **513 tests OK, 9 skipped** (MySQL-gated race suites — skip đúng cơ chế, NOT_RUN) |
| F02 riêng | `FB_FEATURES="f02_program,admin_core,f09_activities" … test family_bridge_features.f02_program` | 45/45 PASS (gồm 9 test mới R02/R04) |
| F09 riêng | `… test family_bridge_features.f09_activities` | 21/21 PASS (gồm 8 test mới R03) |
| Migrations khớp models | `python manage.py makemigrations --check --dry-run` (harness, FB_FEATURES f02+admin_core+f09) | `No changes detected` |
| Mini App toàn phần | `cd zalo-mini-app && npm test` | **326/326 pass** (318 baseline + 8 mới) |
| Mini App regression mới | `node --test tests/companion-qa-20261019.test.mjs` | 8/8 pass ([miniapp-regressions.txt](evidence/miniapp-regressions.txt)) |
| Repro độc lập của QA (R01/R05/R06) | `F02_APP_ROOT=<checkout> node --test <docs>/f02/tools/miniapp_repro.test.mjs` | **3/3 GREEN** (RED trên c29469b) — [miniapp-repro-qa-tool.txt](evidence/miniapp-repro-qa-tool.txt) |
| Web toàn phần | `cd web && npm test` | **239/239 pass** (231 baseline + 8 mới) |
| Web regression mới | `node --test tests/f02-companion.test.mjs` | 8/8 pass ([web-regressions.txt](evidence/web-regressions.txt)) |
| Mini App build + verify | `cd zalo-mini-app && npm run build` | PASS ("Verified Zalo app-config and all referenced assets") |
| Web build | `cd web && npm run build` | PASS |
| Import boundaries (web ≠ mini) | `node scripts/check_import_boundaries.mjs` | "KHÔNG có vi phạm biên giới import" — SẠCH |

## HTTP thật trên backend chạy cục bộ (không mock)

Fixture tổng hợp đúng cách QA dùng (`f02/tools/local_fixture.py`): SQLite mới hoàn toàn, admin cấp cặp HS901/PH901 + HS903/PH903 active ngay (không bắt xác nhận ghép đôi), seed chương trình + publish nội dung, hoạt động tuần 1 có revision 1 và 2 cùng published. Backend chạy `manage.py runserver 127.0.0.1:8004` (DJANGO_ENV=development, DB_ENGINE=sqlite, FB_ZALO_LOGIN_ENABLED=false).

1. **Chạy lại toàn bộ bộ HTTP probe của QA** (`f02/tools/http_qa.py --base http://127.0.0.1:8004`): **46/46 PASS** — [http-results.json](evidence/http-recheck-results.json). Trên bản c29469b bộ này fail ở `NEW-TIMESTAMP` (R04) và `NEW-F09-UNLINK` (R03); nay cả hai PASS, không câu nào hồi quy.
2. **Kịch bản R02 tái hiện đúng FINDINGS qua HTTP thật** (script riêng, fixture mới): **15/15 PASS** — [http-r02-results.json](evidence/http-r02-repin-results.json). Điểm mấu chốt: sau khi cả hai chủ động repin rev2 (template giữ revision), propose trả **row MỚI** pin rev2 (khác agreement_id cũ), lặp propose vẫn row mới, HS confirm (chữ ký 1, vẫn proposed) → PH confirm (chữ ký 2) → confirmed; `confirmed_at` = thời điểm chữ ký hai; lịch sử giữ 2 row (rev1 superseded, rev2 confirmed); catalog `/activities/catalog` trả body typed + minutes trung thực.

## Giao diện thật (browser thật — agent-browser, không phải unit test)

Stack: backend thật 8004 + `vite preview` cho `web/dist` (3000) và Mini App preview (3004), cả hai build với `VITE_API_BASE_URL=http://127.0.0.1:8004`. Mỗi bước đều có server log xác nhận request API thật:

- WEB `#/login` HS901 → consent → chọn vai trò → `#/companion`: thấy chương trình THẬT từ catalog ("Tiếng lòng chưa nói" là title tuần 1 của nội dung seed, không phải placeholder).
- WEB bấm "Tham gia chương trình" → dialog → "Tham gia" → view đã tham gia: "Phiên bản nội dung đang theo: rev 1", chip "Hoạt động chung: [THỬ LOCAL] Tiếng lòng chưa nói…", nút "Xem chi tiết hoạt động"/"Tôi đã làm"/"Nghỉ chương trình" — [03](evidence/03-web-enrolled.png).
- WEB "Xem chi tiết hoạt động": "CÁCH LÀM:" + 4 bước từ body.steps, "Thời lượng: chưa được cung cấp trong nội dung đã phát hành…" (nguồn không có minutes — trung thực, không bịa), "không ai tick hộ ai", nút "Mời cùng làm hoạt động này" — [04](evidence/04-web-activity-detail.png).
- WEB "Tôi đã làm" → `POST /api/v1/program/progress 201` trong server log; chip chuyển "Đã làm" — [05](evidence/05-web-progress-done.png).
- MINI preview (3004) **đăng nhập cùng HS901**: thấy cùng enrollment, cùng tiến độ "Đã làm", cùng rev pin — hai client dùng chung account/API, không chia sẻ giao diện — [06](evidence/06-mini-cross-client-shared-account.png). Chi tiết hoạt động trên mini — [07](evidence/07-mini-activity-detail.png).
- MINI HS903 (chưa tham gia): nút "Xem trước hướng dẫn từng tuần" mở guide cả hai vai trò của cả 4 tuần — [01](evidence/01-mini-not-enrolled-preview-closed.png), [02](evidence/02-mini-not-enrolled-preview-open.png); nhấn tham gia vẫn là thao tác riêng tường minh.

## Chưa xác minh (không được đánh dấu PASS)

- **MySQL/TiDB:** race/concurrency suites NOT_RUN (skip gated). Khi có MySQL test, chạy `FB_TEST_DB=mysql` cho f01/f02/f09/f16 trước khi chốt.
- **Zalo thiết bị thật:** NOT_RUN — chỉ browser preview 3004 + unit test. Cần Huy mở Zalo Mini App thật để kiểm luồng zmp-sdk (silent login, share…).
- **Suy ngẫm đi F08/F15, chọn/sửa cam kết 1–3, concurrency MySQL:** giữ nguyên trạng thái gap như FINDINGS vòng trước đã ghi — không thuộc phạm vi R01–R07, không tự đánh dấu.
