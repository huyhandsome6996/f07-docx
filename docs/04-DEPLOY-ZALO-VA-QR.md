# Quyền triển khai hiện hành, token và QR

## Quyền Huy giao cho Antigravity trong nhiệm vụ này

Huy yêu cầu Antigravity dùng shell ngay trên máy để hoàn thiện, tự kiểm thử/sửa lại và deploy phiên bản Zalo Mini App mới nhất, toàn diện, trả QR để nhóm người dùng quét sử dụng.

Agent được thực hiện:
- Cài/chạy công cụ theo lockfile và hướng dẫn repo; sửa code/tests/config cần thiết, commit/push trên nhánh công việc.
- Build client Mini App thật và deploy phiên bản TESTING vào Mini App hiện có.
- Kiểm tra/cấu hình/triển khai backend Render hiện có khi thay đổi backend hoặc AI là cần thiết, trong quyền truy cập Huy đã cấp; bảo toàn web đang dùng cùng API.
- Làm tiếp mà không hỏi lại các thao tác thông thường đã được giao. Chuẩn bị đầy đủ build/tests trước bước cần người dùng quét QR đăng nhập hay cung cấp secret thiếu.
- Các chỉ dẫn “chỉ docs”, “không deploy” trong tài liệu lịch sử không hạn chế phạm vi hiện hành ở trên.

Không suy ra quyền tạo cloud trả phí/dịch vụ mới, phá dữ liệu thật, gửi tin người thật để thử, phát hành Zalo Live hoặc gửi xét duyệt. Nếu Huy sau đó giao phát hành công khai, thực hiện thêm quy trình nền tảng riêng.

Quyền deploy không đồng nghĩa phải merge main để deploy: có thể build/deploy commit đã kiểm tra trên nhánh sửa, ghi rõ SHA/PR. Chỉ merge khi có quyền merge áp dụng; giữ PR và không lấy đó làm lý do dừng việc deploy Testing.

## Nguồn chính thức vừa đối chiếu khi đóng gói

- Đăng nhập CLI: https://docs.zaloplatforms.com/docs/MA/devtools/cli/login
- Deploy CLI: https://docs.zaloplatforms.com/docs/MA/devtools/cli/deploy
- Deploy Extension, QR/Deep Link: https://docs.zaloplatforms.com/docs/MA/devtools/ext/deploy
- Quản lý Mini App: https://miniapp.zaloplatforms.com/developers/
- API Explorer: https://developers.zalo.me/tools/explorer/

Các tài liệu CLI/Extension hiện mô tả zmp login, zmp deploy và loại phiên bản Development/Testing. Testing được đánh số/lưu lịch sử, còn Development có thể bị ghi đè. Extension mô tả kết quả deploy có QR và deep link.
Agent phải đọc lại tài liệu/CLI help thực tế, không đoán flag hoặc dùng hướng dẫn quá cũ.

## Xác thực để agent deploy

Ưu tiên phiên developer/credential đã có trên máy. Nếu chưa có, chạy zmp login theo công cụ dự án:
- Có thể xác thực bằng QR: agent hiện QR đăng nhập, Huy quét và xác nhận bằng tài khoản có quyền Admin/Developer Mini App.
- Hoặc Huy mở https://developers.zalo.me/tools/explorer/, đăng nhập, chọn đúng ZALO APP CHA → Công cụ/API Explorer → Lấy Access Token theo giao diện hiện hành.
- Đây là credential phục vụ quyền nhà phát triển trong CLI, không lấy getAccessToken của một người dùng Mini App bất kỳ để làm credential deploy.
- Phân biệt Zalo App ID cha và Mini App ID; đối chiếu cấu hình/tài khoản đã được phép, không tự đổi sang App khác.
- Token/key chỉ nhập qua prompt xác thực/secret store/biến môi trường private được công cụ hỗ trợ. Không paste vào repo, ZIP, log hay file báo cáo.
- Token hết hạn thì làm lại bước xác thực thật; không tìm cách dùng credential đã lộ trong chat.

