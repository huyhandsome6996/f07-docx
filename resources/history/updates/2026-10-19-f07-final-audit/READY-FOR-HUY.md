# Gate để Huy review như người dùng bình thường

**Hiện tại: NOT_READY, SHA 2ffd674.** Web đã có UI F07 thật; cần sửa R08–R10 ở cả hai client, hoàn thiện bằng chứng còn thiếu và chuẩn bị đường truy cập đúng bản. Review này không merge hoặc deploy.

## Điều kiện bắt buộc

- Repro lưu liên tiếp (4 scenario), hết trang (2 scenario), lỗi stale ngay trong sheet (2 chiều) đều PASS sau sửa. Thêm tests nhiều trang, mục ngày cũ, lỗi mạng/unknown outcome, không kết nối, thao tác đồng thời; không dùng workaround remount editor.
- R01–R07 giữ xanh trên SHA mới, gồm MySQL edit/share race, hai owner cùng recipient, ngày full-string, lifecycle và chữ lớn của hai UI.
- Hoàn thiện mapping X01–X10, đánh dấu UI/backend/device riêng. X07 unlink/reconnect/F15 không hồi sinh grant, X08 logout thực sự có private detail + late response/đổi actor. NOT_RUN không phải PASS.
- Cung cấp SHA branch/PR đã push, bộ tài khoản synthetic HS/PH/người lạ, URL web/Mini API thật và checklist 10–15 phút. Trước khi ghi URL usable phải kiểm tra đường truy cập cho người nhận theo hạ tầng được cấp; không cần/deviceshell hay DevTools để dùng tính năng.
- Không có Zalo Android/iOS/native text scaling/keyboard thì ghi NOT_RUN. Có thể báo riêng “đạt kiểm tra local browser” sau khi sửa; chưa được gọi là toàn bộ Zalo/production đã đạt. Không tự deploy hoặc dùng người tham gia thật để mở đường thử.

## Checklist Huy khi gate đã qua

| Bước | Thao tác bằng UI | Kỳ vọng |
| --- | --- | --- |
| 1 | HS vào Cá nhân → Tâm trạng của mình trên cả hai client | Có UI thật, ngày/emotion/note theo backend |
| 2 | HS chưa kết nối ghi note, lưu rồi sửa/lưu tiếp 2 lần ngay editor | Cùng một mục, revision tăng, không lỗi trùng ngày |
| 3 | Mở lại history ở client kia, thử Tải thêm đến cuối | Đúng nội dung; không lặp mục, hết trang không còn nút nhận click |
| 4 | Với pair synthetic active: mở preview một mục, chọn PH, xác nhận | Xem đủ note/revision trước khi chia sẻ; không auto-share |
| 5 | PH ở client kia mở Được chia sẻ với bạn → Mở nội dung | Chỉ mục được cấp, đúng note và revision |
| 6 | HS mở preview; HS sửa ở client kia; HS xác nhận preview cũ | Lỗi stale đọc được ngay trong sheet, có cách xem bản mới; phải duyệt lại |
| 7 | HS sửa sau khi đã share, PH mở lại | Bản mới riêng tư đến khi share rõ ràng lại |
| 8 | Thu hồi ở web rồi PH mở Mini, làm chiều ngược lại | Lần đọc mới bị chặn, nội dung cũ không giữ lại trên màn |
| 9 | Unlink/reconnect/F15 revoke theo fixture riêng | Grant cũ không tự sống lại; test không phá pair dùng cho bước khác |
| 10 | PH đang xem note rồi logout bằng nút thật; login người lạ | Không còn note/overlay từ phiên trước; người lạ không thấy dữ liệu HS |

Reviewer mới chỉ chạy local Chromium + API và MySQL loopback. Các địa chỉ trong log/repro là kỹ thuật nội bộ, không phải link bàn giao cho Huy. Việc tài liệu được push main cũng không đưa code F07 lên website đang chạy.
