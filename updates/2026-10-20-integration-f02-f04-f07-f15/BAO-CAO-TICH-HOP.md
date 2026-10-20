# Báo cáo tích hợp F02 + F04 + F07 + F15 vào main — 20/10/2026

Thực hiện bởi: lead agent (Super Z) + 3 team agent phản biện chéo, theo `PROMPT-COPY-F02-F04-F07-F15.md` và tài liệu 00–09 của nhánh này. Bàn giao bằng tiếng Việt; phân biệt rõ PASS/FAIL/SKIP/NOT_RUN/BLOCKED và code-merge vs release gate.

## A. Nguồn ghép và SHA (đã pin lại khi làm — không dùng mốc cũ)

| Ref | SHA | PR |
| --- | --- | --- |
| main gốc | `a64f6531e627a9163b98d5a4fe8d6787ea45e36e` (không đổi so với pin của bộ) | — |
| F15 | `aeae32124a00bd05fc39802f662370df60ebea93` (không tiến) | #33 |
| F07 | `3fe66cd6b30fd4e1b905e243f272f13823a52ab1` (không tiến) | #42 |
| F02 | `e38688c8bbcd1848aca727630f0fe79cb98ce992` (không tiến) | #39 |
| F04 | `d33b250f16cab362cb3d93908274ea1df2967351` (không tiến) | #40 |
| nhánh tích hợp | `tich-hop/f02-f04-f07-f15-an-toan` head `67ba956897cce65a159f453be150bb2e7998404c` | PR #43 |
| **main sau merge** | **`72302c528c8d5b25c4b0e2de920043770e0005a6`** (merge commit, parents `a64f653` + `67ba956`) | #43 MERGED |

Thứ tự ghép: **F15 → F07 → F02 → F04** (đúng đề xuất 06, đã xác minh dependency: F15 đặt nền revoke/session/deletion; F07 là consumer grants; F02/F09 thêm program; F04 thêm AI). Không force-push, không ours/theirs toàn file, không snapshot chép đè; mỗi merge commit ghi rõ intent từng hunk.

## B. Quyết định giải conflict (file chung)

| File | Quyết định + lý do |
| --- | --- |
| `packages/family_bridge_shared/src/adapter/{contract,http-endpoints,mock-adapter}.js` + 2 test | UNION thuần: 91 (main F10–F13) + 8 F07 + 12 F02 + 1 listDeletionRequests = **112 method, 0 trùng tên, 0 mất**; pin đếm cập nhật 82→99→111→112 tại từng bước và chạy shared tests thật sau mỗi bước |
| `packages/family_bridge_features/f07_mood/services/mood.py` | Nền F07 (row-lock R02, expected_revision→PreviewStale 409, cursor_paginate, `_require_reader` 503) **+** ledger revoke R10 của F15 (DeletionLedgerEvent trên mọi đường revoke domain). Re-share sau revoke = re-activate tường minh của owner — 3 test F07 pin semantic này; F15 không có test pin FL-05; invariant privacy giữ: không auto-revive khi reconnect (test pin), revoke chặn ngay |
| `backend/core/wiring.py` | Bỏ đăng ký InviteService vào registry f09 — F02 mang `apps.ready()` wiring riêng (F01ConnectionReader có `order_by("-id")`, `relationship_kind`, generation chuẩn hóa). Core giữ wiring f03/f05/f07/f08. f02_program giữ reader riêng lọc RELATIONSHIP_PRIMARY cho thỏa ước (core không đụng registry f02) |
| `zalo-mini-app/src/pages/privacy/index.js` (add/add) | Giữ trang native main (id "privacy", chrome app, parity 1:1 với web) + port cursor v2/share_id của F15 vào trang native; test `f15-privacy.test.mjs` thích ứng sang trang native GIỮ 100% semantic (0 assertion bị xóa/làm mềm — đã phản biện lại so với bản gốc aeae321) |
| `zalo-mini-app/src/pages/profile/index.js` | Giữ phía main (superset: logout re-read generation + hasLiveSession guard + nút Cài đặt/Riêng tư) |
| `zalo-mini-app/tests/pages.test.mjs` | Union: nhãn "Riêng tư & đồng ý" của main + click-nav /privacy của F15 |
| `web/src/styles/components.css` | Block Admin CAP-23 (main) + compose conflict N06/N03 (F04) + U01 CTA + section F04 AI: giữ nguyên từng block, không ghi đè file |
| `.gitignore`, `f15_privacy/services/sessions.py` | Union / phía F15 (comment production path — hai bên đã hội tụ code) |

## C. Hoàn thiện ngoài merge (phát hiện qua phân tích + phản biện chéo 3 team)

