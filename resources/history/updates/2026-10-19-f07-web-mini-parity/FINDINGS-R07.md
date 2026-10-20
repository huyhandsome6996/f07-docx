# R07 — Web chưa có UI F07 đầy đủ dù API/shared adapter đã có

Mức ưu tiên: cần hoàn tất trước nghiệm thu người dùng. Source kiểm: bb75b2c.

## Đã quan sát bằng browser và API thật

| Phép kiểm | Mini App | Web |
| --- | --- | --- |
| Form class-session login | HTTP 200 | HTTP 200 |
| Shared adapter có 8 method F07 bổ sung | Có | Có |
| Adapter list/detail mục synthetic từ backend | HTTP 200 | HTTP 200 |
| Mở `#/mood` sau login | Có trang mood | `data-page=not-found` |
| Mở `#/mood-shared` sau login | Có trang nhận | `data-page=not-found` |
| Profile có lối vào hai màn F07 | Có | Không |
| Home quick mood gọi API | Không phải phép so sánh trong case này | Có POST; duplicate trả HTTP 400 nghiệp vụ |
| Chỉnh sửa sau duplicate trên web | — | Thông báo “Màn nhật ký sẽ cho phép chỉnh sửa ở bản đầy đủ.” |

Kết quả trong `evidence/client-parity.log`, request metadata ở `evidence/client-parity/results.json`. Không ghi token hoặc response body. Ảnh `web-mood.png`, `web-mood-shared.png`, `web-profile.png`, `web-home-duplicate-no-edit.png` thuộc thư mục evidence/client-parity.

## Nguồn liên quan

- `web/src/app/router.js` không đăng ký `/mood` hoặc `/mood-shared`.
- `web/src/pages/profile/index.js` không có entry F07.
- `web/src/pages/home/index.js` có quick create và list hôm nay, nhưng duplicate vẫn dẫn lời hứa chỉnh sửa trong tương lai. Khi không có connection, home sớm render trạng thái chưa kết nối; chức năng private không được buộc phải có connection khi xây F07 web.
- `web/src/pages/diary/index.js` là stub “Nhật ký sẽ mở ở bản đầy đủ”, không phải giao diện F07; không gọi nó là F07 đã hoàn thành hoặc thay F08 bằng F07.
- `web/src/adapter/web-adapter.js` và Mini App đều dùng `packages/family_bridge_shared/src/adapter/http-endpoints.js`. Shared method tồn tại không tự tạo route/UI.

Source-reference giữ 11 tệp có chọn lọc để đối chiếu, kèm hash trong PROVENANCE.json. Đọc checkout mới nhất trước khi sửa.

## Yêu cầu đóng finding

Triển khai đầy đủ UI web cho tạo note/cảm xúc, history/pagination/detail/edit/summary, chọn recipient/preview/share, list/revoke grants và phía nhận list/detail. Dùng API thật và cùng semantics với Mini App; có navigation thật, không chỉ URL gõ tay hoặc gọi method từ console. Xem ma trận trong REQUIREMENTS-AND-ACCEPTANCE.md.

Các phép gọi adapter trực tiếp trong smoke chỉ chứng minh phần HTTP đã có. Chưa chạy được E2E UI web → Mini App hoặc ngược lại vì web thiếu màn hình; ghi **BLOCKED_R07**, không PASS. Sau sửa cần thêm tests của web và E2E qua UI hai chiều.
