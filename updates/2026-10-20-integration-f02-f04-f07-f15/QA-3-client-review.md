# QA-3 — BÁO CÁO PHẢN BIỆN CHÉO NHÁNH CLIENT (Team 3)

- Task ID: QA-3 · Trưởng Team 3 (Client) · **CHỈ ĐỌC** — không sửa code, không commit.
- Cây đối chiếu: `/home/z/my-project/wt-integration` @ `6d8b709` (nhánh `tich-hop/f02-f04-f07-f15-an-toan`, working tree clean).
- Phạm vi diff: `a64f653..6d8b709` — privacy 2 client, tests F15, `packages/family_bridge_shared/`; spot-check mood/mood-shared/companion (F07/F02).
- Phương pháp: đọc diff + code trực tiếp (không tin báo cáo implementer), chạy test thật tuần tự, grep a11y/honesty. Tham chiếu: `reports/T1-d-f15.md`, `docs-f0245-f15/hoan-thien-f02-f04-f07-f15/07-NGHIEM-THU-HAI-CLIENT.md` (đặc biệt M02: "nút hidden thật; không request/append trùng, bounded và dedup").

---

## Mục 1 — Parity web/mini trang privacy: **PASS** (kèm 2 P2 đã có tiền lệ QA-1, xác nhận lại bằng bằng chứng mới)

- `diff web/src/pages/privacy/index.js zalo-mini-app/src/pages/privacy/index.js` → **byte-identical, 0 dòng lệch** (33.278 byte mỗi file, 832 dòng). Task 3-a (`89e80b0`) đã patch HAI file cùng nội dung; parity 1:1 giữ nguyên sau 3-a/3-b. Không có lệch nghiệp vụ nào ở `index.js`.
- Hạ tầng xung quanh: `app/dom.js` **identical**; `core/session.js` khác nhau nhưng chỉ là 2 shim re-export cùng nguồn `packages/family_bridge_shared/src/session.js` (không lệch ngữ nghĩa).
- mood/mood-shared (F07): `index.js` **identical** 2 client. companion (F02) lệch 623 dòng diff — kiểm tra kỹ: là **khác biệt cấu trúc có chủ đích** (ADR-3 "web và Mini App có giao diện riêng, dùng chung API"): web `buildActivityMeta/activityDetailNodes/programPreviewNodes` ↔ mini khối inline `activityMeta` + `renderActivityDetail/renderProgramPreview/renderPaperNote`; cùng semantics R01 (chỉ nhận published, revision cao nhất thắng) và R06 (detail qua textContent, thời lượng có nguồn). Không mất tính năng nào phía mini.
- **FINDING P2-1 (xác nhận lại QA-1, thêm bằng chứng): `/privacy-items` MỒ CÔI.**
  - Route chỉ tồn tại ở mini (`zalo-mini-app/src/app/router.js:37`); web **không có** route lẫn trang items.
  - `grep "privacy-items"` toàn src → chỉ có router.js. Trang `/privacy` (identical 2 client) **không có nút/link nào** sang `/privacy-items`; trang profile cũng chỉ dẫn "…nằm ở trang Riêng tư & đồng ý" → `/privacy`. Người dùng chỉ chạm được items page bằng cách gõ hash tay.
  - Mâu thuẫn tài liệu: header `zalo-mini-app/tests/f15-items.test.mjs` (dòng 6–7) viết "quyết định ghép F15: giữ page-core family + items.js, **nối điều hướng từ /privacy**" — khẳng định này **KHÔNG đúng với cây** (khuyến nghị (a) của T1-d B.3 chưa được thực hiện).
  - 2 test f15-items vẫn PASS vì chúng render items.js trực tiếp — test không bắt được việc trang không tới được.

## Mục 2 — Cursor v2 "Tải thêm" (privacy/index.js, khối renderGrantsCard)

