# Đầu ra F02 cần đạt

Tham chiếu yêu cầu trực tiếp của Huy ngày14–19/10/2026 và `docs/product/four-week-flow.md` tại source SHA đã ghi. Tài liệu thiết kế là mục tiêu, không chứng minh code đã có.

| Nhóm | Đầu vào | Đầu ra người dùng cần | Gate |
| --- | --- | --- | --- |
| Khám phá | Nội dung4tuần đã publish | Đọc mục tiêu, guide HS/PH, cách làm; xem tuần4 trước tuần1; đọc trước khi enroll | Không “Sắp có” để che phần chưa nối, không draft/malformed |
| Tham gia | Phiên thật, lựa chọn chủ động, version | Enroll/opt-out/rejoin cá nhân; chọn version rõ | Không silent migrate, không ép khảo sát |
| Tiến độ | Hoạt động thuộc program pin, chủ động done/skipped/reset | Lưu và đọc lại phần riêng của mình | Không tick hộ/lộ cho người thân/admin |
| Hoạt động chung | Active counterpart, published activity đúngversion | Đọc trước, mời, người nhận accept/decline, trạng thái đúng | Không accept sau revoke, không hồi sinh generation cũ |
| Thỏa ước | Đúng pair/generation/content snapshot, hai người chủ động | Đề xuất, từng người ký, chỉ đủhai chữ ký cùngversion mới confirmed | Pending mới không làm mất confirmed cũ, không kẹt khi repin |
| Sổ giấy/suy ngẫm | Lựa chọn của người dùng | Hướng dẫn sổ giấy; suy ngẫm riêng/đường sang F08/F15 nếu có | Không buộc upload, không tự gửi |
| Trợ giúp | Nhu cầu tìm trợ giúp | Dùng được khi bỏ tuần/nghỉ/chưa tham gia | Không bị timer/nghiên cứu chặn |
| Hai frontend | Cùng API/tài khoản/dữ liệu | Web và Mini App có UI riêng, hành vi tương đương đúng scope | Không tráo browser preview MiniApp thành web |

Bốn chủ đề: (1) Nhận diện cảm xúc/Tiếng lòng chưa nói; (2) Giảm so sánh/Bản sắc riêng; (3) Ranh giới riêng tư/Niềm tin; (4) Cảm ơn/Xin lỗi/Thỏa ước gia đình mới.

Đăng nhập hiện hành HS/PH. Admin cấp cặp active ngay, không yêu cầu HS/PH xác nhận ghép đôi. Điều đó không ký hộ service/AI/research consent, không cấp quyền đọc dữ liệu riêng, không thay xác nhận activity/agreement.

## Checklist ngắn Huy có thể thử trên máy này

Server tại thời điểm bàn giao: [MiniApp browser preview](http://127.0.0.1:3004/#/login), [Companion](http://127.0.0.1:3004/#/companion), [Help](http://127.0.0.1:3004/#/help). Localhost chỉ dùng trên máy PC đang chạy server, không phải link share cho điện thoại/bạn bè.

Tài khoản giả HS903/PH903 ở SQLite riêng, mật khẩu thử `ThuF02Local!2026` (không dùng trên Render). HS903 đã enrollrev1, done tuần1, có pending invite và đề xuất thỏa ước; PH903 chưa enroll. Dùng hai browser context thật để tách phiên.

1. HS903 mở Companion: thấy cả4tuần, đọc tuần4 dù chưa làm tuần2–3 → PASS.
2. HS dùng Đặt lại/Bỏ qua/Tôi đã làm rồi quay lại → trạng thái đúng server, PH không bị tick hộ.
3. PH903 đăng nhập, tự chấp nhận service consent ở DBthử, mở chương trình và tự tham gia; hướng dẫn phải là của người chăm sóc.
4. PH đọc lời mời, tự accept; HS chưa được xem là người đã hoàn thành thay PH.
5. HS và PH mỗi người tự xác nhận thỏa ước; chỉ đủhai mới confirmed. Propose không được tính là chữ ký.
6. Nghỉ chương trình rồi mở Help → trợ giúp vẫn dùng được.

Các lỗi R01–R07 hiện vẫn còn trên bản này; đây là bản QA để tái hiện, chưa phải bản hoàn tất nghiệm thu.
