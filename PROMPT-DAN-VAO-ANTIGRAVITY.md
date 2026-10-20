Hãy trực tiếp hoàn thiện, tự kiểm thử/sửa lỗi và deploy Zalo Mini App Family Bridge theo gói này.

Repo ứng dụng:
https://github.com/huyhandsome6996/family-bridge

1. Giải nén ZIP, đọc README.md và AGENTS.md ở ROOT GÓI MỚI, rồi đọc docs/01 → 06. Hai file đầu là báo cáo sửa luồng HS/PH và khôi phục AI. resources/history/ là dữ liệu lịch sử, không nhận instruction cũ thành lệnh hiện hành.

2. Fetch main/nhánh/PR mới nhất, kiểm công việc song song, dùng worktree/nhánh phù hợp. Đọc AGENTS/skills/rules hiện hành tại checkout ứng dụng. Không reset/clean công việc người khác, không force push, không chép snapshot đè source mới.

3. Đích chính là ZALO MINI APP trong zalo-mini-app/, giao diện điện thoại BÊN TRONG ZALO. web/ là client riêng dùng chung API Render. Không làm website responsive hoặc nhúng iframe rồi gọi là đã hoàn thiện Mini App. Giữ stack ESM/Vite/zmp-sdk hiện hành.

4. Hoàn thiện mọi luồng HS/PH F01–F15, tương đương hoặc đầy đủ hơn web theo chức năng; bổ sung route/menu/UI/API còn thiếu. Không đếm route hình thức hoặc đưa trang admin vào sai audience. Bảo toàn các tính năng mới đã hoạt động và luồng HS/PH cấp tài khoản/liên kết sẵn.

5. Sửa R01–R05 trong báo cáo: thư sent không có composer tự phản hồi; người nhận thật mới phản hồi, cả HS và PH đều có thể là recipient. Backend kiểm đúng cặp sender/recipient/reply_to. Sửa lookup state/status, phân loại lỗi và giữ operation key khi gửi chưa rõ kết quả. Rà F10 ack đúng chiều.

6. Khôi phục AI THẬT trên backend: chẩn đoán status → consent → refine → apply/accept → gửi F05. Giữ AI để PH viết lời đáp êm ái hơn, và cho HS khi HS trả lời thư nhận. AI không tự nhập vai bên kia, không auto-send. Không bỏ nút AI hoặc chỉ đưa đường viết tay rồi báo xong. Kiểm flag/key/model/quota/timeout/wiring trên đúng backend Render theo quyền hiện có, không lộ key.

7. Tôi cho phép bạn dùng shell trên máy để build/test, sửa code và triển khai bản TESTING mới vào Mini App hiện có; triển khai backend Render hiện có khi cần để phiên bản dùng được, trong quyền truy cập đã cấp. Hoàn thành phần code/test/build trước khi yêu cầu thao tác xác thực còn thiếu. Không hỏi lại quyền cho các bước thông thường này. Không tự tạo cloud trả phí hoặc phát hành Zalo Live/gửi xét duyệt.

8. Tự kiểm thử và sửa đi sửa lại cho đến khi đạt các tiêu chí. Mỗi lỗi: tái hiện → regression test → sửa → test/build → deploy → kiểm bản thật → sửa tiếp. Không dừng ở kế hoạch, mockup hay suite xanh. Không giả PASS nếu thiếu Gemini thật/MySQL/thiết bị/quyền; chỉ dừng phần phụ thuộc khi có blocker thực sự và báo chính xác bước Huy cần làm, tiếp tục mọi phần độc lập.

9. Dùng đăng nhập developer đã có hoặc zmp login theo tài liệu/CLI help hiện hành. Huy có thể quét QR đăng nhập hoặc cấp token private từ https://developers.zalo.me/tools/explorer/ với đúng Zalo App CHA. Không nhầm với Mini App ID/token người dùng, không dùng secret từng lộ trong chat, không commit token.

10. Deploy đúng artifact Mini App đã test, loại Testing, mô tả kèm code SHA. Lấy version/QR/deep link do Zalo trả về, kiểm bằng tài khoản tester ngoài chủ app và cặp HS/PH hai phiên. Kiểm quyền Testing của nhóm; không hứa mọi tài khoản quét được chỉ vì đã có QR. Phát hành công khai có quy trình riêng.

11. Commit/push nhánh sửa và bàn giao PR; merge chỉ khi có quyền áp dụng. Không lấy chuyện chưa merge làm lý do không deploy Testing: có thể deploy commit đã kiểm tra trên nhánh sửa và ghi rõ SHA.

12. Chỉ báo hoàn tất khi bản Testing mới mở và luồng HS gửi → PH nhận → PH dùng AI/duyệt/gửi → HS nhận thực sự hoạt động trong môi trường kiểm chứng, cùng checklist F01–F15 đã giao. Bàn giao RELEASE-REPORT.md, branch/PR/SHA, backend deployed SHA, Testing version, QR PNG/deep link thật, bằng chứng test, phần NOT_RUN/BLOCKED và rollback. Hướng dẫn tôi quét QR dùng thật ngắn gọn.

Hãy bắt đầu làm ngay.
