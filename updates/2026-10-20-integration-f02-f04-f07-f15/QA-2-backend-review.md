# QA-2 — BÁO CÁO PHẢN BIỆN CHÉO (TEAM 2 — BACKEND)

- **Task ID:** QA-2 · **Vai trò:** Trưởng Team 2 (Backend) — vòng phản biện chéo.
- **Chế độ:** READ-ONLY — 0 file code sửa, 0 commit.
- **Đối tượng:** cây tích hợp `wt-integration` @ **6d8b709** (main a64f653 + F15/F07/F02/F04 + các fix T2-a/T2-c/T2-d).
- **Phương pháp:** KHÔNG lấy báo cáo implementer làm bằng chứng duy nhất — đọc trực tiếp diff + trace code path + chạy test thật trên MySQL (FB_TEST_DB=mysql, port 33061).

---

## TÓM TẮT

| # | Mục | Kết luận |
|---|---|---|
| 1 | F04 claim race fix (T2-c) — wait/replay | **PASS** (+2 NOTE, 0 defect code) |
| 2 | F16 provision MySQL (T2-d) — 3 lớp chắn | **PASS** (+1 NOTE vận hành) |
| 3 | F04 hook cutoff (T2-a) — idiom F15 | **PASS** |
| 4 | A5 harness thích ứng | **PASS** (+1 P2 kế thừa từ QA-1, đã tái xác nhận nguyên nhân gốc) |
| 5 | Sạch scope backend diff | **PASS** (+1 NOTE .gitignore) |

**P1 trong phạm vi diff T2: 0.** P2: 1 (kế thừa, ngoài diff T2 — xem mục 4). Test chạy thật: **F04 concurrent 3/3 PASS**; **f16_classroom 91 tests OK (3 skip có lý do)**; **f04 deletion/claim/transaction 17/17 OK**; **f16 races 3/3 OK**.

---

## MỤC 1 — F04 CLAIM RACE FIX (T2-c): PASS

Đối tượng: `packages/family_bridge_features/f04_ai/services/express.py` (diff +445), hàm `_claim_refine_operation` + `_replay_completed` + Phase 5 finalize.

### (a) Người chờ lấy kết quả winner THẬT, không kết quả SAI — ĐẠT
- Mọi đường replay đều đi qua `_replay_completed()` (2 nơi gọi: gặp claim COMPLETED ở vòng create, và gặp COMPLETED trong vòng poll) — hàm này fetch **row `AiSuggestion` thật** theo (author, key) và **bắt buộc `winner.payload_hash_hex == payload_hash` của request** trước khi trả; lệch → 409 `same_key_different_payload`; claim COMPLETED mà suggestion biến mất → 409 `duplicate_key_state_mismatch` (không fake operation mới). Không tìm thấy đường nào trả suggestion sai payload.
- Vòng poll chạy NGOÀI `transaction.atomic` (mỗi poll là 1 SELECT autocommit → luôn thấy commit mới nhất trên MySQL REPEATABLE READ, không kẹt snapshot cũ); `time.sleep(0.1)` giữa các poll, **không giữ lock nào** → finalize của winner không bị waiter chặn.

### (b) Bounds 0.1s / 2.0s / 3 lần — GHI ĐÚNG
- `REFINE_CLAIM_WAIT_STEP_SECONDS = 0.1`, `REFINE_CLAIM_WAIT_TOTAL_SECONDS = 2.0`, `for _ in range(3)` (3 lần attempt create claim) — đúng như tài liệu hóa trong docstring + module comment; deadline 2.0s ≪ TTL reclaim 60s nên cửa sổ chờ **không thể** đụng đường reclaim claim của người khác.

### (c) Winner bị F15 xóa claim giữa chờ — HÀNH VI ĐÚNG HỢP ĐỒNG
- Winner gọi provider xong, finalize lock claim theo pk → row đã mất → `_RefineFencedByDeletion` → 503 `refine_result_discarded_after_deletion`, **không persist gì** (test `test_finalize_after_deletion_completed_stores_nothing` che phủ).
- Waiter poll thấy `op is None` → break → re-claim thành **thế hệ mới** (pk mới) → gọi provider → Phase 4 recheck consent/kill-switch → finalize fence theo pk mới. Kết quả chỉ được lưu đúng 1 lần, đúng nghĩa "sau deletion, retry = thế hệ mới, không hồi sinh" (khớp C9 + invariant F04 trong T1-b).

