# QA-1 — PHẢN BIỆN CHÉO: đối chiếu quyết định giải conflict của lead với spec Team 1

- **Task ID:** QA-1 · **Team 1 (Phân tích) — trưởng vòng phản biện** · **Chế độ:** READ-ONLY (không sửa code, không commit).
- **Đối tượng:** `/home/z/my-project/wt-integration` @ `6d8b709` (nhánh `tich-hop/f02-f04-f07-f15-an-toan`; chuỗi ghép: main a64f653 → F15 8fbfe01 → F07 c7ce30d → F02 1184a37 → F04 435adce → client 3-a 531ec07 → adapter 3-b 4915be8 → f04 race 2-c 8a9a8d3 → f16 2-d 6d8b709).
- **Soi chiếu:** T1-a (F02), T1-b (F04), T1-c (F07), T1-d (F15), T1-e (main surface) + worklog Task 2-a/2-b/3-a/3-b/2-c/2-d.
- **Bằng chứng chạy trên cây tích hợp (SQLite, harness settings, 17 label):**
  `harness.tests.test_f04_e2e_a5 + f07_mood + f15_privacy` = **171 OK / 5 skip (MySQL-gated)**; `f09_activities + f02 wiring-agreement` = **38 OK**; shared `node --test` = **82/82 PASS**; `django.setup()` production-order probe (trích dẫn trực tiếp ở mục 1).

---

## TỔNG KẾT 6 MỤC

| # | Đối tượng phản biện | Kết luận | Mức |
|---|---|---|---|
| 1 | `f07_mood/services/mood.py` (F07 nền + F15 ledger) | **FINDING** — file mood.py đúng spec T1-c; nhưng cụm wiring registry đi kèm **mất 2 khối F15 ở production boot** (P1-1, P1-2) | **P1** |
| 2 | `backend/core/wiring.py` (bỏ đăng ký f09 InviteService) | **PASS** (+2 NOTE) | — |
| 3 | Shared union 112 method | **PASS** — 112 method, 0 trùng, 0 mất F10–F13/CAP-23 | — |
| 4 | Trang privacy native (id "privacy") | **FINDING** — không có lỗ hổng bảo mật; 1 P2 (route mồ côi) + NOT_RUN đã ghi nhận | **P2** |
| 5 | `web/src/styles/components.css` (+ mini) | **PASS** — 0 selector của main/f04 bị mất; `[hidden]` byte-verified nguyên vẹn | — |
| 6 | Harness A5 thích ứng (actor_id + _AllowAllAuthorizer) | **PASS** — gate R07 không mất ý nghĩa (+1 P2 kế thừa đã ghi worklog) | **P2** |

---

## MỤC 1 — mood.py: FINDING (P1-1, P1-2)

### 1a. Phần giải conflict TRONG FILE mood.py — đúng spec T1-c B.1 ✅
Đối chiếu từng hunk bảng B.1 của T1-c với bản tại `6d8b709`:

| Hunk T1-c | Đề xuất T1-c | Thực tế trên cây | Đánh giá |
|---|---|---|---|
| 1 parse_entry_date | Giữ F07 (fullmatch) | fullmatch + fromisoformat (dòng 56–78) | ✅ |
| 2 create race | Giữ F07 (atomic + IntegrityError→400) | đúng (dòng 116–129) | ✅ |
| 3 edit R02 | Giữ F07 (select_for_update) | đúng (dòng 152) | ✅ |
| 4 share expected_revision | Giữ F07 + quyết lead re-share | F07: khoá row + PreviewStale 409 + re-activate/rebind (dòng 216–247) | ✅ (semantics F07, gate F07-17) |
| 5 revoke ledger | Giữ CẢ HAI | F07 revoke + khối ledger F15 (dòng 261–279): `DeletionLedgerEvent.EVENT_GRANT_REVOKED`, payload item_type/item_id/recipient_id, `entry_point="f07_domain_service"`, ImportError-guarded | ✅ đúng chữ "F15 thêm revoke ledger" |
| 6/7 list_shared_by_me + _connections_current | Giữ F07 | đúng (pair-cache R03, status thật, bound 50) | ✅ |
| 8 list_shared_with_me | Giữ F07; pre-filter SQL là "tùy chọn hybrid" | Giữ F07: filter SQL (recipient/revoked/revision-current) + `cursor_paginate` + recheck Python theo trang | ✅ — xem 1b |
| 9 read_shared 503 | Giữ F07; cân nhắc default −1 | F07: `_require_reader` 503 fail-closed; default `0 or 0` | ✅ (NOTE về −1: tự-consistent, readers trong build đều có `generation`; chấp nhận được) |
| 10 imports/helpers | Bỏ import chết + helpers F15 | `models_f7_entry_revision`, `_binding_current`, `_LIST_BINDING_BOUND` không còn trong cây (grep 0 tham chiếu); import chết F15 không còn | ✅ |

