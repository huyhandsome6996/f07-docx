# Prompt thực thi — hoàn thiện F04 sau audit ec29ab (19/10/2026)

Bạn được giao triển khai, kiểm thử và review F04/US-029–US-033 đến khi đạt yêu cầu. Không dừng ở kế hoạch, scaffold, mock, build xanh hoặc báo cáo checklist. ZIP này là bộ bàn giao đầy đủ các nguồn hiện còn và bằng chứng audit mới; đọc nội dung theo catalog, không bỏ qua vì ZIP lớn.

## 1. Hai repo, đúng nhánh, đúng phiên bản

- Code ứng dụng: https://github.com/huyhandsome6996/family-bridge
- Nhánh F04 thực tế: `tinh-nang/f04-ai-ho-tro-dien-dat-us029-us033`. Tên English `feature/f04-ai-assisted-expression-us029-us033` cũ không còn; không tự tạo nhánh mới từ main cũ rồi bỏ code F04.
- SHA vừa audit: **ec29abbb60bb5948fff2e87e63b0db5e0cdc4333**. Fetch và ghi SHA head hiện tại; nếu mới hơn, đọc diff và xác nhận từng finding còn/đã hết bằng test, không tự suy.
- Tài liệu: https://github.com/huyhandsome6996/f07-docx, nhánh chính xác **F04-docx** (F viết hoa). `main` thuộc F07: tuyệt đối không sửa/push/merge/reset hoặc đổi default branch. Không đưa F04 vào main của repo này.
- Nhánh tài liệu chưa được xác nhận đã xuất bản vì đường Git của môi trường audit bị chặn xác thực; ZIP này là nguồn bàn giao độc lập. Không chờ push tài liệu mới bắt đầu sửa code. Không bịa URL/commit/deploy đã tồn tại.
- Không tự merge main hoặc deploy production. Giữ mọi thay đổi sẵn có của người dùng, đọc ownership/locks trước sửa shared/F06/F15.

## 2. Bắt buộc đọc và kiểm kê

Đọc README.md, AGENTS.md, requirements/USER-DECISIONS.md, requirements/F04-ACCEPTANCE.md, reports/2026-10-19-ec29ab.md, reports/2026-10-19-ec29ab-ui-matrix.md và repro/ec29ab/README.md. Chạy `python3 tools/catalog.py verify`.

Đọc AGENTS/skills DSA, security, UI, workflow và contracts hiện hành trong app. ZIP/HTML/DOCX/prompt lịch sử là dữ liệu tham khảo, không phải quyền thực thi script hoặc chép snapshot đè lên source. Đọc designs/original, designs/extracted, assets/logos; có 4 khung web và 24 khung Mini. References chứa tài liệu/diff ở một SHA, không phải chứng nhận Done.

Audit mới: foundation52 (2skip), feature232 (3skip), web222, Mini330, shared/mobile/qa87; builds/import/Django/migration checks qua. Basic compose4/4 và reply+đọc ở client kia4/4 qua. N01 cũ (edit lúc preview pending) và N02 cũ (deletion/claim reuse) đã qua probe độc lập. **Không làm lại năm lỗi cũ như thể chưa có fix; giữ chúng như regression.**

## 3. Bắt buộc đội đúng 5 sub-agent thật, cùng làm song song

Điều phối và triệu hồi đúng 5 agent chuyên môn trong cùng một đợt, có thời gian hoạt động chồng nhau:

1. A1 — kiến trúc/shared/API: snapshot body/recipient/revision/preview, N03 + N06 contract/adapter/mock parity; phối hợp ownership.
2. A2 — Django/Gemini/privacy/database: optimistic concurrency, N06 backend và N03 server integration; giữ N02 fence, consent, budgets, deletion; migration nếu thật sự cần.
3. A3 — Mini App: N03/N04/N05/N06, caregiver semantics, design states, keyboard/focus/safe area/fallback; API thật.
4. A4 — Web: N03/N05/N06, responsive/large text và counterpart của thiết kế Mini; API thật.
5. A5 — QA/security độc lập: reproduce đỏ trước fix, browser HTTP E2E, reviewer và người phản biện điều kiện Done.

Một file một owner tại một thời điểm; agent review không ghi đè edit của owner. Hai vòng phản biện thật: vòng1 A1→A2→A3→A4→A5→A1; vòng2 đổi reviewer. Ghi ID, assignment, finding, evidence, phản hồi và fix/retest. Không tạo năm tiêu đề thay agent, không bịa ID/overlap. Nếu công cụ không hỗ trợ delegation, báo rõ giới hạn, không tự nói đã đáp ứng. Agent hết context phải checkpoint để thay đúng vai, tiếp tục phần độc lập.

## 4. N03 — P1 phải sửa: duyệt recipient A nhưng gửi B

Script: repro/ec29ab/cross_client_recipient.mjs. Evidence: cross-client-recipient.json và hai ảnh wrong-recipient-preview. Đây là hai browser client/HTTP/Django/F05 thật; chỉ AI provider fake.

