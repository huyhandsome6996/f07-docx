# Các finding còn mở trên bb75b2c

Chỉ kiểm tra local với dữ liệu tổng hợp. Mức ưu tiên dưới đây dành cho nhánh chưa nghiệm thu; không khẳng định các hành vi này có trên production.

## R01 — Cao: preview riêng tư còn trên trang khác và sau khi xóa phiên

**Nguồn:** `zalo-mini-app/src/pages/mood/index.js`, đặc biệt `cleanupFn`, `openDialogs` và `openShareSheet`; `createSheet` gắn overlay vào `document.body`. Cần rà cả lifecycle `mood-shared/index.js`.

**Quan sát:** đăng nhập HS bằng form thật, mở `/mood`, mở sheet chia sẻ một mục synthetic. Đổi hash sang `/help`: sheet và ghi chú vẫn còn. Gọi `clearSession()` từ module phiên thực rồi chuyển `/login`: sheet và ghi chú vẫn nằm trên màn đăng nhập. Thao tác xóa phiên trong bộ tái hiện là gọi module phiên để cô lập lifecycle; chưa đồng nghĩa đã kiểm mọi nút logout của ứng dụng.

**Nguyên nhân:** tập `openDialogs` được tạo nhưng sheet/dialog không được đăng ký vào đó; `cancelled`/`runId` không được dùng trong các callback. Destroy của trang không gỡ overlay chứa preview.

**Bằng chứng:** `evidence/browser-review.log`, `evidence/browser/r01-after-session-clear.png`; 3 kiểm tra lifecycle đều FAIL.

**Tiêu chí sửa:** track và đóng sheet/dialog khi rời trang, logout, đổi actor hoặc session generation; xóa preview/private DOM; bỏ phản hồi đến muộn và callback ghi sau destroy. Thêm regression cho page.destroy, hash navigation thật, nút logout thật, actor switch và request trả chậm. Không chỉ ẩn overlay bằng CSS. Giữ hành vi sau revoke/unlink/resume đúng contract. Liên quan F07-23, SEC-08/10, DSA-09/10.

## R02 — Cao: hai lần sửa đồng thời dùng lại revision, grant đọc được nội dung chưa duyệt

**Nguồn:** `packages/family_bridge_features/f07_mood/services/mood.py`, `MoodEntryService.edit` và ranh giới transaction của `MoodShareService.share`.

**Quan sát MySQL 8.4.11:** hai transaction đọc cùng revision 1. Lần sửa A commit revision 2, owner share đúng revision 2 đã xem trước. Lần sửa B sau đó ghi note khác nhưng vẫn revision 2. Recipient đọc qua service thật được note B chưa được duyệt chia sẻ. Log: `final_revision=2 unapproved_readable=True`.

**Nguyên nhân:** `@transaction.atomic` không tự khóa SELECT. Đọc model rồi `revision += 1; save()` cho phép lost update. Kiểm tra revision trước transaction chia sẻ cũng cần đối chiếu với quy tắc khóa hiện hành.

**Bằng chứng:** `repro/review_regressions.py`, test `test_R02_concurrent_edits_cannot_reuse_shared_revision`; `evidence/independent-mysql-regressions.log`.

**Giới hạn tái hiện:** test dùng model, DB, connection reader, edit/share/read thật. Chỉ patch điểm đọc để điều phối thứ tự hai luồng; không mock nội dung, quyền hoặc persistence. Có chờ giới hạn để cách sửa dùng row lock vẫn có thể hoàn tất.

**Tiêu chí sửa:** dùng khóa hàng hoặc optimistic concurrency có kiểm tra ở DB; không tái sử dụng revision cho hai nội dung khác nhau. Kiểm tra expected_revision và tạo/rebind grant trong cùng ranh giới đồng bộ với edit. Hai lần sửa thành công phải có revision phân biệt; nếu từ chối stale, lỗi phải theo contract và client giữ nháp. Mọi recipient read phải chặn nội dung chưa được duyệt lại. Chạy regression trên MySQL thật, gồm edit/edit và edit/share; không sửa test thành chấp nhận lộ nội dung. Liên quan F07-06/13/14/18, SEC-07/08/15, DSA-08.

## R03 — Trung bình: một recipient nhận từ hai owner nhưng chỉ thấy một owner

**Nguồn:** `MoodShareService._connections_current` cache connection bằng `recipient_id`; `list_shared_with_me` gọi helper cho các row thuộc nhiều owner.

**Quan sát:** tạo 2 owner, cùng recipient và 2 canonical active connections thật, mỗi owner share một mục. Cả hai mục đều đọc được riêng bằng `read_shared`; list trả đúng 1 mục thay vì 2. Tái hiện trên SQLite và MySQL.

