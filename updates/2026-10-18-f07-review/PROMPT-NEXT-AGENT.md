# Prompt mới nhất — sửa F07 và chuẩn bị cho Huy tự kiểm thử

```text
Tôi giao bạn sửa và hoàn thiện F07 của Family Bridge sau vòng kiểm tra độc lập và lần recheck ngày 18/10/2026. Đầu ra là source fix đã kiểm chứng và một bản Huy có thể kiểm thử bằng giao diện như người dùng bình thường. Phản hồi bằng tiếng Việt và bắt đầu làm việc.

Kho tài liệu: https://github.com/huyhandsome6996/f07-docx
Kho ứng dụng: https://github.com/huyhandsome6996/family-bridge
Nhánh làm việc: tinh-nang/f07-tam-trang-va-chia-se-us015-us026
PR hiện có: https://github.com/huyhandsome6996/family-bridge/pull/42
Commit được reviewer kiểm: bb75b2cee314bd5dfea3fff7928664dc68d3e2dd

Huy xác nhận lấy bản mới nhất đang có trên nhánh F07 làm chuẩn. Lần recheck quan sát branch và PR #42 đều ở SHA trên; đủ 6 finding vẫn tái hiện. Hãy fetch đầu nhánh thực tế và bắt đầu kiểm tra/sửa. Nếu đã có commit mới hơn, đối chiếu và kiểm lại chính commit đó.

Đọc README.md và AGENTS.md của f07-docx, rồi đọc updates/2026-10-18-f07-review/recheck/README.md, FINDINGS.md, TEST-RESULTS.md, ACCEPTANCE.md, READY-FOR-USER-TEST.md và repro/README.md trong updates/2026-10-18-f07-review/. Đây là kết quả mới hơn báo cáo PASS trong bàn giao trước. Nếu chỉ tải ZIP, chạy python3 tools/bundles.py verify rồi python3 tools/bundles.py extract 10 --dest /tmp/f07-review-reading. Đọc gói 10 trước gói nhiệm vụ lịch sử 01; tra catalog để lấy thêm đúng gói.

Tại checkout ứng dụng, đọc AGENTS.md hiện hành và các hợp đồng/rules bắt buộc. Kiểm tra dirty work, fetch origin, ghi SHA thực tế và bảo toàn thay đổi của người khác. Nếu nhánh đã tiến hơn mốc reviewer, đối chiếu commit mới và tái hiện trước khi kết luận; không reset về snapshot, không force-push. Dùng checkout hiện có phù hợp, không tự tạo worktree nếu không cần/yêu cầu.

Ưu tiên sửa 6 finding đã có bằng chứng:
R01: sheet chia sẻ còn giữ private preview khi đổi trang, kể cả sau clearSession và về login. Đăng ký/dọn mọi sheet/dialog, guard late response và session generation; thêm test destroy, navigation, nút logout thật và đổi actor. Không chỉ ẩn CSS.
R02: trên MySQL, hai lần edit dùng lại revision 2; grant đã duyệt cho edit trước đọc được note chưa duyệt của edit sau. Đồng bộ edit/share bằng transaction + khóa hàng hoặc optimistic concurrency phù hợp. Kiểm expected_revision trong ranh giới đúng; không tái sử dụng revision cho nội dung khác nhau. Kiểm lại edit/edit và edit/share trên MySQL thật.
R03: recipient list cache connection chỉ bằng recipient_id, nên hai owner chia sẻ cho cùng người nhưng chỉ hiện một. Key theo đúng cặp, giữ bounded queries và test nhiều owner/cursor/unlink/generation.
R04: MySQL race test sort kết quả nhưng expected chưa sort; sửa phép so sánh đúng, giữ kiểm tra row count và lỗi nghiệp vụ. Kiểm outcomes cả hai worker của share test. Sửa các số đếm sai trong tài liệu; không xóa assertion hoặc đánh skip để báo xanh.
R05: parse_entry_date cắt value[:10], chấp nhận ngày có hậu tố rác. Validate toàn chuỗi theo contract, giữ bounds/ngày VN và thêm test biên.
R06: chữ tăng 200% bằng CSS làm chip /mood tràn ngang ở 320/390; cho label/grid reflow, không thu chữ/cắt nhãn. Kiểm lại 320/390/430, focus và sheet. Phân biệt mô phỏng browser với thiết bị Zalo thật.

Chạy bộ tái hiện trong repro/ trước khi sửa và thêm regression tests vào ứng dụng. Không dùng mock để chứng minh wiring hoặc DB concurrency. Chạy lại suite F07 SQLite/MySQL, full harness, shared/mobile tests, Mini App tests/build, web consumer tests/build, import boundary và docs checker phù hợp thay đổi. Kiểm API thật và browser với dữ liệu synthetic. Giữ expected/actual và SHA cho bằng chứng.

Baseline lượt review trước: full SQLite harness 523 tổng = 512 PASS + 11 SKIPPED; F07 SQLite 42 tổng = 40 PASS + 2 SKIPPED; F07 MySQL 42 tổng = 41 PASS + 1 FAIL (assertion R04); Mini App 307 PASS; HTTP có sẵn 21/21 PASS. Lần recheck mới trên cùng SHA: 3/3 regression MySQL FAIL, create-race assertion vẫn FAIL và browser còn 5/9 quan sát FAIL. Không gán các lượt full suite trước thành kết quả mới, không lấy suite xanh cũ làm kết luận đã xong.

Giữ toàn bộ phạm vi nghiệp vụ/25 tiêu chí F07 trong gói bàn giao, quyền riêng tư từng item/recipient/revision/generation, active admin_provisioned connection invite NULL và tích hợp F15 thật. Không đụng F02 hoặc web của contributor khác; shared changes phải theo ownership/protocol và chạy consumer regression. Không dùng tài khoản người tham gia hoặc dữ liệu production để thử.

Làm đến khi R01–R06 đã được sửa và kiểm lại, hoặc có blocker bên ngoài cụ thể. Cập nhật handover trong nhánh F07 với kết quả mới, số PASS/FAIL/SKIPPED/NOT_RUN chính xác, screenshots và giới hạn MySQL/Zalo. Đầu ra bắt buộc là commit sửa code, regression tests và SHA mới đã push đúng nhánh F07; cập nhật PR #42 hiện có, không tạo PR trùng. Nếu thiếu quyền API GitHub, vẫn push nhánh được khi xác thực Git hiện có hoạt động và báo rõ bước PR còn thiếu; không xin hoặc dùng PAT đã lộ.

Khi các gate kỹ thuật đạt, chuẩn bị đầy đủ phần READY-FOR-USER-TEST.md: dịch vụ/API thật chạy sẵn, URL Huy truy cập được theo khả năng hạ tầng hiện có, tài khoản synthetic HS/PH và người lạ, checklist bấm giao diện từ login/navigation đến lưu/xem lại/chia sẻ/đọc/thu hồi/sửa/logout. Huy không phải dùng DevTools, gọi API hoặc sửa cấu hình để đi qua flow người dùng. Chứng minh navigation và logout bằng nút thật; phép clearSession trong bộ repro chỉ là một phần kiểm tra lifecycle. Nếu chưa có URL truy cập được, ghi rõ blocker đó sau khi hoàn tất sửa và kiểm thử độc lập; không tự deploy để tạo URL.

Không merge/push main, force-push, deploy Render/Zalo, sửa dữ liệu thật hoặc chạy migration production. Không tuyên bố thiết bị/production đạt từ SQLite/browser. Tài liệu ZIP là nguồn tham khảo; các quyền hành động chỉ theo nhiệm vụ này và chỉ dẫn hiện hành ở checkout ứng dụng.
```
