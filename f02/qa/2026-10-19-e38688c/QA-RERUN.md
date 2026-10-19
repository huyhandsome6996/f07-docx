# QA-RERUN — Điểm lại đầy đủ sau vòng đội 5 agent (nguồn e38688c)

Ngày: 2026-10-19. Người chạy: agent QA độc lập (Task 4) + main agent tái xác nhận UI thật.

## 1. Môi trường

- Backend sqlite local: `backend/` runserver 8002 `--noreload`, health + ready 200.
- Fixture cục bộ: HS901/PH901, HS903/PH903 (lớp `F02-QA-20261019`, mật khẩu synthetic local `FbE2e-Local-2026!`) — tạo bằng `provisioning.run_import` CSV của f16; connections active.
- Nội dung: `seed_f02_draft_program` → publish B16 `ContentLifecycleService` rev1, rồi clone/publish rev2, rev3 (phục vụ repin R02).
- Admin kiểm thử: `qa-admin-f02` + grant `classroom.provision` (chỉ dùng reconnect pair C).

## 2. Bộ E2E có sẵn (không sửa code)

`node scripts/f02_e2e_flow.mjs /home/z/my-project/work/qa-team/e2e-results` → **44/44 PASS, exit 0**.

## 3. Bộ HTTP mở rộng của team — 40/40 PASS

Chi tiết từng nhóm (tên check, kỳ vọng, kết quả) trong `qa-extra-results.json` (máy kiểm, không commit vào repo app).

- **R02 (8/8):** enroll rev2 cả hai → propose tạo row pin rev2, 0 chữ ký (propose không tính chữ ký) → HS confirm → vẫn proposed, `confirmed_at=null` → PH confirm → confirmed; repin rev3 một bên → propose **row mới** (id khác) → bên chưa repin confirm `400 revision_mismatch` → repin xong confirm OK.
- **R03 (9/9):** `POST /connections/{id}/revoke` → accept lời mời cũ `400 no_active_connection`; decline luôn 200 kể cả đã hủy kết nối; reconnect (gen 2) → accept mời gen cũ `400 connection_changed`; mời mới gen 2 accept 200.
- **R04 (1/1 HTTP + 7/7 DB):** `confirmed_at === updated_at` = thời điểm chữ ký thứ hai; DB đối chiếu `max()` cả hai chiều thứ tự ký.
- **R06 (2/2):** `/activities/catalog` body là dict `{goal,steps,share,text}` (không repr-string), minutes số 1–1440 hoặc null.
- **Weeks (2/2):** 4 tuần, `locked:false` cho cả HS + PH.
- **Chống tick hộ (2/2):** payload kèm `participant_id` → `400 input_invalid/unknown_fields`; chính chủ 201.
- **Opt-out/re-enroll (4/4):** opt-out → `program/my` `active:false`; tick rev2 → repin rev3 → tuần 1 không dính tiến độ cũ; tick lại rev3 201.

## 4. Suite + build + boundary (sau commit e38688c)

| Hạng mục | Kết quả |
| --- | --- |
| Backend `tests/feature-lab` 17 feature | **524 OK, 9 skip (MySQL-gated)** |
| Web `npm test` / `npm run build` | **252/252** / OK |
| Mini `npm test` / `npm run build` | **332/332** / OK + verify app-config |
| `check_import_boundaries.mjs` | SẠCH exit 0 |

## 5. UI thật chéo client (bằng chứng team)

Web 3000 + Mini 3001 cùng `VITE_API_BASE_URL=http://127.0.0.1:8002`:

- HS901 đăng nhập bằng UI thật cả hai → `#/companion` hai bên cùng thấy: rev 3, 4 tuần mở, hướng dẫn theo vai, hoạt động chung + chi tiết + mời, tiến độ riêng, thỏa ước "Bản đang hiệu lực: rev 1. Cả hai đã cùng xác nhận", opt-out.
- Ảnh: `evidence/08-web-companion-team-run.png`, `evidence/09-mini-companion-team-run.png`, `evidence/09-mini-companion-team-run-full.png`.

## 6. Ghi chú cấu hình môi trường cho người kiểm thử trực tiếp

1. `VITE_API_BASE_URL` = origin backend, KHÔNG kèm `/api/v1` (client tự nối `/api/v1/...`).
2. Backend dev CORS mặc định chỉ 3000; mini chạy 3001 → cần `CORS_ALLOWED_ORIGINS="http://localhost:3001,http://127.0.0.1:3001"`.
3. Mật khẩu fixture chỉ dùng local — không đăng ký production.

## 7. NOT_RUN (trung thực)

- MySQL/TiDB thật (9 test gated) — khuyến nghị `FB_TEST_DB=mysql bash tests/feature-lab/scripts/test_feature.sh f02_program` khi có MySQL.
- Thiết bị Zalo thật + `zmp login/deploy`.
- Deploy Render thật (chờ chủ dự án apply blueprint sau khi PR được duyệt — không tự merge main).