**Nguyên nhân:** trong recipient list, `recipient_id` giống nhau cho mọi row. Connection của cặp đầu tiên bị dùng lại khi xét owner tiếp theo. Đây là bỏ sót mục hợp lệ trong test này; không có bằng chứng helper làm lộ note trái quyền.

**Bằng chứng:** test `test_R03_recipient_lists_grants_from_two_owners`; log `individually_readable=2 listed=1 expected=2`.

**Tiêu chí sửa:** khóa cache phải đại diện đủ cặp owner/recipient; không dùng lại verdict giữa hai cặp. Kiểm tra nhiều owner, nhiều mục/cursor, một connection bị revoke và connection generation mới; giữ bounds/query count hợp lý. Liên quan F07-08/15/19.

## R04 — Trung bình: MySQL race test sai kỳ vọng và báo cáo đếm sai

**Nguồn:** `packages/family_bridge_features/f07_mood/tests/test_race_mysql.py:62` và handover verification report.

**Quan sát:** F07 MySQL chạy 42 tests: **41 PASS, 1 FAIL, 0 skip**. Test tạo đồng thời đã xác nhận 1 row và kết quả đúng `created` + `InputInvalid`, nhưng so sánh `sorted(outcomes)` với danh sách chưa sort `['created', 'InputInvalid']`. Kết quả Python là `['InputInvalid', 'created']`, nên assertion sai. Điều này không chứng minh business create bị lỗi.

**Tiêu chí sửa:** so sánh multiset bằng `assertCountEqual` hoặc sort cả hai; vẫn giữ assertion số row và lỗi nghiệp vụ. Kiểm tra outcomes của cả hai worker trong share-race test, giới hạn thời gian chờ và dọn DB connection theo luồng; không bỏ qua lỗi worker.

**Sửa tài liệu:** module SQLite là **42 tổng = 40 PASS + 2 SKIPPED**, không phải 42 PASS cộng thêm 2 skip. Full harness **523 tổng = 512 PASS + 11 SKIPPED**. Mini App ở cùng SHA thực tế **307 PASS**, không phải 306 trong báo cáo. Sau sửa phải ghi lại số mới từ runner, không cộng các lượt chạy lặp thành một tổng duy nhất.

**Bằng chứng:** `evidence/f07-mysql-tests.log`, `evidence/f07-sqlite-tests.log`, `evidence/full-harness.log`, `evidence/miniapp-tests.log`.

## R05 — Trung bình: API âm thầm cắt ngày không hợp lệ

**Nguồn:** `parse_entry_date` gọi `date.fromisoformat(value[:10])`.

**Quan sát:** POST một `entry_date` bằng ngày hợp lệ nối thêm hậu tố `-not-an-ISO-date` trả 201 và lưu phần 10 ký tự đầu, thay vì từ chối định dạng. Cùng kết quả qua actual API view trên SQLite và MySQL; force-authenticate chỉ cô lập validation, không phải bằng chứng xác thực.

**Tiêu chí sửa:** validate toàn chuỗi theo định dạng API công bố; không cắt thầm. Giữ chính sách ngày VN/bounds hiện hành và thêm test suffix, timestamp, chuỗi dài, ngày không tồn tại, ngày biên. Phân biệt kiểu date nội bộ với JSON string đầu vào. Liên quan F07-07, SEC-11.

## R06 — Trung bình: chữ lớn làm tràn ngang ở viewport 320 và 390

**Nguồn quan sát:** trang `/mood`, chip `fb-mood`/`fb-mood__label` trong grid 4 cột. Không tự suy rằng cần sửa CSS shared thay vì lớp F07.

**Phương pháp:** Chromium thật, UI/API local; đo 320/390/430 CSS px. Với cỡ chữ bình thường cả 3 không tràn. Sau khi tăng font-size và line-height của phần tử văn bản lên 200% bằng CSS, content width ở 320 và 390 đều lên **395px**, gây cuộn ngang; 430 vẫn không tràn.

**Bằng chứng:** `evidence/browser-review.log`, ảnh `evidence/browser/layout-*-css-text-200.png`.

**Tiêu chí sửa:** label/chip co giãn, xuống dòng hoặc đổi số cột khi cần; không thu chữ hoặc cắt nhãn để làm xanh phép đo. Đọc/chọn được đầy đủ ở chữ lớn, keyboard/focus/help vẫn hoạt động. Kiểm tra lại cả sheet. Đây là mô phỏng text scaling bằng CSS trong browser, chưa phải kiểm tra text scaling hệ điều hành hay Zalo Android/iOS. Liên quan F07-25 và UI rules.
