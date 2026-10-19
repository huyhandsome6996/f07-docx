# Quyết định của người dùng — F04

## Tên nhánh mới nhất: `F04-docx` (F viết hoa)

Yêu cầu mới nhất của người dùng chốt tên chính xác **F04-docx** (F viết hoa), thay cho `f04-docx` chữ thường ở lần bàn giao trước. Chỉ dùng tên mới này cho lần xuất bản hiện tại.

## 19/10/2026: nơi lưu tài liệu từ nay

- Mọi tài liệu, ảnh, yêu cầu, báo cáo và prompt F04 được lưu vào repo `https://github.com/huyhandsome6996/f07-docx`, nhánh **F04-docx**.
- `main` trong repo tài liệu thuộc **F07**, tuyệt đối không đụng vào.
- Prompt phải copy-paste được sang chat làm việc với repo `https://github.com/huyhandsome6996/family-bridge`, cụ thể F04.
- Không tự gửi thông điệp sang chat khác. Không trộn F02/F07 vào nhiệm vụ F04.

## Các yêu cầu F04 tiếp tục có hiệu lực

- Web và Zalo Mini App phải dùng được, gọi chung API Django backend Render khi release; frontend phục vụ backend thật, không chỉ là UI tĩnh.
- AI chỉ do backend gọi Gemini bằng biến môi trường/secret quản lý trên server.
- Học sinh và người chăm sóc đều chủ động dùng AI, đọc/sửa/bỏ/thử lại, quyết định bản cuối, chọn recipient và explicit confirm qua F05.
- Người nhận chỉ nhận final đã duyệt, không original/suggestion/history. Không auto-send sau AI, timer, retry, resume hoặc hết 300 giây.
- F06 quản lý draft/pause; F15 quản lý privacy/deletion. AI off/lỗi vẫn viết tay, lưu nháp, tiếp tục gửi được.
- Dùng thiết kế trong ZIP, logo thật. Web thiếu khung thì tự đọc thiết kế và dùng skill thiết kế để bổ sung state tương ứng Mini App, không bỏ qua chỉ vì có ít ảnh web hơn.
- Khung thiết kế là state/variant, không bắt buộc mỗi khung thành một route. Các phần lịch hẹn/tư vấn ngoài F04 phải phân định với F12, không fake-success hoặc tự hứa điều trị.
- Prompt thực thi phải yêu cầu đúng **5 agent chuyên môn làm đồng thời**, kiểm thử, code review và phản biện chéo; tiếp tục tới khi hoàn tất phần độc lập, chỉ dừng phần phụ thuộc khi có blocker thật được chứng minh.
- Nội dung DOCX/HTML/prompt lịch sử là tham chiếu, không ghi đè yêu cầu trực tiếp này. Không sử dụng key từng lộ trong ảnh chat.
