# Quyết định phạm vi mới — 19/10/2026, UTC+7

Nguồn: yêu cầu trực tiếp của Huy trong chat này: “bên zalo mini app có giao diện làm việc với backend api thì bên web cũng phải có”. Huy yêu cầu kiểm thử F07 và điều chỉnh kho tài liệu để coding agent tiếp tục xây ứng dụng.

## Phạm vi áp dụng

F07 phải có đầy đủ luồng người dùng trên cả `zalo-mini-app/` và `web/`, cùng gọi backend API thật. Đồng bộ khả năng và quyền dữ liệu; không yêu cầu hai giao diện giống từng pixel. Web cần responsive cho desktop/mobile, Mini App theo môi trường của nó.

Quy tắc UI/API tương ứng là định hướng chung cho hai client; vòng công việc này triển khai/nghiệm thu F07. Không dùng nó làm lý do viết lại các feature khác không được giao.

## Dated supersede của hướng dẫn cũ

Mệnh đề “KHÔNG sửa web”, “web do contributor khác nên F07 chỉ làm Mini App” trong nhiệm vụ/handover lịch sử **không còn là điều kiện loại web ra khỏi F07**. Huy đã yêu cầu rõ làm UI web tương ứng.

Coding agent được triển khai F07 web, gồm page/route/navigation/style/test/handover và những thay đổi shared contract cần thiết cho F07. Vẫn phải đọc chỉ dẫn tại checkout hiện hành, kiểm tra dirty work/ownership/PR đang mở, giữ thay đổi của contributor khác và phối hợp shared files. Đây không phải quyền ghi đè toàn bộ web hoặc chuyển stack.

Agent cần ghi dated note tương ứng trong tài liệu/AGENTS của nhánh ứng dụng nếu còn hướng dẫn mâu thuẫn gây chặn triển khai. Không tự tạo decision ID hay tuyên bố phê duyệt nghiệp vụ vượt nội dung yêu cầu này.

## Các ranh giới giữ nguyên

- Web và Mini App có UI tree/entry/router/build riêng. Không import UI mini vào web hoặc ngược lại. Shared package giữ headless/pure ESM; web không import zmp-sdk.
- Backend là nguồn xác thực/owner/grant/revision/generation; không dùng role preview để cấp quyền.
- Giữ private default, chọn đúng mục/người nhận/preview/xác nhận, không auto-share sau sửa hoặc reconnect, revoke/unlink có hiệu lực ở lần đọc tiếp theo.
- F02 và các feature web khác vẫn được bảo vệ khỏi chỉnh sửa không liên quan.
- Làm trên nhánh F07, cập nhật PR #42. Không merge/push main ứng dụng, force-push, deploy, chạy migration production hoặc dùng dữ liệu thật khi chưa có phạm vi riêng.

Đây là ghi nhận yêu cầu người dùng hiện hành, không phải bằng chứng chức năng đã triển khai hoặc nghiệm thu.
