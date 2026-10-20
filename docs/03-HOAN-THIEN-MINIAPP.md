# Hoàn thiện Zalo Mini App — đầu ra bắt buộc

## Phạm vi hiện hành

Nguồn yêu cầu là Huy trong cuộc trao đổi ngày 21/10/2026. Đây là nhiệm vụ TRIỂN KHAI, KIỂM THỬ, SỬA VÀ DEPLOY; không dừng ở kế hoạch hay mockup.

Repo ứng dụng: https://github.com/huyhandsome6996/family-bridge
Main tại lúc đóng gói: 7ace3dab80c2473095cdef51c0cd3b35805b4143.
Agent phải fetch lại main, remote branches và PR đang làm để tránh bỏ sót cập nhật/công việc song song. Nhánh tồn tại không chứng minh đã merge; chỉ lấy nội dung đã được giao/duyệt để tích hợp, không tự gom mọi nhánh.

Đích là client trong zalo-mini-app/ chạy BÊN TRONG ZALO. web/ là client độc lập. Hai client dùng chung backend API trên Render và shared headless contracts. Không lấy website responsive hoặc web deploy thành bằng chứng Mini App đã hoàn thành.

Đọc AGENTS/skills/rules hiện hành tại checkout ứng dụng. Stack mới là HTML5/CSS3/JS ES Modules + Vite + zmp-sdk. Không tự chuyển React/zmp-ui theo snapshot lịch sử.

## Yêu cầu đã chốt cần giữ

- HS/PH được cấp tài khoản và liên kết sẵn. Không bắt dùng mã mời hoặc tự đồng ý điều khoản/AI/nghiên cứu hộ người dùng.
- Người nhận mới phản hồi thư đang mở; phân quyền theo actor/sender/recipient thật. PH và HS đều có thể là người nhận.
- AI hỗ trợ sửa ý tác giả đang soạn, không tự nhập vai người kia. Dùng gợi ý chỉ điền ô soạn; tác giả duyệt/gửi.
- Riêng tư mặc định; chia sẻ từng item/recipient/revision/current connection generation.
- Pause 300s tự chọn không tự gửi khi hết giờ. Help/tín hiệu lắng nghe không bị pause trì hoãn.
- Admin có named capability/scope/TTL, không bypass thư/nhật ký riêng bằng is_staff/superuser.
- Không nhúng iframe website Render để thay client Zalo; không bê desktop shell vào điện thoại.
- Không fake dữ liệu tham gia, tin nhắn, phản hồi hoặc AI thành dữ liệu thật. Chỉ seed nội dung hoạt động phù hợp và dữ liệu synthetic cô lập cho test.
- Main tại mốc đóng gói đã có F08 diary đầy đủ; không lấy finding cũ để khôi phục placeholder.

## Đối chiếu toàn bộ F01–F15

Lập route-feature-API matrix từ code mới nhất: web route, Mini route/màn, API, actor, loading/empty/error, tests và link/đường vào.
Đạt tương đương hoặc tốt hơn về mọi luồng HS/PH có trên web; không đếm route để làm đẹp báo cáo. Một màn Mini có thể gộp nhiều route web nếu mọi hành vi vẫn đủ. Trang quản trị web không ép đưa vào Mini nếu ngoài audience/quyền.

| Feature | Đầu ra người dùng phải dùng được |
| --- | --- |
| F01 | Đăng nhập HS/PH, consent, phiên/logout, thấy đúng người ghép; giữ Zalo login theo cấu hình hiện hành |
| F02 | Bốn tuần, hoạt động riêng/chung, chọn tham gia/tiến độ, thỏa ước hai phía; không khóa tuần sau |
| F03 | Chọn thẻ, recipient thật, preview, xác nhận gửi, nhận/đọc/phản hồi đúng chiều |
| F04 | Viết/gợi ý/consent/refine/apply/discard; AI thật, giữ ý, không auto-send |
| F05 | Hộp thư nhận/gửi, chi tiết, phản hồi, trạng thái gửi/lookup đúng contract |
| F06 | Lưu/mở/sửa nháp, pause/resume, hết giờ vẫn chờ xác nhận |
| F07 | Ghi tâm trạng, lịch sử, sửa, chia sẻ/thu hồi, xem item được chia sẻ |
| F08 | Viết/xem/sửa nhật ký, song hành, share từng trang và nhận/phản hồi hợp lệ |
| F09 | Hoạt động/bài học có danh sách + chi tiết + thực hiện/tiến độ phù hợp, không chỉ tiêu đề |
| F10 | HS chủ động phát tín hiệu; PH nhận/ack/viết phản hồi; ack không giả làm câu trả lời |
| F11 | Điểm tựa đã đồng ý, quản lý vai trò, gửi/đọc tin đúng quyền và hết hạn |
| F12 | Danh bạ trường, liên hệ, đặt/xem/hủy hẹn, tiếp nhận đúng school/assigned scope |
| F13 | Danh bạ trợ giúp thật từ backend, số/giờ hoạt động đã duyệt, mở gọi chủ động |
| F14 | Khảo sát tự nguyện, nhập/xác nhận/kết quả hoàn tất, own/aggregate đúng quyền |
| F15 | Quản lý chia sẻ từng mục, thu hồi/unlink, consent và yêu cầu xóa, state/cache đúng |

Chức năng backend đã có thì nối UI/API thật. Nếu backend còn thiếu, triển khai phần cần thiết theo repo contract, không dựng nút giả rồi báo xong.

## Mọi màn có đầy đủ trạng thái

Loading nhẹ; empty có giải thích; error/retry có chủ đích; offline không mất nháp; hết phiên; revoked/stale; success chỉ sau xác nhận server.
Không HTTP failure → success giả, không ẩn phần lỗi rồi coi đã hoàn tất.

## Nguồn thiết kế

Đọc docs/06-THIET-KE-MINIAPP.md và resources/README.md.
Resources chứa tài liệu/ảnh/logo/font/HTML Stitch/snapshot gốc trong repo tài liệu; là THAM KHẢO lịch sử, không chép đè ứng dụng.
Ưu tiên các frame có tên zalo_/mini và thiết kế mobile. Web frames chỉ đối chiếu nội dung/chức năng.
Chỉnh theo host Zalo/action bar/menu/insets thật. Không cần chờ Stitch tạo thêm nếu tài nguyên hiện có đủ triển khai.