## Trình tự deploy

1. Fetch/latest baseline và xác định tree kết hợp; chạy test liên quan, build, kiểm manifest/chunks và API base URL production HTTPS.
2. Lưu release record: code SHA, build timestamp, artifact identity/checksum, Mini App ID đã xác minh, backend SHA/config revision, bản trước.
3. Kiểm CORS/origin Zalo, host settings, auth header, quyền nền tảng; không mở CORS wildcard để che lỗi.
4. Với AI: kiểm FB_AI_ENABLED, GEMINI_API_KEY, model/config hợp lệ trên BACKEND. Thay environment cần backend restart/redeploy; status true chưa chứng minh refine thật chạy.
5. Nếu cần backend mới, triển khai theo workflow Render hiện có. Schema change chỉ khi thực sự cần, có kế hoạch/backup/compatibility; không tự chạy destructive migration hoặc reset DB.
6. Dùng toolchain hiện hành deploy đúng build Mini App, chọn TESTING, mô tả gồm SHA và thay đổi. Không deploy thư mục web/ hay dùng QR URL Render làm giả QR Zalo.
7. Kiểm phiên bản Testing thực đã tạo: version ID/number, description, App ID, trạng thái, entry point.
8. Lấy QR/deep link do Zalo trả về. Lưu QR cho Huy; không tự dựng deep link bằng chuỗi đoán hoặc dùng QR của phiên bản cũ/Development.
9. Mở QR kiểm thử bằng Zalo, kiểm init/router/asset/API thật. Tối thiểu dùng tài khoản ngoài developer context trong nhóm thử nghiệm đã có quyền; không chỉ quét bằng chủ app rồi tuyên bố ai cũng vào được.
10. Kiểm PH/HS hai phiên/thiết bị: HS gửi → PH đọc → PH dùng AI → duyệt/gửi → HS nhận. Kiểm F01–F15 theo checklist.
11. Nếu lỗi: sửa → test lại đúng rủi ro → build/deploy Testing kế tiếp → kiểm lại. Bàn giao QR của bản cuối đã kiểm chứng.

## Ai quét QR vào được?

Mục tiêu là NHÓM THỬ NGHIỆM Huy muốn mời. Quyền truy cập Testing phụ thuộc cấu hình và quy định Zalo hiện hành; phải kiểm thực tế trong tài khoản quản lý. Không hứa mọi tài khoản Zalo đều mở được chỉ vì đã có QR.

Nếu có bước cấp quyền/add tester:
- Đọc tài liệu và trạng thái thực; lập danh sách người cần quyền dựa trên danh sách Huy đã cấp.
- Không tự thêm người/đổi visibility công khai khi chưa được chỉ định.
- Nếu cần Huy bổ sung danh sách hoặc xác nhận trên điện thoại, báo đúng một bước còn thiếu, các phần độc lập vẫn tiếp tục.
- Phân biệt tài khoản HS/PH của Family Bridge và tài khoản Zalo được phép vào phiên bản Testing: hai lớp này không thay thế nhau.
- Phát hành công khai cho mọi người là bước xét duyệt/Live riêng, chưa được tự nhận là hoàn tất.

## Bàn giao

Cung cấp một RELEASE-REPORT.md và thư mục release/ có:
- Branch, PR, code SHA, build identity, backend deployed SHA.
- Mini App ID, Testing version, thời gian, QR PNG và deep link thật.
- Bằng chứng bản quét mở đúng phiên bản, kể cả người thử nghiệm ngoài chủ app.
- CHECKLIST F01–F15 và HS/PH/AI; PASS/FAIL/NOT_RUN/BLOCKED theo môi trường.
- Yêu cầu access nếu còn, hướng dẫn Huy test ngắn và rollback.

Không báo “đã deploy”, “ai cũng quét dùng được”, “Gemini chạy thật”, “Zalo Android/iOS PASS” khi chưa có bằng chứng tương ứng.