### 1b. Tái đánh giá việc BỎ pre-filter SQL R09 — không mất invariant, chỉ mất hiệu năng (NOTE)
T1-c gọi pre-filter là "tùy chọn" — sau khi tái đánh giá, đồng ý bỏ:
- **Invariant an toàn giữ nguyên:** hàng stale không bao giờ ĐỌC ĐƯỢC — (i) SQL lọc `revoked_at__isnull` + `approved_revision=F(entry__revision)`; (ii) `_connections_current` recheck đúng `(connection_id, generation)` theo từng cặp (R03) trên trang có bounds; (iii) `read_shared` recheck lại TOÀN BỘ điều kiện lần nữa. Reconnect tạo generation mới → verdict False → bị lọc.
- **"Đẩy vọt bound" không còn là lỗ hổng trong thiết kế cursor:** loại trừ của F15 sinh ra vì list có trần cứng (200 rồi DỪNG) — hàng stale có thể đẩy hàng hợp lệ qua trần. Bản F07 dùng `cursor_paginate` (không trần tổng; trang theo `page_size`), nên mọi grant hợp lệ vẫn TỚI ĐƯỢC bằng cách tải thêm — không mất dữ liệu, chỉ tốn thêm request. Trang mood-shared giữ nút "Tải thêm" khi `nextCursor` còn (guard R09 nguyên vẹn, dòng 94–138 cả 2 client) → trang rỗng + cursor không kẹt người dùng.
- **Giá còn trả (chấp nhận):** trang có thể ngắn hơn `page_size` hoặc rỗng trong khi `next_cursor` vẫn còn; số lượt gọi reader = số cặp phân biệt trong trang (bounded). Nếu muốn tối ưu sau này, hybrid T1-c (pre-filter SQL qua `reader.list_active_for_user`) vẫn khả thi — P3.

### 1c. Test nào bị phá? — KHÔNG (đã chạy thật)
- `f07_mood` (53) + `f15_privacy` (90) + harness A5 (28): **171 OK / 5 skip MySQL** trên cây tích hợp.
- grep `reshare|expected_revision|cursor` trong tests 2 feature: F15 head `aeae3212` **không hề có test pin** `reshare_after_revoke_requires_edit` (git grep = 0 kết quả) ⇒ chọn semantics re-activate của F07 không phá test F15 nào; F07 pin phía mình (`Finding4ReshareSemantics`, `ReshareUnlinkReconnectIntegration`) và PASS.

### 1d. Nhưng cụm wiring registry đi kèm mood.py — MẤT 2 KHỐI F15 Ở PRODUCTION BOOT (P1)
Đây chính là kịch bản T1-c B.5/D.1 cảnh báo ("đăng ký đè nhau trên F15 registry — P1"), xảy ra ngược với khuyến nghị:

**Bằng chứng sống (django.setup() với INSTALLED_APPS production trên cây 6d8b709):**
```
REGISTERED ITEM TYPES: ['mood_entry']
mood_entry -> family_bridge_features.f07_mood.services.grant_provider
journal_page provider is None: True
mood_entry accepts after_created_at: False
mood_entry revoke accepts expected_revision: False
deletion hook mood -> f07_mood/services/deletion.py
```
Cơ chế: `settings.py` xếp `f07_mood` (dòng 66) TRƯỚC `f15_privacy` (dòng 68) ⇒ `f07.apps.ready()` đăng ký `mood_entry` **không điều kiện** (apps.py dòng 55–59, chỉ có guard None cho connection_reader, không có cho grant_provider) ⇒ guard all-or-nothing của F15 `if (has_f07 or has_f08) and not registry.registered_item_types()` (wiring.py dòng 52) thấy registry KHÁC rỗng ⇒ **bỏ qua CẢ khối**, mất luôn `journal_page`. `test_f15_wiring.py` không bắt được vì setUp `reset_registries()` rồi gọi `configure_production_wiring(force=True)` → trong test registry rỗng → F15 đăng ký đủ cả hai ⇒ test xanh, production hỏng (không có test nào boot đúng thứ tự production rồi assert journal_page).

