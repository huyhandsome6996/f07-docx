# Bàn giao — tiếp tục công việc F02 sau bản cập nhật e113887

## Trạng thái nhánh

- **Ứng dụng:** [family-bridge](https://github.com/huyhandsome6996/family-bridge) nhánh `tinh-nang/f02-dong-hanh-bon-tuan-us036-us044`, head **e113887** (cha là `c29469b3…` — bản đã QA). Bốn commit: `ba244da` (backend R02/R03/R04 + R06 backend), `85ab7d1` (mini R01/R05/R06), `652e29d` (web R07), `e113887` (đính chính checklist `docs/handover/f02-qa/06-RESUME-HANDOVER.md` — propose không tính là chữ ký). Đã push; KHÔNG đụng main; KHÔNG force push; KHÔNG deploy.
- **Tài liệu:** [f07-docx](https://github.com/huyhandsome6996/f07-docx) nhánh `F02-docx` — vòng QA cũ `f02/qa/2026-10-19-c29469b/` giữ nguyên từng byte; bản cập nhật này `f02/qa/2026-10-19-e113887/` (có liên kết hai chiều qua README). Checksums trong `f02/SHA256SUMS` có thêm phần "2026-10-19-e113887".

## Chạy lại môi trường local để tự kiểm (đúng như bản cập nhật này đã chạy)

```bash
# 0) checkout nhánh F02 head e113887 (không db.sqlite3, không backend/.env)
git clone https://github.com/huyhandsome6996/family-bridge && cd family-bridge
git checkout tinh-nang/f02-dong-hanh-bon-tuan-us036-us044

# 1) fixture tổng hợp (từ kho tài liệu F02-docx, tools của QA)
export F02_QA_PASSWORD="<mật khẩu tổng hợp >=12 ký tự, chỉ local>"
python <f07-docx-checkout>/f02/tools/local_fixture.py --app-root .

# 2) backend thật
( cd backend && DJANGO_ENV=development DB_ENGINE=sqlite FB_ZALO_LOGIN_ENABLED=false \
  CORS_ALLOWED_ORIGINS="http://127.0.0.1:3000,http://127.0.0.1:3004" \
  python manage.py runserver 127.0.0.1:8004 )

# 3) hai giao diện (build trỏ về backend local)
( cd web && VITE_API_BASE_URL=http://127.0.0.1:8004 npx vite build && npx vite preview --port 3000 )
( cd zalo-mini-app && VITE_API_BASE_URL=http://127.0.0.1:8004 npx vite build && npx vite preview --port 3004 )

# 4) chạy lại bộ HTTP probe của QA (phải 46/46)
python <f07-docx-checkout>/f02/tools/http_qa.py --base http://127.0.0.1:8004 --out /tmp/qa-recheck.json
```

Tài khoản fixture: `HS901`/`PH901`, `HS903`/`PH903` + `F02_QA_PASSWORD`. Admin cấp cặp → kết nối active ngay (không cần xác nhận ghép đôi).

## Checklist nhanh (trang → thao tác → PASS)

| Trang | Thao tác | PASS khi |
| --- | --- | --- |
| WEB `#/login` | Đăng nhập `HS901` + mật khẩu fixture | Vào app, không lỗi cấu hình |
| WEB `#/companion` (chưa tham gia) | "Xem trước hướng dẫn từng tuần" | Guide cả 2 vai trò của cả 4 tuần hiện ra; KHÔNG có request enroll trong network |
| WEB `#/companion` | "Tham gia chương trình" → dialog → "Tham gia" | View đã tham gia: "Phiên bản nội dung đang theo: rev N", 4 tuần đều mở (không "Sắp có") |
| WEB `#/companion` | "Xem chi tiết hoạt động" | Mục tiêu/Cách làm (steps)/thời lượng có nguồn hoặc "chưa được cung cấp" (không có "khoảng 1 phút" bịa) |
| WEB `#/companion` | "Mời cùng làm hoạt động này" (cần PH đã kết nối) | Lời mời gửi đi với revision = bản published MỚI NHẤT (không phải bản cũ) |
| WEB `#/companion` | "Tôi đã làm" | Chip "Đã làm"; server log `POST /program/progress 201` |
| MINI preview 3004, cùng HS901 | Mở `#/companion` | Thấy CÙNG enrollment + tiến độ đã tạo trên WEB (chung account/API) |
| MINI HS903 (chưa tham gia) | "Xem trước hướng dẫn từng tuần" | Như WEB, không POST enroll (R05) |
| Hai tài khoản, thỏa ước | HS "Đề xuất" → HS "Tôi xác nhận thỏa ước này" → PH "Xác nhận thỏa ước" | Sau HS confirm VẪN "Chờ hai bên xác nhận"; chỉ sau PH confirm mới "Đã cùng xác nhận"; `confirmed_at` = thời điểm chữ ký 2 (R04 + checklist đã đính chính) |
| API (unlink) | HS revoke connection → PH accept lời mời cũ | `400 no_active_connection` (hoặc `connection_changed` sau reconnect) — accept bị chặn, decline vẫn được (R03) |
| API (repin) | Enroll rev1 → propose → clone program rev2 (cùng template) → cả hai repin rev2 → propose | Propose trả row MỚI pin rev2; confirm ×2 thành công — không kẹt `revision_mismatch` (R02) |

## Việc còn mở (cho agent/qa kế tiếp)

1. **MySQL/TiDB race suites** — NOT_RUN. Khi có MySQL test: `FB_TEST_DB=mysql` cho f01/f02/f09/f16, đối chiếu migration 0003 (drop/add constraint) trên dữ liệu thật.
2. **Zalo thiết bị thật** — NOT_RUN. Kiểm luồng zmp-sdk thật (silent login, back, share) trên bản mini mới.
3. **Gap còn lại từ FINDINGS vòng trước** (không thuộc R01–R07): nghi vấn concurrency MySQL, chọn/sửa cam kết 1–3, suy ngẫm đi F08/F15, completed/paused — đối chiếu requirements trước khi mở rộng schema.
4. **Nội dung thật:** fixtures seed không có `minutes` — nếu thầy muốn hiển thị thời lượng, bổ sung minutes khi soạn nội dung (UI đã sẵn sàng hiển thị có nguồn).
5. Nếu thay đổi identity `FamilyAgreement` nữa: nhớ giữ nguyên lịch sử row và đọc kỹ commment QA 19/10 trong `f02_program/models.py` + `services/program.py`.

## Lưu ý cho agent kế tiếp

- Làm việc trên nhánh F02, fetch lại trước khi push, KHÔNG force push, KHÔNG merge main hai kho, KHÔNG đụng production.
- Bằng chứng cũ trong `2026-10-19-c29469b/` là bất biến; tạo thư mục cập nhật mới theo mẫu `2026-10-19-<sha>/` và thêm checksum vào `f02/SHA256SUMS`.
- Regression tests phải giữ RED-able: `test_f02_qa_20261019.py`, `test_f09_unlink_guard.py`, `companion-qa-20261019.test.mjs`, `f02-companion.test.mjs` đều ghi rõ fail trên c29469b.