### (d) Không có đường nào gọi provider 2 lần trong 1 thế hệ — ĐẠT (trace)
- `_call_provider` có ĐÚNG 1 call-site (`refine()` Phase 3), không nằm trong vòng lặp; chỉ đạt được khi `_claim_refine_operation` trả identity dict (claim FRESH mới). Trong cùng thế hệ: 1 key = 1 provider call (test assert `provider.calls == 1` — PASS 3/3).
- Provider call thứ hai cho cùng key CHỈ xảy ra khi claim biến mất giữa chờ do F15 deletion (hoặc TTL reclaim ≥60s do user chủ động) — tức là **khác thế hệ**, được docstring của `_claim_refine_operation` ghi rõ. KHÔNG có auto-retry/auto-resend ở bất kỳ đường nào (C6 giữ nguyên).

### (e) Khác-payload vẫn fail fast — ĐẠT
- Claim INFLIGHT khác payload → `SlotUnavailable(refine_in_progress)` 409 **ngay, không chờ**; sau khi winner settle, request lại gặp Phase 1 replay-check → 409 `same_key_different_payload`. Khác `input_revision` → khác payload_hash (`context_revision` đưa vào hash) → cùng đường 409 (test `test_same_key_different_input_revision_conflict_409`).

### Kết quả test chạy thật (MySQL)
- `harness.tests.test_f04_e2e_a5.F04A5ConcurrentKeyTests` — **chạy 3 lần: 3/3 OK** (0.21–0.32s/lần); assert: cả 2 request thành công/replay, cùng 1 suggestion id, `AiSuggestion.count()==1`, `AiRefineOperation.count()==1`, `provider.calls==1`.
- Bổ sung: `test_f04_deletion + test_f04_claim_identity + test_f04_transaction` = **17/17 OK** trên MySQL.

### NOTE (không chặn)
- **NOTE-1 (P3, docs):** câu mở file *"a concurrent same-key request never calls the provider a second time"* chưa định nghĩa "trong cùng thế hệ claim" — trong khi chính docstring `_claim_refine_operation` đã ghi nhận đường re-claim sau khi row biến mất (F15 deletion) sẽ gọi provider lần nữa (thế hệ mới). Nên chèn 3 chữ "per claim generation" để tránh tranh cãi sau này.
- **NOTE-2 (P3, semantics):** trong lúc winner còn INFLIGHT, caller khác-payload nhận 409 reason `refine_in_progress` thay vì `same_key_different_payload` (đổi được ngay khi settle). Client không phân biệt được 2 tình huống trong cửa sổ chờ — chấp nhận được, nhưng client không nên hiển thị reason này nguyên văn cho user.

---

## MỤC 2 — F16 PROVISION FIX (T2-d): PASS

Đối tượng: `f16_classroom/services/admin_provision.py` `_create_admin_connection` (+69) + `tests/test_races_mysql.py` (+74).

Tiền đề xác nhận bằng test thật: system check trên MySQL in **4 warning models.W036** (trong đó `f01_identity.Connection`) — `uniq_active_pair` là constraint có điều kiện `Q(status="active")`, MariaDB **không tạo constraint** → INSERT trùng KHÔNG báo IntegrityError → 3 lớp chắn tầng app là bắt buộc, không phải thừa.

### (a) DEADLOCK giữa 2 batch — KHÔNG XẢY RA giữa các batch provision; nếu có (lưu ngoài) thì KHÔNG bị nuốt
- Lớp 1 khóa row ClassAccount **cả hai bên bằng MỘT query duy nhất** `select_for_update().filter(user_id__in=[...]).order_by("user_id")` — thứ tự khóa là **deterministic theo code** (user_id tăng dần trên index duy nhất của OneToOne), không phụ thuộc thứ tự submit batch → 2 batch cùng cặp / cùng tài khoản khóa theo CÙNG thứ tự → không có chu trình AB-BA giữa chúng. Backfill dùng cùng helper (`_create_admin_connection`) → cùng thứ tự.
- Cross-flow: f01 invite/f15 revocation khóa Connection/Invite nhưng **không bao giờ** đụng ClassAccount → không có chu trình ClassAccount→Connection ngược chiều.
- Giả sử deadlock vẫn xảy ra (lưu nào đó ngoài ràng buộc trên): InnoDB tự giết 1 bên → Django `OperationalError`. Code chỉ catch `_ActivePairRace` và `IntegrityError` → **OperationalError KHÔNG bị nuốt**: thoát atomic (rollback), bị `_apply_one_row` bắt rộng → row trả `status=error, problems=["row_failed: OperationalError"]`, `summary["errors"] += 1`, `summary["ok"] = False` — **row error trung thực, không bị đổi thành success**; không dupe, không mất dữ liệu.