**P1-1 — `journal_page` không bao giờ được đăng ký ở production:**
- `f15_privacy/api.py:135` `item_types = list(grant_registry.registered_item_types())` ⇒ **privacy overview (trang web+mini đang dùng) chỉ liệt kê grant mood, mất hẳn grant nhật ký F08** so với main a64f653 (main không có f07 apps.py mới ⇒ guard của F15 pass ⇒ cả hai được đăng ký qua `f15_privacy.services.adapters`). Người dùng không xem/thu hồi được grant nhật ký từ trang Riêng tư.
- Kèm theo: `can_view_item("journal_page", …)` luôn False (deny-by-default khi provider None) — hiện chưa có caller production nên chưa vỡ luồng đọc, nhưng là bẫy cho tương lai.

**P1-2 — hook xoá dữ liệu category "mood" = bản F07 KHÔNG có cutoff:**
- Hook được đăng ký là `f07_mood/services/deletion.py` — xoá TOÀN BỘ `MoodEntry` của user, bỏ qua `requested_at`. F15 invariant 2 (T1-d C.2): "retry/replay không nới phạm vi/xoá mục tạo sau cutoff". Hậu quả: (a) yêu cầu xoá category `mood` một phần xoá cả mục tạo SAU thời điểm yêu cầu; (b) restore replay chạy lại hook với cutoff gốc có thể xoá dữ liệu tái tạo sau restore.
- Mâu thuẫn nội bộ: Task 2-a vừa sửa F04 hook "ai" đúng idiom cutoff (commit b7a95de) nhưng "mood" — cùng một lớp lỗi mà T1-d chỉ ra trước — lại bị F07 nuốt slot theo đúng cơ chế ở P1-1. T1-c B.5 đã đề xuất "một hook hợp nhất — cutoff của F15 + phần revoke received-grants của F07 — đăng ký đúng một nơi": chưa thực hiện.

**Suy giảm kèm (đúng như T1-c B.5 dự đoán khi F07 thắng slot):** overview mất cursor cho mood (provider F07 không nhận `after_created_at`/`after_share_id` ⇒ rơi vào nhánh "legacy provider: single bounded batch" ≤200 — chính điều R09 sửa; comment trong `_overview_page` "never used in production wiring" giờ SAI); F15 API revoke kèm `expected_revision` → 400 `provider_cannot_validate_expected_revision` (UI native KHÔNG gửi expected_revision khi thu hồi — đã kiểm `http-endpoints.js:867–874` — nên UI không vỡ; chỉ contract api.md của F15 suy giảm).

**Khắc phục đề xuất (trước merge):**
1. F15 CHỦ slot khi f15 có trong build: trong `f07_mood/apps.py` thêm điều kiện `not apps.is_installed("family_bridge_features.f15_privacy")` cho cả `mood_entry` lẫn hook `mood` (đăng ký của F07 chỉ còn ý nghĩa standalone); HOẶC đổi guard của F15 từ all-or-nothing thành per-item (`"journal_page" not in registered_item_types()` / `"mood_entry" not in …`) + hợp nhất provider.
2. Hook "mood" hợp nhất: cutoff F15 (parse/`created_at__lte`/postcondition, idiom đã chuẩn hoá ở Task 2-a) + revoke received-grants của F07; đăng ký đúng một nơi; đồng bộ với fix "ai" của 2-a.
3. Thêm 1 test wiring **không reset registry** (boot đúng thứ tự INSTALLED_APPS như production, assert `journal_page` + `mood_entry` + hook `mood` có cutoff) — lớp test hiện tại đều reset nên không thấy được lỗi thứ tự này.

**Kết luận mục 1:** file mood.py PASS theo spec; cụm wiring đi kèm = **FINDING P1-1 + P1-2** (phải sửa trước merge).

---

## MỤC 2 — core wiring f09: PASS ✅ (+2 NOTE)