**(a) Dedup `item_type|item_id|share_id` khi share_id rỗng: PASS + NOTE.**
- `shareKey()` (dòng ~276): `share_id || ""` — cùng share quay lại với share_id rỗng ở CẢ HAI trang → khóa `type|item_id|` trùng nhau → dedup vẫn chặn (phân biệt theo item_id, đúng như comment "provider cũ không có share id"). Backend tự nhất quán: `api.py:99` cursor tie-break cũng fallback `share_id or item_id`, và representation share_id (null/"") ổn định trong một phiên server → không có kịch bản hợp lệ nào cùng một share đổi giữa rỗng/không rỗng GIỮA hai trang liên tiếp.
- Test pin đúng hướng: f15-privacy dùng cùng item_id + KHÁC share_id (s1/s2) để chứng minh dedup dựa share_id, không chỉ item_id.
- **NOTE-1:** dedup giữ lần XUẤT HIỆN ĐẦU (trang cũ hơn). Nếu một share bị revoke (bởi chính user từ thiết bị khác) giữa lúc tải trang-1 và trang-2, bản `revoked:true` ở trang sau bị bỏ → hàng cũ "đang chia sẻ" còn hiển thị đến lần reload đầy đủ kế tiếp. Cửa sổ rất hẹp (giây), writer duy nhất của grant là chính user, mutation trong trang luôn đi qua reload → chấp nhận được, ghi nhận để hậu kỳ.

**(b) Trần 300 + dừng-có-trần: PASS + NOTE-2.**
- `SHARE_ITEMS_MAX = 300`; khi đủ trần, nút Tải thêm không render và hiện hint: *"Đã hiển thị 300 mục gần nhất; các mục khác vẫn nằm an toàn trên máy chủ."* — trung thực (không fake "đã tải hết").
- Dừng-có-trần khi trang kế 0 mục mới: `sharedExhausted = true` + note *"Chưa tải thêm được mục mới nào. Tải lại trang để xem danh sách mới nhất."* — trung thực, có test pin (assert `/Chưa tải thêm được mục mới nào/`).
- **NOTE-2:** trần chỉ chặn LẦN BẤM KẾ (check nằm ở `drawLoadMore`), không cắt giữa trang: một trang server (tối đa ~50 mục) có thể đẩy hiển thị vượt 300 (ví dụ 290 → 340) trong khi hint vẫn nói cứng "Đã hiển thị 300 mục gần nhất" → con số trong hint có thể lệch thật. Gợi ý sửa: dùng `listWrap.children.length` thực tế trong hint.

**(c) Stale-guard `renderSeq`/`isConnected` nuốt response MỚI: PASS (không tìm thấy đường nuốt) + NOTE-3.**
- Phân tích thứ tự sự kiện: `state.renderSeq` CHỈ tăng trong `renderGrantsCard`, mà hàm này chỉ chạy sau khi một GET overview MỚI (page-1) resolve xong. Response "Tải thêm" chỉ bị nuốt khi một reload đầy đủ đã xảy ra — mà reload đó tự thân fetch page-1 MỚI HƠN từ server và reset cursor/dedup. Response bị nuốt luôn là response CŨ so với lần render mới, không có dữ liệu nào bị che mất vĩnh viễn.
- Không thể có 2 request "Tải thêm" song song: `loadMoreBusy` + nút disabled trong khi bay → không có kịch bản response MỚI của chính luồng load-more bị luồng khác nuốt.
- Race revoke-đang-bay ↔ load-more-đang-bay: thứ tự nào cũng kết thúc bằng một render page-1 fresh (cursor reset) — dữ liệu tải thêm có thể phải bấm Tải thêm lại, không mất dữ liệu.
- **NOTE-3:** sau revoke/rút đồng ý (reload), các trang đã tải thêm SỤP VỀ page-1 (cursor reset theo thiết kế) — người dùng phải bấm lại; đây là đánh đổi an toàn (danh sách mới là nguồn thật), không phải bug che dữ liệu.

**(d) Nút Tải thêm khi `has_more=false`: PASS — biến mất KHỎI DOM thật.**
- `drawLoadMore()` mở đầu bằng `clear(loadMoreArea)` rồi chỉ append nút khi `sharedHasMore && !sharedExhausted` → khi `has_more=false`, node nút bị GỠ (không chỉ `disabled`/`hidden`).
- Test Task 3-b pin đúng: `assert.equal(loadMore2, undefined, "has_more=false → nút Tải thêm phải biến mất khỏi DOM (ẩn thật)")` — khớp tiêu chí M02 (mood-shared dùng `moreBtn.hidden = !state.nextCursor` — hidden-attr, privacy page còn mạnh hơn).

