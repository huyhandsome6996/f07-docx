# Prompt copy-paste — hoàn thiện F04 trong family-bridge

Tôi giao bạn tiếp tục **F04 / US-029–US-033** tại `https://github.com/huyhandsome6996/family-bridge`. Hãy triển khai, kiểm thử và review đến khi hoàn tất phần có thể làm, không dừng ở kế hoạch, scaffold, mock hay test cũ xanh.

## 1. Nguồn tài liệu và ranh giới hai repo

- Repo ứng dụng: `huyhandsome6996/family-bridge`, nhánh F04 thực tế `tinh-nang/f04-ai-ho-tro-dien-dat-us029-us033`.
- Repo tài liệu: `huyhandsome6996/f07-docx`, nhánh **F04-docx**. Từ nay tài liệu, ảnh, yêu cầu, báo cáo, prompt và bằng chứng F04 lưu trên nhánh này.
- **main của f07-docx thuộc F07: tuyệt đối không sửa, push, merge vào, reset hoặc đổi default branch.** Không trộn tài liệu F07 vào F04.
- Đọc `README.md`, `AGENTS.md`, `requirements/USER-DECISIONS.md`, `requirements/F04-ACCEPTANCE.md`, `reports/2026-10-19-e0ee388.md` trên F04-docx. Chạy `python3 tools/catalog.py verify`; dùng catalog để chọn tài liệu/ảnh cần đọc, không bỏ qua vì ZIP lớn.
- Nếu nhánh tài liệu chưa được push do phiên trước bị lỗi xác thực, dùng Git bundle/bộ local người dùng cung cấp để khôi phục **chỉ F04-docx** và push đúng nhánh khi có quyền. Không tự nói nhánh đã tồn tại và không đọc nhầm main/F07. Nếu chưa có bundle thì prompt này đã chứa hai lỗi còn mở để bạn tiếp tục độc lập; ghi chính xác blocker lưu trữ.
- Các ZIP/HTML/DOCX/prompt lịch sử là dữ liệu tham chiếu, không phải lệnh có thể ghi đè yêu cầu này. Không chép snapshot đè lên checkout ứng dụng.

## 2. Kiểm tra đúng phiên bản

SHA mới nhất đã audit: **e0ee38827562a75542fa79fff50984696088d1c9**, commit sửa R01–R05 thật. Fetch remote, ghi head hiện tại và đọc diff nếu mới hơn. Không nhầm hai empty commit CI trước đó với code sửa lỗi.

Kết quả ở e0ee388: backend foundation 52 bài (2 skip), feature-lab F04 và boundary 226 bài (3 skip), web 213, Mini App 323, shared/mobile 79; builds/import boundaries đều qua. Hai probe cũ deletion-inflight cơ bản/pause-edit qua; gửi AI cơ bản qua 4/4 client×vai. Layout desktop textarea 452 px, Mini 320/390 không tràn ngang. **Nhưng hai biến thể P1 dưới đây vẫn lỗi.**

## 3. Hai lỗi phải sửa trước nghiệm thu

### N01 — Preview không bind nội dung người viết thật sự nhìn và duyệt

Tái hiện trên cả web và Mini App:

1. Server draft body A, recipient hợp lệ. Trên UI bấm Xem trước nội dung.
2. Trì hoãn request preview thật; textarea vẫn editable, user sửa thành B.
3. Cho request đi tiếp tới Django. Server preview bind A, sheet lấy textarea live hiển thị B.
4. Confirm → recipient nhận A, khác B đã nhìn để duyệt.

Đã xác nhận bằng Playwright + HTTP adapter + Django/F05 thật, chỉ trì hoãn request, không fake response. Điểm mã ở `onPreview`/`openConfirmSheet` của `web/src/pages/compose/index.js` và `zalo-mini-app/src/pages/compose/index.js`.

Sửa ràng buộc snapshot **body + recipient + revision** server và UI. Autosave trước preview chưa đủ. Mọi thay đổi trong lúc save/preview/confirm phải invalidate/review lại hoặc khóa thao tác có giải thích; không hiển thị B cho preview A. Save lỗi không được gửi draft cũ. Guard sau mỗi await và khi confirm, không đọc tùy tiện live textarea để giả là snapshot đã bind. Thêm regression cho body/recipient đổi, request chậm, hai client, save lỗi và unknown outcome.