- Lead đã BỎ khối f09 trong `wire_backend_ports` kèm comment lý do đầy đủ (dòng 253–261): core đứng trước feature apps, đăng ký trước sẽ shadow reader của F02/F09 do guard slot-None ⇒ quyết định này giữ đúng intent T1-a Rủi ro #1.
- **"Primary pair đúng dù có backup":** f02_program KHÔNG bị core đụng (không có block f02 trong core wiring) ⇒ reader lọc `relationship_kind=PRIMARY, status=ACTIVE, order_by("-id")` của F02 vẫn sở hữu slot f02 (invariant 2 + `test_current_connections` 5 test). f09 dùng reader riêng của mình (F09 `wiring.F01ConnectionReader`): `status=ACTIVE` + `order_by("-id")` deterministic, trả **dict** `{connection_id, generation, relationship_kind, status}`.
- **Shape dict vs ConnectionView:** đường đọc connection duy nhất của f09 đi qua `_connection_generation()` (activities.py 91–103) — xử lý CẢ dict (`.get`) lẫn attr view (`getattr`), None-safe; `invite`/`_require_live_connection`/`set_own_response` đều qua helper này, không có chỗ nào truy cập attribute trực tiếp ⇒ không còn đường đọc sai shape. Đã chạy `f09_activities` toàn bộ + `test_f02_wiring_agreement`: **38 OK**.
- **NOTE-1 (trivial):** docstring dòng 4 `core/wiring.py` vẫn liệt kê f09 ("f03, f05, f07, f08, f09, f10") — stale so với code; nên sửa 1 dòng cho trung thực.
- **NOTE-2 (kế thừa T1-a R5, chưa xử lý và cũng không bắt buộc):** f03/f05/f07/f08 vẫn nhận `InviteService`whose `active_connection_between` (invites.py:256–261) không `order_by` ⇒ nondeterministic khi một cặp có nhiều row active (hiện trạng main; mô hình một-cặp-primary nên benign). Chuẩn hoá một adapter dùng chung là việc tương lai.

---

## MỤC 3 — shared union: PASS ✅ — **112 method**

Đếm lại bằng `node --import` trên cây `6d8b709`:
- `ADAPTER_METHODS.length` = **112**, **0 tên trùng**.
- Đối chiếu benchmark T1-e **91** + T1-a **12** (F02/F09) + T1-c **8** (F07) + Task 3-b **1** (`listDeletionRequests`) = **112** ✓ đúng công thức union.
- **F10–F13 + CAP-23 không mất method nào** (check theo tên cụ thể): F10 signals ×5 (`signalMeta/Preview/Send/Detail/Ack`), F11 supporters ×6, F12 appointments ×11, CAP-23 admin ×5, F13 `helpDirectory` — tất cả OK(0 missing). F15 đủ 7 (`privacyOverview, revokeGrant, requestDeletion, getDeletionRequest, cancelDeletionRequest, withdrawConsent, listDeletionRequests`); F02 đủ 12; F07 đủ 8.
- Pins cập nhật đúng luật "union + đếm lại": `http-endpoints.test.mjs:315` và `purity.test.mjs:67` đều = 112.
- Chạy thật: `node --test packages/family_bridge_shared/tests/*.test.mjs` = **82/82 PASS** (gồm test surface duyệt mọi method là function + mock parity).

---

## MỤC 4 — trang privacy native: FINDING (P2) — không có lỗ hổng thật

Lead giữ trang native main (id `privacy`, chrome `app`) + port các semantic page-core (theo header file và test thích ứng): cursor v2 "ov2|…" (nút Tải thêm chỉ hiện khi `has_more`, dedup khóa `item_type|item_id|share_id`, trần `SHARE_ITEMS_MAX=300`), guard double-submit Thu hồi, reconcile đúng 1 GET sau mutation mất response (K7), phân loại `kind=configuration`. web↔mini **giống hệt nhau** (diff 0 dòng). Cancel xoá gửi `expectedRevision` (dòng 707). `pages.test.mjs` hợp nhất đúng T1-d B.5 (nhãn main + assert điều hướng `/privacy` của F15). Test `f15-privacy` 17 it thích ứng theo điểm chặn native, không xoá assertion (đọc header comment test).

**Phân loại những gì còn thiếu so với semantic F15 (T1-d mục B/C):**