## Mục 3 — f15-privacy.test.mjs thích ứng vs bản gốc `aeae321`: **PASS** (không assertion gốc nào bị xóa/làm mềm)

So sánh `git show aeae321:zalo-mini-app/tests/f15-privacy.test.mjs` (230 dòng, 8 test) với bản hiện tại (401 dòng, 9 test):

| Test gốc (F15 page-core) | Bản thích ứng (trang native) | Semantic gốc giữ? |
|---|---|---|
| page contract `id:"f15-privacy"`, `showBottomNav:false` | `id:"privacy"`, `chrome:"app"`, `showBottomNav:true`, `requiresAuth:true` | Đổi ĐIỂM CHẶN có chủ đích (quyết định tích hợp: native là trang chính thức, parity 1:1 web) — ghi rõ trong header test, không phải làm mềm |
| chưa có phiên → copy "chưa có phiên" + **0 GET** | copy "Cần đăng nhập để mở trang riêng tư" + **0 `privacyOverview` VÀ 0 `listConsents`** | GIỮ (thậm chí chặt hơn) |
| có phiên + dữ liệu → mục + nút Thu hồi | giữ nguyên + mở rộng pin cursor v2 (cursor thật xuống GET, dedup, dừng có trần) | GIỮ + mở rộng |
| API lỗi mạng → offline + nút Tải lại | "Không tải được trạng thái riêng tư" + nút "Thử lại" **và bấm thử phải refetch thật** | GIỮ + chặt hơn (bản gốc chỉ tìm nút) |
| double-click Thu hồi → 1 POST | qua dialog confirm của native, 3 click liên tiếp → `revokeCalls.length === 1` | GIỮ (double-submit guard là tính năng mới port từ page-core) |
| timeout → không tự retry POST, đọc lại (gốc: `gets.length >= 2` — yếu) | `revokeCalls === 1` + `overviewCursors.length === 2` (CHÍNH XÁC 1 lần đọc lại) + note "CHƯA XÁC ĐỊNH" | GIỮ + CHẶT HƠN (>= → ==) |
| destroy() → response muộn không render lại | giữ nguyên shape test | GIỮ |
| kind=configuration → thông báo riêng | giữ nguyên | GIỮ |
| — | Task 3-b: lần-2 nhận đúng cursor trang-1; append không trùng; has_more=false → nút out-of-DOM | MỚI |

- Cả 3 semantic gốc nêu trong đề bài đều nguyên vẹn: **không phiên → 0 GET; double-click → 1 POST; unknown → đọc lại đúng 1 lần, không tự gửi lại**. Không tìm thấy assertion bị xóa hay hạ điều kiện; 1 test được THÊM (Task 3-b), 1 assertion được siết chặt (>= → ==).
- `f15-items.test.mjs` (39 dòng, 2 test): giữ nguyên điểm chặn items.js vì assertion (draft giữ khi lỗi, không tuyên bố "Đã lưu") không có tương đương trên trang native — đúng logic tránh xóa semantic; nhưng xem P2-1 về comment sai thực tế điều hướng.

## Mục 4 — Shared adapter Task 3-b: **PASS** (kèm P2-2 + NOTE-4/5)

Endpoint map đối chiếu `packages/family_bridge_features/f15_privacy/urls.py`:

