# Điều kiện để Huy kiểm thử như người dùng bình thường

**Hiện tại chưa đạt:** lượt recheck tại bb75b2c vẫn tái hiện đủ R01–R06. Tài liệu này là đầu ra coding agent phải chuẩn bị sau khi sửa và kiểm lại, không phải thông báo ứng dụng đã sẵn sàng.

## Gate kỹ thuật trước bàn giao

- Đóng R01–R06 bằng source fix và regression tests; MySQL concurrency và kiểm tra lifecycle/browser phải thực sự chạy. Không giảm assertion, dùng xfail/skip hoặc đổi mức zoom để che lỗi.
- Ghi SHA mới đã push đúng nhánh F07, PR #42 và kết quả các suite cần thiết. Tests hiện có xanh không thay thế các regression đỏ.
- Duy trì private default, đúng item/recipient/revision/generation, active admin_provisioned invite NULL, F15 revoke và không tự chia sẻ sau sửa/kết nối lại.
- Phân biệt Browser/SQLite, MySQL và Zalo Android/iOS. Thiếu device thì ghi NOT_RUN cụ thể; không tuyên bố đã nghiệm thu thiết bị.

## Bộ bàn giao để Huy tự bấm trên giao diện

Agent khởi động và kiểm tra sẵn dịch vụ, API base/CORS và dữ liệu synthetic trước khi gửi hướng dẫn:

1. Cung cấp URL thực sự truy cập được trong môi trường sử dụng của Huy và chỉ rõ bản build/SHA. Nếu chỉ có loopback của máy agent, không coi đó là URL Huy truy cập được từ máy khác. Dùng khả năng truy cập đã có; việc deploy/phát hành/tạo tài nguyên trả phí cần phạm vi riêng.
2. Cung cấp tài khoản synthetic HS, PH đã có canonical active connection và một tài khoản synthetic không liên quan; ghi rõ là dữ liệu kiểm thử. Không dùng hoặc sửa tài khoản người tham gia thật. Không đưa credential thật vào kho tài liệu.
3. Huy đăng nhập bằng form, mở F07 từ điều hướng thật, chọn cảm xúc và lưu một ghi chú tiếng Việt/emoji. Giao diện báo lưu thành công và riêng tư sau phản hồi máy chủ.
4. Mở lại hoặc đăng nhập lại vẫn có lịch sử. PH chưa được chia sẻ thì không thấy nội dung của HS.
5. HS chọn một mục, chọn đúng PH, đọc preview rồi xác nhận. PH qua giao diện của mình thấy đúng mục và nội dung được duyệt.
6. HS sửa mục; PH mở lại thì bản mới chưa được đọc cho tới khi HS xem trước và chia sẻ lại. Không tự chia sẻ lại do refresh, timer hoặc reconnect.
7. HS thu hồi một quyền; PH mở lại bị chặn, các quyền không liên quan không bị thu hồi theo. Luồng F15 phản ánh cùng nguồn grant.
8. Rời trang, logout bằng nút thật và đổi actor: không còn sheet/private preview của phiên cũ; không cần Huy dùng DevTools để dọn dữ liệu.
9. Giao diện đọc/bấm được ở màn nhỏ và chữ lớn, tên/label không bị cắt. Có đường trợ giúp và cách phục hồi lỗi mạng rõ ràng.
10. Bàn giao checklist ngắn “bấm ở đâu → nhập gì → thấy gì”, ảnh từ bản đã sửa, hạn chế còn lại và cách báo lỗi. Các bước backend, shell, tạo fixture và sửa cấu hình do agent chuẩn bị, không đưa vào chuỗi thao tác của người dùng thông thường.

Nếu hạ tầng chưa cho Huy truy cập URL thật, hoàn tất sửa và kiểm thử độc lập trước, rồi báo chính xác blocker truy cập. Không công bố đã sẵn sàng cho Huy chỉ từ ảnh hoặc mock.