| Thiếu | Phân loại | Ghi chú |
|---|---|---|
| Nút điều hướng → `/privacy-items` (trang "Chia sẻ từng mục" F08) | **P2-1 — LỖI GHÉP NHẸ** | Route `"/privacy-items"` còn đăng ký ở mini router (dòng 37) + `items.js/api.mjs/session-bridge.js/page-core.js` giữ nguyên, nhưng **grep toàn bộ mini src: 0 chỗ navigate tới `/privacy-items`** — trang mồ côi, chỉ vào được bằng tay. Comment trong `tests/f15-items.test.mjs` khẳng định "nối điều hướng từ /privacy" — KHÔNG đúng với cây. T1-d B.3 khuyến nghị (a) chưa làm; yêu cầu 05-F15 "giữ route HOẶC điều hướng tương đương" chỉ thoán chữ "giữ route". |
| Danh sách yêu cầu xoá (GET `/deletion-requests/list` + cursor v2) trên UI | **NOT_RUN đã chấp nhận** (Task 3-b ghi rõ: method + fixture sẵn sàng, KHÔNG tự thêm UI ngoài scope) | Hệ quả thật: sau reload, người dùng không tìm lại được yêu cầu xoá cũ (receipt chỉ hiện 1 lần theo SEC-19/22; status-dialog chỉ theo request_id trong phiên). Nên nối UI trước release nhưng không chặn merge. |
| Connections list + hủy kết nối R12 trong trang | **NOTE** | Trang main từ trước (wt-main) cũng KHÔNG render `connections` (chỉ nhận payload); page-core có `connectionsCard`+`unlinkConnection` nhưng không port. Khả năng hủy kết nối vẫn có qua luồng F01 khác ⇒ không mất năng lực, chỉ mất một điểm truy cập. (Lưu ý mô tả T1-d B.3 "main có connections list" hơi lạc quan — không phải regression của lead.) |
| verify/process handler trên UI | **Đúng thiết kế — không thiếu** | Handler-only/admin API; fail-closed 503/404 pin bởi `test_f15_wiring` (`test_handler_endpoints_fail_closed_without_authorizer`, `test_handler_endpoints_deny_actor_without_capability`). |

**Kết luận mục 4:** FINDING **P2-1** (nối 1 nút/nav vào `/privacy-items` ở mini — hoặc quyết định bỏ trang một cách tường minh); còn lại NOT_RUN/NOTE, không có lỗ hổng bảo mật (không auto-send, không fake success, trạng thái trung thực).

---

## MỤC 5 — components.css: PASS ✅

So bằng **tập selector** (parse CSS, bỏ comment) giữa wt-main / wt-f04 / wt-integration, cả web lẫn mini:

| So sánh | web | mini |
|---|---|---|
| Selector của main BỊ MẤT trong integration | **0 / 300** | **0 / 284** |
| Selector của f04 BỊ MẤT trong integration | **0 / 321** | **0 / 285** |
| Mới thêm (F07…) | +18 (339 tổng) | +2 (287 tổng) |

- Block **Admin CAP-23** (web, dòng 2217), block **compose N06/N03 của F04** (dòng 2274), section **U01 CTA glyph Zalo** (2393 — section cuối theo main), các block EOF F04 (Sheet consent AI 2545, Bảng kết quả gửi 2574) — **đủ tất cả**, không rule nào bị nuốt. Thứ tự Admin↔compose hoán đổi so với đề xuất T1-b B.1 nhưng T1-b đã ghi rõ hai block selector rời rạc, thứ tự hoán đổi được — không tương tác cascade.
- F07 R06/R09 nguyên vẹn: `.fb-btn[hidden]` — kiểm tra **byte-level** (đếm chuỗi + dump codepoint, né lỗi hiển thị terminal đã gây báo nhầm "idden]" ở T1-b D.1 và được Task 2-b xác minh lại): đúng 1 occurrence `.fb-btn[hidden]`/client, 0 dạng hỏng; `minmax(0,1fr)` ×9/×6, `overflow-wrap:anywhere` ×2, `.fb-mood .fb-sec__sub` có mặt.
- Mini components.css: cùng kết quả 0 missing.

---

## MỤC 6 — harness A5 thích ứng: PASS ✅ (+1 P2 kế thừa)

Commit `711e1ee` (+18/−2): hai call-site `verify_request` trong `F04A5AiDeletionTests` thêm `actor_id=_A5_OPERATOR_ID` (UUID tổng hợp test-only) + `authorizer=_AllowAllAuthorizer()`; giữ nguyên 100% assertion scoped/idempotent/replay-safe.