1. **F04 hook xóa "ai" tôn trọng cutoff F15** (trước: xóa toàn bộ, bỏ qua cutoff — vi phạm "retry không nới phạm vi"). Idiom `_parse_cutoff` khớp từng dòng MoodDeletionHook; +4 regression test.
2. **F04 claim race same-key trên MySQL thật**: người thua race nhận `SlotUnavailable` thay vì chờ (tái hiện 5/6 run trên nhánh F04 thuần). Fix: chờ bounded (poll 0.1s, tổng ≤2.0s, tối đa 3 lần thử create) rồi replay COMPLETED claim; khác-payload vẫn 409 fail-fast; provider gọi đúng 1 lần; 2s ≪ TTL reclaim 60s nên không bao giờ chiếm claim của winner.
3. **F16 provision idempotent thật trên MySQL** (tái hiện trên main thuần): `uniq_active_pair` có điều kiện (W036) không được tạo trên MariaDB → re-apply tạo row trùng. Fix 3 lớp: select_for_update ClassAccount hai bên (order_by("user_id") — không tự deadlock) + locking read connection ACTIVE + postcondition rollback; giữ IntegrityError (SQLite) làm lớp cuối. + race test 2 thread ổn định 5/5.
4. **F15/F07 slot ownership theo thứ tự boot** (P1 của phản biện): trước fix `journal_page` không bao giờ được đăng ký ở production (f07 đăng ký vô điều kiện trước f15, guard all-or-nothing). Fix: F15 chủ slot — (re-)register mood_entry qua adapter wrapper (revoke nhận expected_revision, list cursor after_created_at/after_share_id), journal_page + hook mood force-register; f07 guard per-item cho build không có f15; + test boot-order production thật.
5. **Hook "mood" hợp nhất cutoff + revoke received-grants** (P1): một implementation duy nhất ở f07_mood/services/deletion.py; F15 wrapper ủy quyền.
6. **verification.py fail-closed**: actor rỗng/không UUID → 503 `handler_not_authorized` trước khi query (trước: ValidationError 500).
7. **Client parity F15**: `/privacy-items` hết mồ côi (web thêm route 26→27 + trang items thích hợp; mini thêm nút "Chia sẻ từng mục" từ /privacy); `listDeletionRequests` nối UI cả 2 client (7 STATUS_* đúng models.py, nút Hủy per-item giữ expected_revision, 409 → đọc lại đúng hàng không tự retry); `privacyOverview({cursor})` cursor v2 end-to-end; mock fixture test-only.
8. **Test thích ứng hợp lệ (không phải làm mềm)**: harness F04-A5 gọi `verify_request` theo hợp đồng R07 mới (actor_id tin cậy + `_AllowAllAuthorizer` test-only, đúng idiom F15 tự dùng).

## D. Kiểm chứng trên chính SHA tích hợp (`67ba956`) và sau merge (`72302c5`)

| Suite | SQLite | MariaDB 11.4.5 cục bộ (FB_TEST_DB=mysql) | Sau merge trên main |
| --- | --- | --- | --- |
| Harness đầy đủ 17 feature | **787/787 OK** (17 skip MySQL-gated) | **787/787 OK** (5 skip env-gated: Gemini transport, Zalo gate) | **787/787 OK** (5 skip) |
| Foundation `manage.py test` | 52/52 OK | 52/52 OK | — |
| Shared | 82/82 OK | — | 112 method, 0 dup |
| Mobile packages + core | 85/85 OK | — | — |
| Web | 331/331 OK + build PASS | — | — |
| Zalo Mini App | 437/437 OK + build PASS + verify manifest | — | — |
| `makemigrations --check` | sạch | sạch (graph additive, leaf mới: f02 0003, f09 0002, f16 0002 đã có) | sạch |
| Boundary checker / agent-docs / `git diff --check` | SẠCH / OK / OK | — | — |
| CI GitHub trên PR head | backend, mobile, miniapp, web, sqlite-checks, **mysql-checks (service MySQL 8.4 của CI)**, production-guard, test-and-build, agent-docs — **9/9 SUCCESS** | — | CI main sau merge: **toàn XANH** |

**Phản biện chéo (3 team):** QA-1 (conflict vs spec): 2 P1 đã sửa (mục C4, C5) + PASS các mục khác; QA-2 (backend fixes): 0 P1, 1 P2 đã sửa (C6), 3/3 run race test ổn định trên MySQL; QA-3 (client): 0 P1, 2 P2 đã sửa (mục C7), 847/847 test thật. Báo cáo đầy đủ: `reports/QA-1-conflict-review.md`, `QA-2-backend-review.md`, `QA-3-client-review.md` (workspace agent), tóm tắt trong worklog.

## E. Browser thật từ build production (local — KHÔNG phải Render/Zalo device)

Backend thật local + web dist build có `VITE_API_BASE_URL` trỏ backend thật; cặp HS/PH synthetic cấp bằng admin-provision (DEC-24, Connection ACTIVE `relationship_kind=primary`, generation 1); screenshots 17 file (kèm thư mục evidence-browser-smoke/ bàn giao cùng báo cáo):

