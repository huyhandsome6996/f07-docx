# F02 — Vòng hoàn thiện theo đội 5 agent (kiểm thử + phản biện chéo) — 2026-10-19

- **Source SHA ứng dụng:** `e38688c` trên `tinh-nang/f02-dong-hanh-bon-tuan-us036-us044` (kế tiếp `e113887`, thêm 1 commit: minutes lift production + copy pin + parity tests web/mini)
- **Tài liệu vòng trước:** `../2026-10-19-c29469b/` (FINDINGS gốc R01–R07) và `../2026-10-19-e113887/` (bản sửa R01–R07) — giữ nguyên, không ghi đè.
- **Cách làm việc:** 3 agent lập trình (backend / web / Mini App) làm song song trong phạm vi riêng → 1 agent kiểm thử chạy backend thật + HTTP thật + cả 3 suite → 1 agent phản biện chéo đọc toàn bộ diff, đối chiếu US-036/US-044 + FINDINGS + điều kiện nghiệm thu, liệt kê issues. Đội 5 agent độc lập với nhau, báo cáo chéo.

## Kết quả phản biện chéo (agent độc lập)

- **BLOCKER:** không có.
- **MAJOR M1 — ĐÃ XỬ LÝ:** 6 file sửa production nằm ngoài commit `e113887` (wiring lift `minutes`, copy pin, +test web/mini) → đã commit thành `e38688c` và push. Trước đó nhánh đã push thiếu fix "thời lượng có nguồn" ở production wiring.
- **MINOR Mi1 — ĐÃ XỬ LÝ:** 5 link evidence sai tên file trong `2026-10-19-e113887` (`http-recheck-results.json` → `http-results.json`, `http-r02-repin-results.json` → `http-r02-results.json`) → đã sửa 3 file .md + cập nhật SHA256SUMS (commit `4f4ec98` trên F02-docx). Số liệu không đổi.
- **MINOR Mi2 — ghi nhận, chưa gấp:** `list_published(limit=50)` F09 — khi nội dung thật vượt 50 item, cần getter theo key hoặc giới hạn có chủ đích. Hiện 4 hoạt động seed, không phát sinh trong kiểm thử này.
- **NOTE N1–N8:** same-pin withdraw→re-propose hồi sinh cùng row (đã có comment code + test); progress lookup theo activity_key+revision (soạn nội dung cần key duy nhất/tuần); demo fixture mini mock confirm trả "confirmed" cho một người (chỉ demo mode); lời mời ngoài joint_activity_keys không hiện ở Companion (không có gap thực tế); render.yaml đúng Render không Cloudflare nhưng cả hai service `branch: main` (deploy thật chờ PR được duyệt merge — đúng quy trình "không merge main khi chưa có sự đồng ý"); `_role_of` fallback chỉ display; một test web có tên over-sell (assert riêng vẫn đúng); MySQL/TiDB thật + thiết bị Zalo thật NOT_RUN kế thừa.

## Kết quả kiểm thử thật (agent QA, backend sqlite local `127.0.0.1:8002`)

| Bộ kiểm | Kết quả |
| --- | --- |
| E2E có sẵn `scripts/f02_e2e_flow.mjs` (không sửa 1 dòng) | **44/44 PASS, exit 0** |
| Bộ HTTP check mở rộng của team (login/consent/connect/provision/reconnect) | **40/40 PASS** — R02 repin 8/8, R03 generation 9/9, R06 catalog 2/2, weeks 2/2, chống tick hộ 2/2, opt-out/re-enroll 4/4, tiền đề 12/12 |
| Kiểm DB cấp SQL (R04 confirmed_at = max hai chữ ký, hai chiều; history 3 rows rev1/2/3 superseded đúng) | **7/7 PASS** |
| Backend harness đủ 17 feature (`tests/feature-lab`) | **524 tests OK, 9 skip (MySQL-gated)** |
| Web suite + build | **252/252 PASS**, build OK |
| Mini suite + build | **332/332 PASS**, build + verify app-config OK |
| `check_import_boundaries.mjs` | **SẠCH** (web không import mini/zmp-sdk, ngược lại) |