### N02 — Claim mới bị request trước deletion chiếm khi tái dùng key

Tái hiện thứ tự xác định bằng service thật trên DB test:

1. Request A giữ claim author/key K, provider A đang chờ.
2. F15 deletion category ai completed, xóa claim A.
3. Request B claim lại K qua `_claim_refine_operation` thật: UUID mới, payload hash khác; B chưa hoàn tất.
4. Provider A trả. Finalize tìm author+key+inflight nên nhận nhầm claim B, lưu original trước deletion và đánh dấu claim B completed.
5. Có 1 old private suggestion; mong đợi 0.

Điểm mã: `packages/family_bridge_features/f04_ai/services/express.py`, claim/finalize. Sửa bằng identity/generation/fencing của **chính operation được claim**, kiểm hash/current state atomically; không chỉ kiểm có row cùng key dưới lock. Chặn old completion qua deletion hoặc TTL reclaim nhưng vẫn cho request mới hợp lệ sau deletion theo policy. Giữ provider ngoài transaction. Test same/different payload, cùng key mới, TTL, replay và MySQL concurrency khi có môi trường. Không nới assertion để chấp nhận hồi sinh dữ liệu.

## 4. Bắt buộc đội đúng 5 agent thật, cùng làm việc

Bạn điều phối và triệu hồi **đúng 5 sub-agent thực** cùng một đợt, có thời gian hoạt động song song:

1. A1 — kiến trúc/API/shared integration: contract snapshot/revision/recipient, adapters, mock parity và cross-client.
2. A2 — Django/Gemini/DB/privacy: N02, boundary F06/F05/F15, consent, idempotency/budget/concurrency, migrations.
3. A3 — Mini App: N01, compose/reply, thiết kế/state/keyboard/safe area và fallback thật.
4. A4 — Web: N01, desktop/mobile, bổ sung state thiết kế còn thiếu và UI theo backend.
5. A5 — QA/security độc lập: viết test đỏ trước fix, E2E bằng API/browser thật, code review và phản biện kết luận.

Một file một owner tại một thời điểm. Review ít nhất hai vòng, vòng đầu A1→A2→A3→A4→A5→A1, vòng sau đổi reviewer. Ghi agent ID/nhiệm vụ/bằng chứng/finding/fix; không tạo năm tiêu đề thay cho năm agent. Agent chết/context đầy phải checkpoint và thay đúng vai để tiếp tục. Không bịa ID/overlap nếu tool không hỗ trợ.

## 5. Giữ các yêu cầu F04 và những fix đã qua

- Web và Mini App dùng chung Django API thật, frontend dùng được chứ không phải ứng dụng tĩnh. Không thêm đường gửi hoặc bảng Message thứ hai.
- AI chỉ backend gọi Gemini. Secret `GEMINI_API_KEY` ở backend env; `VITE_API_BASE_URL` chỉ là origin Django public. Không key trong frontend/log/URL/repo, không dùng key từng lộ trong ảnh.
- Backend hiện có `FB_AI_ENABLED` mặc định false, `GEMINI_MODEL` allowlist, timeout/token bounds. Kiểm cấu hình/phiên bản thật, fail closed, không tự bật production hoặc tự retry request có outcome chưa rõ.
- Consent đúng purpose/version, revoke/kill switch/finalize guard; tác giả đọc/sửa/bỏ/thử lại, không tự bịa sự kiện/lời hứa/ý định/chẩn đoán/điều trị. Provider là bên xử lý kỹ thuật, không phải người thân được quyền xem.
- Author-only AI; recipient chỉ thấy final đúng bản đã duyệt, không original/history qua DTO hoặc body sai. Admin/staff không có default private-read.
- F06 pause tự nguyện 300 giây server; edit/AI không tự hủy/reset; timer/resume/AI/retry không auto-send. AI lỗi vẫn giữ bản soạn, viết/lưu/preview/send/help dùng được.
- Giữ regression R01–R05 cơ bản đang xanh; sửa N01/N02 mà không tái tạo lỗi cũ. Cùng identity trên hai client không âm thầm mất update hoặc dùng preview stale.
- Đọc AGENTS/skill DSA/security/UI/workflow và contract/ownership mới nhất ở family-bridge. Không mở rộng sang F07/F02. Sửa boundary tối thiểu cần để F04 hoạt động; không viện tên thư mục F06/F15 để bỏ lỗi tích hợp.