### (b) Postcondition không thể trả `existing` SAI — ĐẠT
- `dupe` (lớp 3) là locking read `select_for_update` **trong** transaction: nếu tx khác đang giữ row → block tới khi tx kia commit/rollback; chỉ thấy row **đã commit**; `.exclude(pk=connection.pk)` loại chính mình. Sau `_ActivePairRace`, atomic rollback đúng dòng vừa tạo, giữ row committed thật của cặp → trả `existing` = connection ACTIVE hiện hành (dù do batch nào tạo) → `already_active` là **trung thực**, không phải dữ liệu nhầm của batch khác.

### (c) Không mất dữ liệu — ĐẠT
- Toàn đường không có DELETE; raise trong atomic chỉ rollback **insert của mình**; account tạo trước đó trong outer atomic của `_apply_one_row` được commit bình thường khi trả STATUS_ALREADY. Không đổi schema, không migration mới (đúng bounds "chỉ đụng f16_classroom/**").

### Kết quả test chạy thật (MySQL)
- Toàn suite `family_bridge_features.f16_classroom`: **91 tests OK (skipped=3)** — 3 skip là `GateMountedHTTPTests` (gate middleware chỉ mount trên backend settings, liên quan trước T2-d).
- File race riêng `test_races_mysql` verbose: **3/3 OK** gồm test mới `ConcurrentAdminProvisionRaceTests.test_two_concurrent_applies_same_pair_single_connection` (2 thread apply_pairs cùng cặp, batch_ref khác nhau → outcomes `[(0,1),(1,0)]`, `Connection.count()==1`, ACTIVE count==1).

### NOTE (không chặn)
- **NOTE-3 (P3, vận hành):** không có retry-on-deadlock; batch trúng deadlock ghi summary `ok=False` và idempotency theo `batch_ref` sẽ **replay đúng summary thất bại đó** khi re-run cùng batch_ref — admin phải dùng batch_ref MỚI để retry. Hành vi nhất quán (khôngfake success) nhưng nên ghi 1 dòng vào runbook admin-provision.

---

## MỤC 3 — F04 HOOK CUTOFF (T2-a): PASS

Đối tượng: `f04_ai/services/deletion.py` (82 dòng) so với `f15_privacy/services/deletion_hooks.py` (`MoodDeletionHook`).

- **`_parse_cutoff` khớp HỆT idiom F15 (so từng dòng):** `isinstance(requested_at, dt.datetime)` → pass-through; còn lại `dt.datetime.fromisoformat(str(requested_at))` → None/"abc" → **ValueError** (fail-loud, runner F15 báo failed category — không mở rộng phạm vi xóa). Byte-for-byte giống `_parse_cutoff` của `deletion_hooks.py`.
- **Cutoff `lte` khớp MoodDeletionHook:** filter `author_id=str(user_id), created_at__lte=cutoff` — cùng dạng `owner + created_at__lte=cutoff` như Mood/Journal; 2 QS (suggestion + operation) dùng công thức ok **giống hệt idiom 2-QS của `SurveysDeletionHook`/`ConnectionsDeletionHook`**.
- **`ok` đúng nghĩa postcondition:** mỗi QS `ok_i = (expected == 0) or (deleted > 0 and not leftover)`; tổng là conj. Nghĩa: xóa đủ expected trước cutoff và **không còn sót** trong scope → ok=True; còn sót (leftover) hoặc expected>0 mà deleted==0 → **ok=False**; run 0-row (idempotent re-run) vẫn ok=True. Khớp đúng yêu cầu "xóa đủ expected trước cutoff, còn sót → ok=false". `deleted` trả về = tổng 2 QS, detail có tỉ lệ n/n cho cả hai bảng.
- **Khác biệt duy nhất (vô hại):** f04 khai `requested_at=None` default (MoodDeletionHook bắt buộc kwarg) — thiếu cutoff vẫn rơi vào `fromisoformat("None")` → ValueError: cùng kết quả fail-loud, chỉ khác loại exception bề mặt nếu runner gọi sai signature (NOTE P3, không phải lỗi).
- Hook đăng ký tại `f04_ai/apps.py ready()` (guarded, không bao giờ chết boot); test `test_f15_registry_resolves_ai_category_to_f04_hook` pin registry. **Test chạy thật:** `test_f04_deletion` (7 tests, gồm cutoff-scope/idempotent/ISO-string/missing-cutoff-raises/replay-after-deletion) — PASS trong lô 17/17 MySQL nêu trên.