| Adapter (http-endpoints.js) | Backend urls.py | Kết luận |
|---|---|---|
| `privacyOverview({cursor})` → GET `/api/v1/privacy/overview` + `query.cursor` (URLSearchParams encode; trang-1 KHÔNG có param cursor) | `privacy/overview` | ĐỮNG; test pin cursor nguyên vẹn qua decodeURIComponent |
| `revokeGrant` → POST `/api/v1/privacy/grants/{item_type}/{item_id}/revoke` | `privacy/grants/<str:item_type>/<uuid:item_id>/revoke` | ĐỮNG |
| `requestDeletion` → POST `/api/v1/privacy/deletion-requests` | `privacy/deletion-requests` | ĐỮNG |
| `listDeletionRequests({cursor})` → GET `/api/v1/privacy/deletion-requests/list`, shape `{results,next_cursor,has_more}` | `privacy/deletion-requests/list` (GET ở `/list`, view gốc chỉ POST) | ĐỮNG path + shape backend `list_requests`; test pin cả cursor pass-through lẫn fallback rỗng trung thực khi body thiếu trường |
| `getDeletionRequest` / `cancelDeletionRequest` (+`expected_revision`) / `withdrawConsent` | `.../{id}`, `.../{id}/cancel`, `consents/{purpose}/withdraw` | ĐỮNG |

- **FINDING P2-2 (xác nhận lại QA-1): `listDeletionRequests` CÓ Ở ADAPTER, KHÔNG CÓ NGƯỜI DÙNG UI.** `grep` toàn `web/src` + `zalo-mini-app/src` → 0 consumer. Trang privacy giữ `deletionRequestId` trong bộ nhớ (SEC-10) và nói thật "máy chủ vẫn giữ yêu cầu thật của bạn", nhưng sau reload KHÔNG có đường UI nào đọc lại trạng thái — trong khi backend xây endpoint list đúng cho mục đích đó (docstring `api.py:302-304`: "so the app can recover status after a lost response or a re-opened Mini App"). Chức năng "phục hồi trạng thái xóa" mới chỉ xong tầng 1/3 (backend + adapter, chưa có UI).
- **NOTE-4:** backend `DeletionRequestListView` đọc query `limit` (default 20, max 50) — adapter không truyền/expose `limit` (chỉ cursor) → luôn dùng page mặc định; không gãy, chỉ là bề mặt chưa đầy đủ khi có UI.
- **NOTE-5 (mock rò production):** mock-adapter được **static import** vào `web/src/adapter/web-adapter.js:28` và glue mini `zalo-mini-app/src/core/adapter/adapter.js:23` → code mock NẰM TRONG production bundle, nhưng **kích hoạt bị chặn chặt**: `resolveAdapterMode(demoMode)` — mock chỉ khi `?demo=1` rõ ràng (`isDemoModeRequested`), không fallback-on-error nào (`web-adapter.js` invariant 1-3). Không page nào import mock trực tiếp. Fixture demo trung thực: trang-cursor trả rỗng + `has_more:false` + `source:"fixture"`. Kết luận: không rò về HÀNH VI; rò về bundle-size (có thể cân nhắc dynamic import — không bắt buộc).

## Mục 5 — Chạy test thật (tuần tự, KHÔNG npm ci)

| Suite | Lệnh | Kết quả |
|---|---|---|
| shared | `node --test packages/family_bridge_shared/tests/*.test.mjs` | **82/82 PASS** (26 suites, 0 fail, 0 skip), ~33s |
| zalo-mini-app | `npm test` | **434/434 PASS** (85 suites, 0 fail, 0 skip), ~122s |
| web | `npm test` | **331/331 PASS** (74 suites, 0 fail, 0 skip), ~73s |
| F15 subset (mini) | `node --test tests/f15-privacy.test.mjs tests/f15-items.test.mjs` | **11/11 PASS** (9 privacy + 2 items) |
| F07 subset (mini) | `node --test tests/f07-mood.test.mjs tests/f07-shared.test.mjs` | **13/13 PASS** |

Gồm cả `f15-session-bridge-artifact` (build+serve thật, R11) và `f15-session-race` trong 434 — 0 fail. Tổng 3 suite chính: **847 test, 0 fail, 0 skip**.

## Mục 6 — A11y / honesty nhanh: **PASS** (+2 NOTE nhỏ)