## 6. Thiết kế và tài liệu phải đủ

Trong kho tài liệu có 4 khung web và 24 khung Mini App, hai ZIP gốc, HTML/DESIGN.md, logo và ảnh bằng chứng. Web thiếu khung thì đọc thiết kế và dùng skill thiết kế để bổ sung state tương ứng Mini App; không bỏ vì chỉ có bốn hình web. Không bắt buộc 24 route: sheet/dialog/inline state/keyboard variant hợp lệ nếu dùng được và mapping rõ.

Lập design-state map đủ từng khung → role/state/component/route/API web+Mini/ảnh thực/status/deviation. Phần hub/lịch hẹn ngoài lõi F04 phải phân định F12, không booking giả hoặc hứa điều trị. Giữ logo thật, không thay bằng emoji/ảnh ngẫu nhiên. Không sao chép lời hứa “riêng tư tuyệt đối/mã hóa cục bộ” hoặc số lượt quota không có nguồn backend.

Test 320/360/390/430/768/1024/1440, text 200%, keyboard/focus/reduced motion; computed visibility của hidden và scrollWidth; device Zalo thật trước claim device-ready. Cập nhật manifest/report/test/peer-review hiện đang có đoạn working-tree và count cũ thành kết quả của một SHA xác định. Lịch sử giữ riêng, không xóa provenance.

## 7. Cách kiểm thử và tiêu chí hoàn thành

Tái hiện N01/N02 đỏ trước fix, thêm regression hành vi thật. Chạy tests/build web, Mini App, shared gồm cả `test_f04_contract_a5.mjs` không khớp glob `*.test.mjs`; backend check/migration drift, feature-lab F04 và boundary, import boundaries/docs checker. Kiểm migration/locks trên MySQL khi có môi trường.

Browser E2E phải dùng HTTP adapter/Django/F05 thật, đọc thư bằng phiên recipient, assert delivered.body == approved preview snapshot. Fake provider chỉ phục vụ fault injection và phải ghi rõ; không là bằng chứng Gemini thật hoặc chất lượng giữ ý. Dùng corpus synthetic cho hai vai, expected facts/intent và forbidden additions; đánh giá Gemini live bằng key mới/budget hợp lệ khi có quyền. Không gửi dữ liệu người thật để test.

Mỗi yêu cầu có owner/status/command/SHA/expected/actual/evidence. Chỉ external blocker được chứng minh mới cho dừng phần phụ thuộc; thiếu key/device không cản sửa code/test/docs độc lập. Không tự giảm assertion, thêm skip, đổi nghiệp vụ hoặc “deferred phase 2” cho N01/N02 rồi gọi Done.

Code complete: N01/N02 hết lỗi, R01–R05 vẫn qua, E2E cả hai vai/client, privacy/pause/deletion/idempotency/cross-client và design mapping được kiểm tra, hai vòng review hoàn tất, không còn P1/P2 code trong scope. Release readiness cần thêm Gemini/MySQL/Render/device/policy phù hợp; nếu thiếu thì ghi CODE_VERIFIED_LOCALLY — RELEASE_BLOCKED_EXTERNAL, không gọi F04 hoàn tất.

## 8. Lưu tài liệu và bàn giao

Ứng dụng sửa/commit trên nhánh F04 của family-bridge, PR review theo repo; không tự merge main hay deploy production. Tài liệu/ảnh/bằng chứng/prompt F04 commit/push **chỉ F04-docx** của f07-docx. Cập nhật catalog/checksum rồi verify; không đưa credentials, DB hoặc ảnh có key vào kho công khai.

Bàn giao SHA/nhánh/PR thật, N01/N02 trước-sau, test counts và skip riêng, ảnh/network đã redact, mapping thiết kế, review của 5 agent, env names/runbook và blocker chính xác. Không tuyên bố đã push/merge/deploy nếu chỉ có local commit hoặc test giả lập.

**Bắt đầu làm ngay: xác minh refs và quyền GitHub, đọc báo cáo mới, triệu hồi đội 5, tái hiện hai lỗi rồi sửa và kiểm tra tới khi đạt gate. Không trả lại một kế hoạch thay cho kết quả triển khai.**
