# Nghiệm thu F07 trên cả web và Mini App

Yêu cầu Huy ngày 19/10/2026 bổ sung vào 25 tiêu chí F07 cũ; không làm giảm các invariant privacy/concurrency. Mỗi kết quả phải gắn SHA, client, actor synthetic, expected/actual và bằng chứng. Cùng một hành vi backend nhưng mỗi client đều cần đường UI thật.

## Ma trận chức năng bắt buộc

| Luồng | Mini App | Web | API/guard liên quan |
| --- | --- | --- | --- |
| Login/identity | Form/session thật theo cấu hình hiện hành | Form/session thật, không SDK Zalo | Principal/role do server; không cấp quyền từ role preview |
| Vào F07 | Navigation tới `/mood` và `/mood-shared` | Navigation tới hai route tương ứng | Auth guard; không chỉ import page trong test |
| Ghi riêng tư | Chọn emotion và note tùy chọn, lưu hôm nay | Cùng khả năng, có note và thông báo thật | POST `/api/v1/mood/entries`, server VN date, note ≤2000 |
| Không có connection | Vẫn ghi/xem/sửa dữ liệu riêng | Vẫn ghi/xem/sửa dữ liệu riêng | Chỉ chia sẻ cần active connection |
| History/detail | Của mình, cursor bounded, chọn đúng mục | Cùng khả năng, desktop/mobile dùng được | GET entries; GET entries/{id}; auth trước phân trang |
| Edit | Sửa đúng mục, giữ nháp khi lỗi | Sửa được ngay từ history/entry point thực | PATCH entries/{id}; sửa tạo revision khác, không tự share |
| Summary | Mô tả cá nhân, không score/ranking | Cùng dữ liệu/semantics | GET entries/summary; bounded window |
| Preview/share | Một mục, một recipient hiện hành, đủ nội dung | Cùng khả năng | GET entry shares/connections; POST entry share với expected_revision |
| Quản lý grant | Trạng thái thật và revoke đúng quyền | Cùng khả năng | POST mood/shares/{id}/revoke; không báo thành công nếu lỗi |
| Phía nhận | List/detail còn quyền, pagination | Cùng khả năng | GET mood/shared và mood/shared/{id}; recheck revision/generation |
| Edit/revoke/unlink | Nội dung cũ không còn được đọc tiếp | Cùng hiệu lực, kể cả thao tác từ client kia | F15/F01 cùng một nguồn quyền; reconnect không hồi sinh grant |
| Logout/actor/lifecycle | Gỡ private DOM/sheet và bỏ late responses | Cùng yêu cầu | Session generation, page.destroy, thao tác logout thật |
| Mạng/timeout | Loading/empty/error/disabled/success đúng | Cùng yêu cầu | Unknown write outcome không tự retry hoặc fake-success |
| Khả năng tiếp cận | 320/390/430, chữ lớn, focus/keyboard | Mobile và desktop; chữ lớn, focus/keyboard | Không thu chữ/cắt nhãn, help còn mở |

Giữ emotion options theo contract/backend hiện hành, không lấy 5 pill hardcoded cũ trên home làm toàn bộ allowlist. Có thể thay quick card bằng entry point hoặc tích hợp lại nó đúng với trang F07; không giữ hướng dẫn “sẽ chỉnh sửa ở bản đầy đủ” khi chức năng đã được giao.

## Kiến trúc và phạm vi tệp

Các vị trí dự kiến: `web/src/pages/mood/`, `web/src/pages/mood-shared/`, router, profile/home entry points, style và web tests cần thiết. Tên route tương ứng có thể giữ `/mood` và `/mood-shared` như Mini App; nếu chọn route khác phải cập nhật mapping, navigation, tests và hướng dẫn có lý do rõ.

UI hai cây độc lập; chia sẻ client HTTP/session/endpoint contracts qua headless shared package. Không import page/component/CSS UI từ `zalo-mini-app/` vào `web/` hay chiều ngược lại. Không thêm zmp-sdk, React, framework/font mới để đạt parity. Dùng component/tokens sẵn có. Thay đổi shared phải giữ union contract/mock/consumer và import-boundary checks.

R01–R06 vẫn cần fix ở backend/Mini App/tests. R02 đặc biệt phải xét hai thiết bị/client cùng sửa một mục. Quyền sửa web trong phạm vi F07 đã được Huy giao; vẫn bảo toàn contributor changes và ownership của phần ngoài F07.

## E2E bắt buộc sau sửa — qua UI và cùng backend

| ID | Chuỗi thao tác | Kết quả cần thấy |
| --- | --- | --- |
| X01 | HS lưu emotion + note trên Mini App, HS đăng nhập web mở history | Cùng mục, nội dung và revision từ DB thật |
| X02 | HS lưu/sửa trên web, HS mở lại Mini App | Dữ liệu hiện hành; revision thay đổi đúng; không duplicate create khi cần edit |
| X03 | HS trên Mini App share một mục cho PH, PH trên web mở | Chỉ mục đã duyệt, đúng note/recipient/revision |
| X04 | HS trên web share, PH trên Mini App mở | Cùng semantics, không phụ thuộc client tạo grant |
| X05 | HS sửa ở client kia sau preview/after share, PH mở lại | Preview cũ bị stale; bản mới riêng tư tới khi duyệt share lại |
| X06 | Revoke ở web rồi PH mở Mini App; revoke ở Mini App rồi PH mở web | Lần đọc tiếp bị chặn cả hai chiều; quyền khác không đổi |
| X07 | Unlink/reconnect/F15 revoke ở một phía, phía kia mở lại | Không dùng grant generation/revision cũ, không hồi sinh quyền |
| X08 | Logout bằng nút UI, đổi actor, rời trang và response về muộn | Không còn note/preview/sheet của phiên cũ ở bất kỳ client |
| X09 | Stranger/admin thử ID của owner, hai owner share cho cùng recipient | Không bypass quyền; recipient list đủ mục hợp lệ từ từng owner |
| X10 | Hai edit đồng thời và edit/share trên MySQL | Revision không tái sử dụng cho nội dung khác; không đọc được note chưa duyệt |

Hai browser contexts/client có session riêng, không chép token vào URL/storage/log để tiện E2E. Không gọi adapter qua console thay cho UI trong bằng chứng nghiệm thu X01–X08; gọi trực tiếp chỉ dùng để chẩn đoán transport.

## Gate để Huy vào test

Chỉ ghi “sẵn sàng nghiệm thu local” khi R01–R07 được sửa và kiểm lại; các luồng UI cùng backend ở cả hai client hoạt động; có SHA mới đã push, dữ liệu synthetic, URL Huy thực sự truy cập được theo hạ tầng hiện có và checklist thao tác ngắn.

Huy thực hiện login → navigation → lưu note → xem lại → sửa → preview/share → PH đọc → revoke/đọc bị chặn → logout/đổi tài khoản trên web/Mini App và chéo client. Agent chuẩn bị services/API base/CORS/fixtures; không bắt Huy dùng DevTools hoặc chạy API/shell để sử dụng chức năng.

“Mini App trong browser” không thay Zalo Android/iOS. Thiếu device, native text scaling hoặc đường truy cập từ máy Huy thì ghi NOT_RUN/BLOCKED cụ thể, không suy từ build/ảnh. Không tự deploy/phát hành hoặc dùng participant data để mở đường nghiệm thu.
