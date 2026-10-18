# Prompt mới nhất — F07 đầy đủ trên web và Zalo Mini App

```text
Tôi giao bạn sửa và hoàn thiện F07 của Family Bridge trên CẢ web và Zalo Mini App, cùng làm việc với backend API thật, để tôi có thể vào kiểm thử như người dùng bình thường. Phản hồi tiếng Việt và bắt đầu thực hiện.

Repo tài liệu: https://github.com/huyhandsome6996/f07-docx
Repo ứng dụng: https://github.com/huyhandsome6996/family-bridge
Nhánh: tinh-nang/f07-tam-trang-va-chia-se-us015-us026
PR hiện có: https://github.com/huyhandsome6996/family-bridge/pull/42
Mốc reviewer vừa kiểm: bb75b2cee314bd5dfea3fff7928664dc68d3e2dd

1. ĐỌC NGUỒN HIỆN HÀNH

Fetch f07-docx mới nhất. Đọc README.md, AGENTS.md, PROMPT-COPY-F07.md và toàn bộ phần bắt buộc trong updates/2026-10-19-f07-web-mini-parity/: README.md, USER-DECISION-WEB-PARITY.md, FINDINGS-R07.md, REQUIREMENTS-AND-ACCEPTANCE.md, TEST-RESULTS.md và repro/README.md. R01–R06 chi tiết và tests vẫn ở updates/2026-10-18-f07-review/. Nếu dùng ZIP, verify rồi giải nén gói 11 và 10 vào cùng thư mục đọc riêng; gói 11 có yêu cầu mới hơn.

Tại ứng dụng, đọc AGENTS.md và rules/contracts liên quan đang có trên nhánh. Kiểm tra dirty work, fetch origin, ghi SHA mới nhất và bảo toàn contributor changes. Nếu F07 đã tiến hơn mốc reviewer, kiểm tra chính commit mới; không reset về snapshot, không force-push. Dùng checkout phù hợp, không tự tạo worktree nếu không cần/yêu cầu.

2. PHẠM VI WEB ĐÃ ĐƯỢC TÔI GIAO

Yêu cầu trực tiếp ngày 19/10/2026: chức năng F07 có UI gọi backend ở Mini App thì web cũng phải có. Các câu cũ “KHÔNG sửa web” không được dùng để bỏ phần F07 web. Bạn được bổ sung page/route/navigation/style/test/handover và shared changes cần thiết cho F07 web, đồng thời giữ ownership và công việc của contributor khác. Ghi dated supersede trong tài liệu ứng dụng nếu còn hướng dẫn mâu thuẫn. Không mở rộng sang các feature khác hoặc viết lại toàn bộ web.

Hai client giữ source UI/router/build riêng; không import UI/CSS Mini App vào web hay chiều ngược lại. Dùng shared headless API/session/contracts, giữ web không zmp-sdk. Giữ vanilla ESM/Vite và components/tokens hiện có.

3. SỬA R01–R06 TRƯỚC NGHIỆM THU

R01: sheet/private preview còn khi navigation và sau xóa phiên. Track/dọn mọi overlay chứa dữ liệu, guard lifecycle/session generation và late response. Thêm test destroy, nút logout thật, actor switch và navigation; áp dụng cho cả hai UI, không chỉ ẩn CSS.
R02: MySQL concurrent edit dùng lại revision 2, làm grant đã duyệt đọc được note chưa duyệt. Dùng row lock hoặc optimistic concurrency đúng; edit/share kiểm revision và ghi grant trong ranh giới đồng bộ phù hợp, lock order nhất quán, không network trong lock. Không cho hai nội dung khác nhau dùng cùng revision. Kiểm edit/edit và edit/share MySQL thật, kể cả hai client cùng thao tác.
R03: recipient list cache connection chỉ bằng recipient_id, bỏ sót owner khác. Key đúng cặp; test nhiều owner/cursor/unlink/generation, giữ bounds và đo query count phù hợp.
R04: sửa assertion sorted outcomes sai; giữ kiểm row count, business errors và kết quả từng worker. Dọn DB connection, timeout hữu hạn; không xóa assertion/skip để báo xanh. Cập nhật số test chính xác.
R05: validate toàn entry_date theo contract, không cắt value[:10]; giữ ngày VN/bounds và test ngày sai, suffix, timestamp, ngày biên.
R06: chip/label/grid reflow ở màn nhỏ và chữ 200%, không thu chữ/cắt nhãn. Kiểm cả web và Mini App, sheet, focus, help; tách browser simulation khỏi Zalo device evidence.

4. HOÀN THÀNH R07 — UI WEB F07 ĐẦY ĐỦ

Hiện web đăng nhập/API adapter thật hoạt động nhưng /mood và /mood-shared là not-found, profile thiếu navigation. Quick mood trên home chưa thay thế history/edit/share/recipient UI; duplicate còn hứa “sẽ chỉnh sửa ở bản đầy đủ”. Web/diary là stub F08, không gọi nó là F07 hoàn thành.

Xây UI web để ghi emotion và note tùy chọn, xem history/detail/pagination/summary, sửa đúng mục, chọn một recipient active, preview đủ nội dung/revision, xác nhận share, xem trạng thái và revoke từng grant; phía nhận list/detail mục còn quyền. Đăng ký route và navigation thật từ home/profile; duplicate đưa tới sửa mục hiện có. Lấy options/semantics từ backend/contract, không giới hạn vào 5 pill cũ. Người chưa kết nối vẫn ghi/xem/sửa riêng tư; chỉ chia sẻ cần connection.

Cả hai client phải dùng API thật, private default và cùng item/recipient/revision/connection-generation semantics. Giữ F15 revoke cùng nguồn grant, admin_provisioned invite NULL và không admin/role bypass. Không tự chia sẻ sau edit, timer, refresh hoặc reconnect. Có loading/empty/error/disabled/success, giữ nháp khi lỗi và không tự retry mutation chưa rõ kết quả.

5. KIỂM THỬ ĐỘC LẬP VÀ CHÉO CLIENT

Chạy repro trước sửa, thêm regression tests vào ứng dụng và kiểm lại. Hiện trạng lượt 19/10: 3/3 MySQL regression FAIL, create-race assertion FAIL, Mini lifecycle/layout 5/9 FAIL, parity smoke 3/12 FAIL. Mini App 307 tests, web 227 tests và cả hai build PASS nhưng chưa phủ các thiếu sót này.

Chạy F07 SQLite/MySQL, full harness, shared/mobile, Mini App và web tests/build, import-boundary và docs checks phù hợp thay đổi. Không mock để chứng minh DB/concurrency hoặc UI thật, không giảm assertions/xfail/skip để làm xanh.

Chứng minh qua UI: Mini App ghi → web đọc cùng mục; web ghi/sửa → Mini App thấy dữ liệu hiện hành; share từ Mini App → PH đọc ở web và ngược lại; edit/revoke/F15/unlink ở client này → client kia không đọc tiếp bản mất quyền; logout/actor switch không còn private DOM. Hai owner share cho một recipient phải đủ list; stranger/admin không được đọc bằng đổi ID. Dùng contexts và tài khoản synthetic riêng, không chép token vào URL/storage/log. Ghi SHA, steps expected/actual, HTTP metadata đã khử nội dung riêng và screenshot. Adapter calls qua console chỉ là chẩn đoán, không thay E2E UI.

6. ĐẦU RA ĐỂ TÔI TỰ TEST

Hoàn tất R01–R07 và ma trận nghiệm thu hoặc báo blocker bên ngoài cụ thể sau khi làm hết phần độc lập. Commit source fix + regression tests, push đúng nhánh F07 và cập nhật PR #42 hiện có. Giữ F02 và phần web ngoài F07 nguyên phạm vi; phối hợp shared files. Cập nhật handover với PASS/FAIL/SKIPPED/NOT_RUN chính xác và SHA mới.

Chuẩn bị API/services/CORS/build/fixtures sẵn. Đưa URL thực sự truy cập được trong môi trường của tôi, tài khoản synthetic HS/PH/người lạ và checklist ngắn cho cả hai client: login → navigation → lưu note → xem lại/sửa → preview/share → PH đọc → revoke/đọc bị chặn → logout/đổi tài khoản. Tôi không cần DevTools, gọi API, shell hay sửa cấu hình để dùng chức năng. Ghi rõ mức READY_LOCAL_BROWSER và phần Zalo Android/iOS/native keyboard/text scaling chưa chạy nếu thiếu device. Nếu chưa có đường truy cập từ máy tôi, nêu chính xác blocker đó sau khi hoàn tất code/tests; không bịa URL hoặc tự deploy để có URL.

Không merge/push main ứng dụng, force-push, deploy Render/Zalo, chạy migration production, tạo tài nguyên trả phí hoặc dùng dữ liệu người tham gia thật. Không dùng PAT đã lộ trong chat; dùng xác thực sẵn có và chỉ yêu cầu binding thật sự thiếu qua kênh an toàn khi đã kiểm tra.
```