- **Không mất ý nghĩa gate R07:** `_AllowAllAuthorizer` truyền dạng **tham số** của service (đường "injected > registered" theo hợp đồng `authorize_handler_action`), KHÔNG thay port production, KHÔNG đụng `verification.py`. Production vẫn đăng ký `AdminCapabilityAuthorizer` (capability `privacy.case`, fail-closed) từ f15 wiring khi admin_core có mặt.
- Gate R07 vẫn được pin độc lập ở chính f15: `test_handler_endpoints_fail_closed_without_authorizer` (verify+process → 503, row giữ REQUESTED), `test_handler_endpoints_deny_actor_without_capability`, + test đăng ký authorizer production. Harness A5 chạy lại trên cây: PASS (trong lượt 171 OK).
- **P2-2 (kế thừa, đã ghi worklog Task 2-a — nhắc lại để không thất lạc):** `AdminCapabilityAuthorizer.authorize` chỉ bắt `OperationalError`; nếu gọi service với `actor_id=""` (default của `authorize_handler_action`) khi authorizer production đã đăng ký → `UUIDField` `ValidationError` **crash thay vì fail-closed False**. Không có đường production nào truyền actor rỗng (handler luôn xuống actor phiên) nên không chặn merge, nhưng nên sửa phòng thủ (validate UUID rỗng → return False, hoặc bắt thêm ValidationError) — thuộc f15_privacy/admin_core.

---

## DANH SÁCH P1 / P2 TỔNG HỢP

### P1 — phải sửa trước merge (cụm F15 registry ở f07/f15 wiring)
1. **P1-1:** `journal_page` grant provider không bao giờ được đăng ký ở production (f07_mood.apps đăng ký `mood_entry` vô điều kiện + đứng TRƯỚC f15_privacy; guard all-or-nothing `not registered_item_types()` của F15 bỏ qua cả khối) ⇒ privacy overview mất hẳn grant nhật ký so với main; mood_entry suy giảm (overview không cursor — single batch ≤200; revoke `expected_revision` → 400). Fix: F15 chủ slot khi f15 có trong build (f07 chỉ đăng ký khi standalone) hoặc đổi guard per-item; cộng 1 test wiring boot đúng thứ tự production (không reset registry).
2. **P1-2:** hook xoá "mood" đang là bản F07 **không cutoff** — phá invariant F15 "retry/replay không nới phạm vi" cho category `mood` (xoá cả mục tạo sau yêu cầu; replay sau restore có thể xoá dữ liệu mới). Fix: hợp nhất hook (cutoff F15 + revoke received-grants F07), cùng chuẩn idiom mà Task 2-a vừa áp cho hook "ai".

### P2 — nên sửa
1. **P2-1 (mục 4):** `/privacy-items` còn route nhưng mồ côi — không có điều hướng nào từ `/privacy`/profile (mini); comment test `f15-items` mô tả sai trạng thái cây. Nối 1 nút "Chia sẻ từng mục" hoặc quyết định bỏ trang tường minh.
2. **P2-2 (mục 6):** `verification.py` — actor rỗng + authorizer production → ValidationError crash thay vì fail-closed (đường ít gặp, chỉ gọi service trực tiếp); sửa phòng thủ.
3. **P2-3 (mục 4, NOT_RUN chuyển tiếp):** nối `listDeletionRequests` (đã có ở adapter, pin 112) vào UI trang privacy trước release — hiện người dùng không xem lại yêu cầu xoá cũ sau reload.
4. **P2-4 (mục 2, trivial):** docstring `core/wiring.py` dòng 4 còn liệt kê f09.

### NOTE (ghi nhận, không chặn)
- Bỏ pre-filter SQL R09 của F15 trong `list_shared_with_me` là đúng: cursor + recheck Python bù đủ invariant (không có trần cứng để bị "đẩy vọt"); chỉ tốn hiệu năng — hybrid T1-c để sau (P3).
- `generation` default `0 or 0` (F07) thay vì `−1` (F15): tự-consistent (share + read cùng default), mọi reader trong build đều expose `generation` — chấp nhận.
- Semantics re-share: F07 re-activate/rebind thắng — không test F15 nào bị phá (FL-05 chưa từng có test pin); ledger revoke của F15 vẫn ghi ở mọi đường domain.
- Trang privacy không render connections/unlink R12 — như main cũ, năng lực hủy kết nối vẫn có qua luồng F01.
- MySQL chưa chạy lại trên cây tích hợp (race R02/R04 F07, claim race F04, provision F16) — theo checklist các team, không phải phát hiện mới của QA-1.

### Số method contract cuối cùng: **112** (91 main + 12 F02/F09 + 8 F07 + 1 F15 `listDeletionRequests`), 0 trùng, 0 mất F10–F13/CAP-23; shared tests 82/82 PASS.

*Hết báo cáo QA-1.*
