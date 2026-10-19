# F04 — phạm vi nghiệm thu hiện hành

US-029 / US-033. Nhánh ứng dụng thực tế: `tinh-nang/f04-ai-ho-tro-dien-dat-us029-us033`.

| Nhóm | Điều kiện |
| --- | --- |
| AI chủ động | Disclosure provider là bên xử lý kỹ thuật; consent đúng policy, thiếu/revoke không gọi provider hoặc lưu kết quả trái quyền |
| Gemini | Backend-only, env/secret, bounds, timeout/quota/retry, output text không tin cậy, không key trong VITE/bundle/log/URL |
| Chất lượng | Giữ ý, dữ kiện, xưng hô; không tự bịa sự kiện/lời hứa/ý định, không chẩn đoán/điều trị; có corpus và review thật khi có provider |
| Review | Đọc, chỉnh, bỏ, retry trong giới hạn; stale result không đè mới; không tự gửi |
| Draft/preview/send | Final body + recipient + revision người viết nhìn và duyệt phải đúng snapshot server gửi; thay đổi khi bất kỳ request nào đang chờ phải invalidate/review lại |
| Hai client | Web/Mini App × hai vai, cùng backend/identity theo quyền; đồng thời sửa draft không âm thầm ghi đè hoặc dùng preview cũ |
| Privacy | Author-only AI; recipient/admin/staff không có đường đọc original/history; không lộ gián tiếp qua sai body |
| Xóa | Completed deletion chặn mọi kết quả từ request trước xóa; claim được tái tạo, cùng key, TTL retry và restore không hồi sinh dữ liệu cũ |
| Pause | Tự nguyện, server 300 giây; edit/AI không tự hủy/reset; hết giờ chỉ cho explicit preview/confirm |
| Fallback | AI error/off/timeout/429 vẫn giữ bản soạn và cho viết/lưu/preview/send/help bình thường |
| Thiết kế | Mapping đủ 4 khung web, 24 khung Mini App; web bổ sung state thiếu; logo thật; không overflow/hidden sai, có kiểm keyboard/focus/large text/safe area |
| Evidence | Gắn SHA/lệnh/expected/actual; tách SQLite/MySQL, fake/live Gemini, browser/device, local/Render; không gọi Done từ build/test cũ xanh |

Sau ec29ab: N01/N02 và năm ca gốc đã qua kiểm thử cơ bản; N03/N04/N05/N06 trong báo cáo hiện hành còn mở. Không dùng checklist lịch sử để yêu cầu làm lại phần đã sửa mà không đối chiếu SHA.
