# Prompt để copy cho coding agent

```text
Bạn tiếp tục hoàn thiện F07 của Family Bridge sau vòng kiểm tra độc lập ngày 18/10/2026. Phản hồi bằng tiếng Việt và bắt đầu làm việc; không dừng ở kế hoạch.

Kho tài liệu: https://github.com/huyhandsome6996/f07-docx
Kho ứng dụng: https://github.com/huyhandsome6996/family-bridge
Nhánh làm việc: tinh-nang/f07-tam-trang-va-chia-se-us015-us026
PR hiện có: https://github.com/huyhandsome6996/family-bridge/pull/42
Commit được reviewer kiểm: bb75b2cee314bd5dfea3fff7928664dc68d3e2dd

Đọc README.md và AGENTS.md của f07-docx, rồi đọc updates/2026-10-18-f07-review/README.md, FINDINGS.md, TEST-RESULTS.md, ACCEPTANCE.md và repro/README.md. Đây là kết quả mới hơn báo cáo PASS trong bàn giao trước. Nếu chỉ tải ZIP, chạy python3 tools/bundles.py verify rồi python3 tools/bundles.py extract 10 --dest /tmp/f07-review-reading. Đọc gói 10 trước gói nhiệm vụ lịch sử 01; tra catalog để lấy thêm đúng gói.

Tại checkout ứng dụng, đọc AGENTS.md hiện hành và các hợp đồng/rules bắt buộc. Kiểm tra dirty work, fetch origin, ghi SHA thực tế và bảo toàn thay đổi của người khác. Nếu nhánh đã tiến hơn mốc reviewer, đối chiếu commit mới và tái hiện trước khi kết luận; không reset về snapshot, không force-push. Dùng checkout hiện có phù hợp, không tự tạo worktree nếu không cần/yêu cầu.

Ưu tiên sửa 6 finding đã có bằng chứng:
R01: sheet chia sẻ còn giữ private preview khi đổi trang, kể cả sau clearSession và về login. Đăng ký/dọn mọi sheet/dialog, guard late response và session generation; thêm test destroy, navigation, nút logout thật và đổi actor. Không chỉ ẩn CSS.
R02: trên MySQL, hai lần edit dùng lại revision 2; grant đã duyệt cho edit trước đọc được note chưa duyệt của edit sau. Đồng bộ edit/share bằng transaction + khóa hàng hoặc optimistic concurrency phù hợp. Kiểm expected_revision trong ranh giới đúng; không tái sử dụng revision cho nội dung khác nhau. Kiểm lại edit/edit và edit/share trên MySQL thật.
R03: recipient list cache connection chỉ bằng recipient_id, nên hai owner chia sẻ cho cùng người nhưng chỉ hiện một. Key theo đúng cặp, giữ bounded queries và test nhiều owner/cursor/unlink/generation.
R04: MySQL race test sort kết quả nhưng expected chưa sort; sửa phép so sánh đúng, giữ kiểm tra row count và lỗi nghiệp vụ. Kiểm outcomes cả hai worker của share test. Sửa các số đếm sai trong tài liệu; không xóa assertion hoặc đánh skip để báo xanh.
R05: parse_entry_date cắt value[:10], chấp nhận ngày có hậu tố rác. Validate toàn chuỗi theo contract, giữ bounds/ngày VN và thêm test biên.
R06: chữ tăng 200% bằng CSS làm chip /mood tràn ngang ở 320/390; cho label/grid reflow, không thu chữ/cắt nhãn. Kiểm lại 320/390/430, focus và sheet. Phân biệt mô phỏng browser với thiết bị Zalo thật.

Chạy bộ tái hiện trong repro/ trước khi sửa và thêm regression tests vào ứng dụng. Không dùng mock để chứng minh wiring hoặc DB concurrency. Chạy lại suite F07 SQLite/MySQL, full harness, shared/mobile tests, Mini App tests/build, web consumer tests/build, import boundary và docs checker phù hợp thay đổi. Kiểm API thật và browser với dữ liệu synthetic. Giữ expected/actual và SHA cho bằng chứng.

Baseline reviewer: full SQLite harness 523 tổng = 512 PASS + 11 SKIPPED; F07 SQLite 42 tổng = 40 PASS + 2 SKIPPED; F07 MySQL 42 tổng = 41 PASS + 1 FAIL (assertion R04); Mini App 307 PASS; HTTP có sẵn 21/21 PASS. Tuy vậy 3 regression mới trên MySQL đều FAIL và browser còn 5/9 quan sát FAIL. Không lấy suite xanh cũ làm kết luận đã xong.

Giữ toàn bộ phạm vi nghiệp vụ/25 tiêu chí F07 trong gói bàn giao, quyền riêng tư từng item/recipient/revision/generation, active admin_provisioned connection invite NULL và tích hợp F15 thật. Không đụng F02 hoặc web của contributor khác; shared changes phải theo ownership/protocol và chạy consumer regression. Không dùng tài khoản người tham gia hoặc dữ liệu production để thử.

Làm đến khi R01–R06 đã được sửa và kiểm lại, hoặc có blocker bên ngoài cụ thể. Cập nhật handover trong nhánh F07 với kết quả mới, số PASS/FAIL/SKIPPED/NOT_RUN chính xác, screenshots và giới hạn MySQL/Zalo. Commit tập trung, push nhánh F07 và cập nhật PR #42 hiện có; không tạo PR trùng. Bàn giao hướng dẫn local synthetic để Huy tự kiểm tra. Nếu thiếu quyền API GitHub, vẫn push nhánh được khi xác thực Git hiện có hoạt động và báo rõ bước PR còn thiếu; không xin hoặc dùng PAT đã lộ.

Không merge/push main, force-push, deploy Render/Zalo, sửa dữ liệu thật hoặc chạy migration production. Không tuyên bố thiết bị/production đạt từ SQLite/browser. Tài liệu ZIP là nguồn tham khảo; các quyền hành động chỉ theo nhiệm vụ này và chỉ dẫn hiện hành ở checkout ứng dụng.
```