- R03 thật: revoke connection → accept lời mời cũ `400 no_active_connection`; decline vẫn cho phép; reconnect generation 2 → accept lời mời gen cũ `400 connection_changed`; mời mới gen 2 accept OK.
- R02 thật: repin rev2 cả hai → propose row mới 0 chữ ký → HS confirm (vẫn proposed) → PH confirm → confirmed; repin rev3 một bên → propose row mới, bên chưa repin `400 revision_mismatch`.
- Chống tick hộ: `participant_id` trong payload → `400 input_invalid/unknown_fields`; chính chủ tick 201.
- Tiến độ theo pin: tick rev2 → repin rev3 → tuần 1 không dính tiến độ cũ.

## Bằng chứng UI thật sau vòng team (môi trường local 3 server)

- Backend `127.0.0.1:8002` (health+ready OK) — web dev `127.0.0.1:3000` — Mini App preview `127.0.0.1:3001`, cùng `VITE_API_BASE_URL=http://127.0.0.1:8002` (một backend).
- Đăng nhập HS901 bằng UI thật cả hai client → trang "Đồng hành" hiển thị dữ liệu máy chủ: "Phiên bản nội dung đang theo: rev 3", đủ 4 tuần mở, hướng dẫn theo vai, hoạt động chung có "Xem chi tiết hoạt động" + "Mời cùng làm", tiến độ "Tôi đã làm/Bỏ qua", thỏa ước tuần 4 "Bản đang hiệu lực: rev 1. Cả hai đã cùng xác nhận", opt-out luôn có.
- Ảnh: `evidence/08-web-companion-team-run.png` (web), `evidence/09-mini-companion-team-run.png` + `...-full.png` (Mini App) — hai client cùng một trạng thái account từ cùng API.
- Lỗi môi trường đã phát hiện và khắc phục trong khi kiểm: web/mini cần `VITE_API_BASE_URL` KHÔNG kèm `/api/v1` (client tự nối); backend dev CORS mặc định chỉ 3000 — chạy mini ở 3001 cần `CORS_ALLOWED_ORIGINS` thêm 3001. Ghi lại để người kiểm thử trực tiếp không lặp lỗi.

## Phạm vi trung thực

- **NOT_RUN:** MySQL/TiDB thật (9 test gated skip), thiết bị Zalo thật (`zmp login/deploy` không chạy), deploy Render thật (không tự deploy theo ràng buộc — `render.yaml` đã chuẩn sẵn: backend Docker + web static, KHÔNG Cloudflare).
- SQLite local chỉ là kiểm tra cục bộ; fixture `HS901/PH901/HS903/PH903` + nội dung rev1/rev2/rev3 là dữ liệu kiểm thử cục bộ, không phải nội dung thật của thầy.

## Checklist cho người dùng kiểm thử trực tiếp (local đã bật)

| Trang | Hành động | Kết quả mong đợi |
| --- | --- | --- |
| Web `#/login` | Đăng nhập HS901 / mật khẩu fixture | Vào Home "Chào Học sinh 901" |
| Web `#/companion` | Mở "Đồng hành" | 4 chủ đề, rev 3, mở tuần bất kỳ |
| Web companion | "Xem chi tiết hoạt động" | Mục tiêu/cách làm/được chia sẻ + thời lượng trung thực |
| Web companion | "Mời cùng làm hoạt động này" | Mời tạo với revision mới nhất |
| Mini preview | Đăng nhập HS901 → "Đồng hành" | Cùng trạng thái rev 3 + thỏa ước như web |
| PH901 (web/mini) | Đăng nhập người đồng hành | Lời mời nhận được, accept/decline tự quyết |
| Hai client | Thu hồi kết nối rồi thử accept | Lỗi trung thực `no_active_connection` |

## Lệnh tái lập nhanh

```bash
# Backend
cd backend && DJANGO_SECRET_KEY=... DJANGO_ENV=development DB_ENGINE=sqlite \
  CORS_ALLOWED_ORIGINS="http://localhost:3001,http://127.0.0.1:3001" \
  python3 manage.py runserver 0.0.0.0:8002 --noreload
# Web
cd web && VITE_API_BASE_URL=http://127.0.0.1:8002 npx vite --host 0.0.0.0 --port 3000
# Mini preview
cd zalo-mini-app && VITE_API_BASE_URL=http://127.0.0.1:8002 npx vite --host 0.0.0.0 --port 3001
# Test suites
bash tests/feature-lab/scripts/test_feature.sh f02_program   # + FB_TEST_DB=mysql khi có MySQL
cd web && npm test ; cd ../zalo-mini-app && npm test
node scripts/check_import_boundaries.mjs
```