---

## MỤC 4 — A5 HARNESS THÍCH ỨNG: PASS

- Grep toàn repo: `_AllowAllAuthorizer` và `_A5_OPERATOR_ID` **chỉ tồn tại trong 2 file test** (`f15_privacy/tests/test_f15.py` — idiom F15 có sẵn, và `tests/feature-lab/harness/tests/test_f04_e2e_a5.py`). **0 rò vào production path.**
- Production `DeletionService.verify_request` re-authorize qua `authorize_handler_action` (injected > registered): `authorizer=None` + port chưa đăng ký → **False → 503 `handler_not_authorized`** (fail-closed, `verification.py` docstring DEC-14/18 khớp). Test harness chỉ inject authorizer qua **tham số**, không đụng port production.
- `_A5_OPERATOR_ID` là UUID tổng hợp Nil-based (`00000000-…-a5a5`) chỉ dùng làm actor test — không xung đột UUID v4 thật, không được ghi vào đường production nào.
- **P2 kế thừa từ QA-1 (không phải hồi quy của T2, tái xác nhận nguyên nhân gốc):** `AdminCapabilityAuthorizer.authorize` filter `Q(user_id=str(actor_id), …)` — `AdminCapabilityGrant.user` là **FK UUID**; actor rỗng (`""`) + authorizer production → Django `ValidationError` ("not a valid UUID") **không được bắt** (code chỉ catch `OperationalError`) → 500 thay vì fail-closed 503. Harness tránh được vì luôn truyền actor UUID tổng hợp; production view phải đảm bảo actor R07 không rỗng. Khuyến nghị: thêm `uuid.UUID()` guard / bắt ValidationError trong `AdminCapabilityAuthorizer.authorize` (thuộc F15/admin_core, ngoài diff T2).

---

## MỤC 5 — SẠCH SCOPE: PASS

Backend diff a64f653..6d8b709 (114 file backend/packages/tests — trong đó phần lớn là toàn bộ hợp nhất 4 feature của các team khác):

- **f04_ai, f16_classroom, f15_privacy, f07_mood, f02_program** = 4 feature + F02 của Team khác — đúng phạm vi.
- **Phụ thuộc dùng chung, mỗi cái có lý do thật:** `f01_identity` (consent ai_processing + Connection generation cho hook/f09), `f06_drafts` (expected_revision + wire transport — scope F04-A2 theo T1-b), `f08_journal` (JournalDeletionHook của F15 + auth), `f09_activities` (apps.ready wiring — điều kiện để `backend/core/wiring.py` gỡ wiring core cũ), `admin_core` chỉ đọc (capability test f16/f15), **không file nào bị sửa ngoài các nhóm này**.
- **`backend/core/wiring.py` (+15/−9):** chỉ là GỎ wiring `f09_reg.register_connection_reader(invite_service)` — chính đáng: nhánh F02 có sẵn `f09/wiring.py` + `apps.ready()` với reader deterministic `order_by("-id")`; giữ wiring core sẽ shadow reader tốt hơn (core chạy trước feature app trong INSTALLED_APPS). Có test `test_f09_r06_wiring_minutes.py` bảo lãnh.
- **`harness/settings.py`:** chỉ mở `HARNESS_DEPS["f15_privacy"]` (test-only). **`backend/config/settings.py`:** env AI + `CORS_ALLOW_HEADERS + x-idempotency-key` (fix CORS F04, khớp T1-b mục D.6).
- **Bất thường nhỏ:** `.gitignore` +2 dòng (`.f15-artifact-case/`, `www-artifact-test/`) — artifact F15, lành tính, **NOTE P3** (nên chuyển về nhánh F15 nếu muốn diff T2 "sạch tuyệt đối"; không chặn).
- **Secret/env:** grep toàn diff (`api_key|password|secret|token` + pattern literal `password.*=.*['"][A-Za-z0-9]{8,}`): **0 secret thật** — chỉ có tên env đọc qua `os.getenv` (GEMINI_API_KEY, ZALO_APP_SECRET…), không value; credential MySQL trong `scripts/test-env-mysql.sh` (fblocalpw @127.0.0.1:33061) là **file ngoài diff**, local test-only.