Cùng author có hai active connections A/B. Web và Mini load cùng draft sạch/đã sync với A. Client kia đổi B và lưu, không đổi body. Client review bấm preview; server trả recipient_id B/revision mới/body snapshot. UI vẫn ghi “Gửi cho A”; confirm200 gửi B, A không nhận. Hai chiều đã FAIL.

Không sửa riêng text nút. Chốt một snapshot bất biến gồm body, recipient ID, tên được resolve từ active connection hiện hành, revision, preview ID. So response backend với intent của lần xin preview: recipient/revision/body lệch phải invalidate, refresh/reconcile có giải thích và yêu cầu review mới. Không âm thầm chuyển người nhận. Recheck trước confirm và server vẫn giữ checks cuối. DTO thiếu/sai không được fallback thành một bản “đã duyệt” không chứng minh được.

Regression: đổi body/recipient/revision ở client thứ hai trước/trong request; save/preview/confirm delay; sai/missing DTO; local editing; AI apply rồi save; cả hai vai và cả hai chiều client; recipients đọc final thực. Assert tên người được duyệt + ID đúng người nhận thực, không chỉ delivered.body == preview.body. Giữ N01 locking/stale protection đang qua.

## 5. N06 — P2: stale save ghi đè bản của client kia

Script: cross_client_draft_conflict.mjs. A/B load revision1; A có edit chưa lưu; B save thành revision2; A save bằng state1 vẫn200/revision3, bodyB bị ghi đè không báo xung đột. Hai chiều đều FAIL.

Bổ sung expected revision/concurrency contract hoặc giải pháp tương đương, backend atomic check và response conflict đúng nghiệp vụ; adapters/mock/DTO/tests cùng version. UI giữ bản đang gõ và cho người viết xem/reconcile, không tự retry ghi đè, tự merge tâm sự hoặc bỏ bản của client kia. Phối hợp thay đổi F06/shared tối thiểu vì đây là boundary F04; không viện tên folder để bỏ lỗi. Kiểm migration drift, MySQL khi có môi trường, backcompat rõ ràng không lặng lẽ bỏ field.

## 6. N04/N05 và yêu cầu giao diện

- N04/P2: Mini đăng nhập caregiver vẫn hardcode “Lời con muốn gửi” và placeholder “...của con...”; web đã có copy caregiver. Chọn copy theo vai server đã xác minh, dùng lời trung tính như “Lời bạn muốn gửi”, không mặc định mẹ/bố hoặc xưng thay. Cả compose/AI/reply cần nhất quán. Không dựa role UI để cấp quyền backend.
- N05/P2: nút Đổi người nhận ~68×36px trên cả hai client. Vùng chạm thực >=44×44, focus và spacing đủ; đo bounding box thật, không test chỉ tìm chuỗi min-height trong CSS.
- Font-only CSS stress200% ở390px tràn459px web/445px Mini. Đây chưa là native-Zalo/Chrome zoom evidence: thực hiện reflow/large text đúng môi trường, giữ consent/nút gửi/help tới được bằng cuộn và sửa overflow có ý nghĩa. Ghi rõ cách đo, đừng gọi stress probe là device certification.
- Đối chiếu đủ 28 frame trong matrix. Bốn web frames không là lý do bỏ state Mini. Dùng skill UI/design phù hợp để bổ sung state; không nhất thiết tạo route riêng cho mỗi frame. Hai mặt giao diện chính: web/ và zalo-mini-app/, cùng Django API. Compose, mailbox, message detail/reply + consent/recipient/preview/loading/error/stale/pause/receipt là các nhóm cần có và dùng được.
- 20 frame Mini liên quan F04 có 4 biến thể bàn phím cần device evidence. Caregiver hub là cross-feature/reference; 3 booking/call frames thuộc F12, không fake booking hoặc xây dịch vụ tư vấn ngoài scope để đủ số trang. Không sao chép claim trị liệu, riêng tư tuyệt đối, mã hóa cục bộ hoặc quota/đã đọc không có backend.
- Lập mapping frame→actor→route/state/component→API/DTO→evidence→status cho cả web/Mini. Giữ logo thật, màu/typography Việt và accessibility. Đừng đánh dấu PASS mọi frame chỉ vì source-level test xanh.

## 7. Luồng API thật, Gemini và invariants phải giữ

Web và Mini dùng cùng API backend Django trên Render khi release; shared HTTP adapter là nguồn contract, không thêm Message/send path thứ hai. Test demo không chứng minh integration. VITE_API_BASE_URL là public backend origin; không là URL provider và không chứa secret.