| # | Kịch bản | Kết quả |
| --- | --- | --- |
| 1 | Login HS801 (mã + mật khẩu cấp sẵn, không mã mời) → consent lần đầu (service bắt buộc, AI/research tùy chọn riêng) → home | PASS — đúng role/UUID/counterpart |
| 2 | Home hiển thị đủ link F02/F07/F08/F10–F13 | PASS |
| 3 | M01: tạo mood entry + lưu lại → nút chuyển "Lưu thay đổi" (editor giữ entry_id — R08) | PASS |
| 4 | M03: share preview dialog (preview đúng mục + note) → chọn người nhận từ cặp ACTIVE → xác nhận | PASS |
| 5 | X01: PH đăng nhập client riêng → mood-shared list → "Mở nội dung" đọc đúng "2026-10-20 — Vui" + note | PASS |
| 6 | M04: HS thu hồi qua #/privacy (dialog confirm) → list trở về rỗng trung thực; PH đăng nhập lại → "Chưa có gì được chia sẻ với bạn" | PASS |
| 7 | P01: #/companion khi chưa publish → "Chưa có chương trình nào được phát hành" (honest, không fixture) | PASS |
| 8 | AI01: #/compose → nút AI disabled + copy trung thực "Cổng gợi ý AI chưa được bật trên máy chủ"; pause 300s "không tự gửi" | PASS |
| 9 | Reload giữa phiên → về login (token chỉ in-memory, không storage) | PASS (thiết kế) |

## F. Code-merge gate vs Release gate

- **MERGE_READY: ĐẠT** — cây kết hợp đủ 4 feature, không unresolved conflict, không P1/P2 mở, auth/privacy/races/migrations/production-wiring/UI/build/CI đạt; phụ thuộc ngoài chưa bật ở trạng thái default-off + trung thực.
- **RELEASE_READY: CHƯA** — các gate phát hành còn mở (mục G).

## G. Còn thiếu / NOT_RUN / BLOCKED (trung thực, không cộng vào PASS)

| Khoản | Trạng thái |
| --- | --- |
| Gemini live (key hợp lệ chưa lộ, chi phí/retention chốt, smoke live) | **BLOCKED_EXTERNAL** — `FB_AI_ENABLED` default OFF; rotate GEMINI_API_KEY cũ đã lộ trong chat qua kênh bảo mật |
| Render smoke sau merge (backend + web auto-deploy) | **NOT_RUN** — cần Huy kiểm SHA deploy trên dashboard (web build-time `VITE_API_BASE_URL` giữ nguyên; không đổi domain/DB) |
| Zalo Mini App trên thiết bị thật (US-049) + submit production | **NOT_RUN/BLOCKED** — browser mô phỏng không thay device thật |
| MySQL provider thật (RDS/TiDB) | MariaDB 11.4.5 cục bộ + MySQL 8.4 CI container — khác provider production; migration/race đã có bằng chứng 2 môi trường MySQL tương thích |
| F02 nội dung published | Seed chỉ DRAFT (fail-closed); cần người có quyền publish qua admin trước pilot |
| Deletion operator/policy, restore backup thật | Gate release riêng theo 05-F15 — không tự bật destructive processing |
| /privacy-items trên web dùng `api.mjs` web (contract shared chưa có endpoint journal) | NOTE — semantics giữ nguyên, ghi rõ trong commit |
| Trello US cập nhật | Chưa có token |
| Workers Builds (Cloudflare) fail trên nhánh PR | Không thuộc required checks; SUCCESS trên main trước và sau merge — cấu hình nhánh ngoài phạm vi |

## H. Rollback và an toàn dữ liệu

Revert code qua đường hợp lệ (git revert merge commit `72302c5` nếu cần); không drop DB, không inverse migration mất dữ liệu; revoke/deletion ledger không rollback; consumer cũ không đọc schema nháp theo quyền rộng hơn; tắt feature hỏng qua flag (FB_AI_ENABLED...) — help/login/help public luôn an toàn.

## I. Hướng dẫn Huy thử nhanh

1. Web: mở web Render sau auto-deploy (kiểm SHA) → đăng nhập cặp cấp sẵn (mã + mật khẩu) → mood tạo/chia sẻ → PH nhận → thu hồi ở #/privacy → PH mất quyền ngay.
2. Mini App: build/testing từ `zalo-mini-app/` (npm run build; QA 437/437 + manifest PASS) — device thật còn NOT_RUN.
3. Bật AI khi sẵn key: set `GEMINI_API_KEY`/`FB_AI_ENABLED=on` ở backend env — nút AI trong #/compose tự mở (đã gate consent + quota + claim idempotent).
4. Publish F02: admin publish ContentItem kind="f02_program" → #/companion hiện chương trình (seed draft không tự publish).