---

## DANH SÁCH P1 / P2 / NOTE

**P1: 0** (trong phạm vi 3 diff T2-a/T2-c/T2-d + wiring + harness).

**P2: 1** — kế thừa từ QA-1, đã tái xác nhận nguyên nhân gốc (ngoài diff T2, thuộc F15/admin_core):
- **P2-1:** `AdminCapabilityAuthorizer.authorize` (verification.py) — actor rỗng + authorizer production → `ValidationError` (UUID filter) không được bắt → 500 thay vì fail-closed 503. Fix đề xuất: guard/parse UUID hoặc catch ValidationError; và pin test với actor rỗng.

**NOTE (P3, không chặn):**
1. NOTE-1 — docstring đầu `express.py` "never calls the provider a second time" nên định lượng "per claim generation" (đường F15-deletion-mid-wait → re-claim = thế hệ mới, đã được docstring `_claim_refine_operation` mô tả đúng).
2. NOTE-2 — 409 `refine_in_progress` cho caller khác-payload khi winner còn INFLIGHT: không phân biệt được với cùng-payload-bận cho tới khi settle.
3. NOTE-3 — f16: không retry-on-deadlock; re-run cùng batch_ref replay summary thất bại → cần batch_ref mới khi retry; nên ghi runbook.
4. NOTE-4 — f04 hook nhận `requested_at=None` default (F15 hook bắt buộc kwarg): cùng fail-loud ValueError, khác loại exception bề mặt.
5. NOTE-5 — `.gitignore` +2 artifact dir của F15 nằm trong dải merge chung (lành tính).

---

## BẰNG CHỨNG TEST CHẠY THẬT (MySQL 127.0.0.1:33061, FB_TEST_DB=mysql)

| Lệnh | Kết quả | Ổn định |
|---|---|---|
| `manage.py test harness.tests.test_f04_e2e_a5.F04A5ConcurrentKeyTests -v 2` | OK (1 test) | **3/3 run PASS** |
| `manage.py test family_bridge_features.f16_classroom -v 1` | **OK — 91 tests (skipped=3** GateMountedHTTP, lý do cũ) | 1 run |
| `manage.py test family_bridge_features.f16_classroom.tests.test_races_mysql -v 2` | OK — 3/3 (gồm test mới ConcurrentAdminProvisionRaceTests) | 1 run |
| `manage.py test …test_f04_deletion …test_f04_claim_identity …test_f04_transaction` | OK — 17/17 | 1 run |

System check trên MySQL in 4 warning `models.W036` — xác nhận đúng tiền đề "constraint điều kiện không được tạo trên MariaDB/MySQL" của fix T2-d.

## HÀNH ĐỘNG TIẾP THEO (đề xuất, không chặn merge các fix T2)

1. (P2-1) F15/admin_core: fail-closed actor rỗng trong `AdminCapabilityAuthorizer` + test pin — gom vào đợt fix wiring registry P1 của QA-1 (cùng vùng F15).
2. (NOTE-1/2/3) 3 chỉnh docs/runbook 1–2 dòng: express.py module docstring, f16 admin runbook (retry sau deadlock cần batch_ref mới), client F04 không hiển thị reason 409 nguyên văn.
3. Không cần thay đổi code trong 3 diff T2 — đủ điều kiện giữ nguyên trong cây 6d8b709.

*Hết báo cáo — QA-2 (READ-ONLY, 0 commit).*