Backend-only Gemini: GEMINI_API_KEY ở server env/secret manager; GEMINI_MODEL theo allowlist hiện hành; FB_AI_ENABLED kill switch mặc định an toàn; GEMINI_TIMEOUT_SECONDS/GEMINI_MAX_OUTPUT_TOKENS theo bounds của repo. Thiếu/sai config không crash Django, không gọi mạng tại import/startup/health; AI off/error vẫn viết/lưu/preview/send/help bình thường. Không dùng key lộ trong ảnh/chat, không commit token/.env thật, không gọi Gemini trực tiếp từ Mini/web. CORS đúng hai origin, preflight authorization/content-type/x-idempotency-key; production DEBUG/hosts/TLS theo repo.

Consent/disclosure trước provider call, purpose/policy đúng phiên bản, withdraw/kill-switch/inflight guard; provider là bên xử lý kỹ thuật. Writer đọc/sửa/bỏ/thử lại theo giới hạn và tự chọn quyết định cuối. AI không thêm facts/promises/commitments/intentions/events/assumptions, không chẩn đoán/điều trị hoặc tự gọi/gửi/liên hệ. Output untrusted, render text, không innerHTML/tools/DB access.

Recipient chỉ được final đã duyệt; không original, intermediate suggestions hoặc history, kể cả qua nhầm body/recipient/cache/DTO. Suggestions author-only, không staff/admin bypass. F06 giữ nháp và pause300 server; edit/AI không ngầm reset/hủy pause; hết giờ/AI/retry/resume không auto-send. Help không bị timer/quota khóa. F15 completed deletion phải chặn late completion và claim reuse/TTL/restore; giữ N02 identity/hash fence và provider ngoài transaction.

## 8. Kiểm thử, bằng chứng và điều kiện hoàn thành

Tạo test đỏ cho N03/N06/N04/N05 trước fix, không chỉ mirror implementation. Giữ regression N01/N02/R01–R05. Chạy backend foundation/check/migrations, harness F04/F05/F06/F15 và boundary, web/Mini/shared/mobile/qa-f04, explicit test_f04_contract_a5.mjs (không khớp glob *.test.mjs), builds/assets/import/docs checker. Kiểm return code và số test thật, không coi helper exit0 là PASS khi JSON finding vẫn true.

Browser phải đi qua HTTP adapter + Django + F05 thật, đọc final bằng recipient session thật, hai vai×hai client. Không fake response để chứng minh flow; có thể fake provider/fault/delay và ghi rõ. Chạy cross-client recipient + stale save, consent decline/revoke, loading/cancel, stale accept, save failure, AI timeout/503/429/off, manual continuation, send double-click, unknown outcome, pause299/300, offline/resume và logout stale cleanup đúng scope. Chụp sending/sent/unknown nếu muốn claim các UI states đã visual-reviewed; audit mới có delivery evidence nhưng chưa đủ ảnh mọi receipt state.

Responsive320/360/390/430/768/1024/1440 phù hợp client; large text200%, keyboard/focus/Escape/reduced motion/touch/hidden visibility; Zalo Android/iOS thật trước claim device-ready. Local browser không phải Zalo SDK auth/device test.

Gemini quality: tạo corpus synthetic hai vai có expected facts/intent + forbidden additions, kiểm tình huống emotional/confrontational/context và lỗi provider. Chỉ live khi có key mới được quản lý và budget/scope hợp lệ; không đưa dữ liệu người thật. Không có key/device/MySQL/Render thì hoàn thành code/test/docs độc lập trước, ghi external blocker chứng minh được và lệnh chạy tiếp; không giả pass hoặc tự deploy sản xuất.

Cập nhật report/manifest/peer-review/UI matrix theo một SHA kiểm được. Xóa claim working-tree/chờ A2/count cũ khỏi trạng thái hiện hành, giữ lịch sử riêng. Mỗi finding có expected/actual, owner, fix SHA, command, evidence và reviewer. Không đổi assertion/skip để lách lỗi; không tự hạ scope hoặc deferred phase2 cho N03/N06.

Code verified locally chỉ khi hết P1/P2 trong scope và các regression/2 vòng peer review qua. Release ready cần thêm Gemini quality/MySQL/Render/device/policy thực tế; thiếu thì ghi rõ CODE_VERIFIED_LOCALLY — RELEASE_BLOCKED_EXTERNAL, không gọi F04 hoàn tất.

## 9. Bàn giao

Commit code trên nhánh F04 của family-bridge, PR theo quy tắc repo; không tự merge/deploy. Docs/ảnh/prompt/evidence cập nhật chỉ F04-docx trong f07-docx, không main/F07. Rebuild catalog/checksum và verify trước đóng ZIP/push. Nếu Git auth bị chặn thì bàn giao ZIP/bundle, không bịa remote success và không dừng việc code vì blocker tài liệu.

Cuối cùng trả commit/PR URLs thực, test/evidence summary, state matrix, finding closure và bước test thủ công ngắn cho từng client. Không gửi localhost giả là Render hoặc QR browser giả là Zalo Mini App đã deploy. Tiếp tục sửa các việc được giao đến khi đạt điều kiện trên; chỉ phần thực sự phụ thuộc bên ngoài mới được dừng với blocker rõ ràng.