- **"Sắp có"/placeholder ảo:** grep `Sắp có|sắp ra mắt|coming soon` trên privacy/mood/mood-shared (+toàn pages) → 0 hit trong UI text (chỉ 2 dòng COMMENT ghi việc đã bỏ "Sắp có"). Trang privacy nói rõ "Mọi trạng thái dưới đây là dữ liệu thật từ máy chủ tại thời điểm tải trang" + "không bịa hoặc làm đẹp".
- **Banner demo:** `createDemoBanner` chỉ render khi `demo` (3 điểm trong privacy: load/error/render — đều `if (demo)`); demoMode chỉ đến từ `?demo=1` (không fallback); banner text trung thực "Dữ liệu minh họa — chế độ xem trước", `role="status"`. Demo thực sự đi cùng adapter mock — đúng cặp (banner ⇄ fixture).
- **Nút disabled có giải thích:** mood share — `confirmBtn.title = "Hãy xem lại bản mới rồi xác nhận lại"` / `"Đang gửi…"` (có giải thích); privacy deletion — submit disabled kèm note "Đang gửi yêu cầu…"; thu hồi/rút đồng ý luôn mở dialog nêu hậu quả thật (copy "bản sao ngoài ứng dụng không thu hồi được" lấy từ note backend). Trạng thái xóa: nhãn `completed` chỉ khi máy chủ báo; `failed_needs_action` hiển thị "chưa hoàn tất" — trung thực.
- **NOTE-6 (a11y nhỏ):** nút "Tải thêm" khi busy chỉ `disabled = true`, không có `aria-busy`/label đổi — thời điểm ngắn, ảnh hưởng thấp.
- **NOTE-7:** mini router đăng ký `"/privacy"` HAI LẦN (dòng 38 và 51, cùng module) — vô hại (key sau đè key trước cùng giá trị), nên dọn.

---

## Tổng hợp

**P1 (phải sửa trước release):** 0 — trong phạm vi diff client của QA-3 không tìm thấy lỗi chặn. (P1 backend của QA-1 — registry `journal_page`/hook cutoff — ngoài phạm vi client, không đánh giá lại tại đây.)

**P2:**
1. **P2-1 — `/privacy-items` mồ côi + web thiếu hẳn trang items:** 0 điểm điều hướng từ `/privacy`/profile; web không có route; comment test `f15-items` tuyên bố "nối điều hướng từ /privacy" trái với cây. Sửa: thêm 1 nút "Chia sẻ từng mục" → `/privacy-items` vào trang privacy (khuyến nghị T1-d B.3-a), quyết định phạm vi web (thêm trang hoặc ghi nhận gap).
2. **P2-2 — `listDeletionRequests` chưa nối UI:** trạng thái yêu cầu xóa không phục hồi được sau reload dù backend+adapter sẵn sàng; nối danh sách/tra cứu vào trang privacy trước release.

**NOTE (không chặn):**
- NOTE-1: dedup giữ bản đầu tiên — revoke giữa hai trang có thể hiển thị "đang chia sẻ" cũ đến reload kế (cửa sổ hẹp, writer duy nhất là chính user).
- NOTE-2: hint trần cứng "300 mục" có thể lệch thật khi một trang server đẩy vượt mốc (dùng số hàng thực tế).
- NOTE-3: sau mutation-reload, các trang đã tải thêm sup về page-1 (an toàn, phải bấm lại).
- NOTE-4: adapter không expose `limit` cho list deletion (backend default 20/max 50).
- NOTE-5: mock code nằm trong production bundle (activation gated chặt bằng `?demo=1`) — cân nhắc dynamic import.
- NOTE-6: "Tải thêm" busy thiếu `aria-busy`.
- NOTE-7: mini router khai báo `"/privacy"` trùng 2 lần.
- NOTE-8: `overview.connections` được fetch nhưng không render ở trang privacy (dư payload, không hại).
- NOTE-9: companion web/mini khác cấu trúc có chủ đích (ADR-3), semantics tương đương — không phải parity gap.

**Kết luận từng mục:** 1 PASS (+P2-1) · 2 (a) PASS+NOTE (b) PASS+NOTE (c) PASS+NOTE (d) PASS · 3 PASS · 4 PASS (+P2-2, NOTE-4/5) · 5 **847/847 PASS thực chạy** · 6 PASS (+NOTE-6/7).

Sản phẩm: báo cáo này + worklog QA-3. READ-ONLY: 0 file code sửa, 0 commit.
