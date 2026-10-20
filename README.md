# Family Bridge — Gói Antigravity hoàn thiện Mini App, phản hồi, AI và deploy QR

## Bắt đầu tại đây

Gói ngày 21/10/2026. Đích là Mini App chạy trong Zalo; web riêng dùng chung backend.
Đọc PROMPT-DAN-VAO-ANTIGRAVITY.md rồi docs/01 → 06. Đây là nhiệm vụ hoàn thiện code, kiểm thử và deploy Testing theo yêu cầu Huy, không phải chỉ docs.

| File | Mục đích |
| --- | --- |
| docs/01-SUA-LUONG-PHAN-HOI-HS-PH.md | Bản kiểm tra luồng thư và R01–R05, T01–T22 |
| docs/02-KHOI-PHUC-AI-PHAN-HOI.md | Khôi phục AI, Render diagnosis, AI01–AI10 |
| docs/03-HOAN-THIEN-MINIAPP.md | Toàn bộ yêu cầu Mini F01–F15, parity chức năng với web |
| docs/04-DEPLOY-ZALO-VA-QR.md | Quyền deploy, token/QR, Testing audience, release/rollback |
| docs/05-KIEM-THU-VA-SUA-DEN-KHI-DAT.md | Chu trình kiểm thử/sửa, các gate không được giả PASS |
| docs/06-THIET-KE-MINIAPP.md | Đặc tả 40 màn/trạng thái đích cho điện thoại Zalo |
| resources/README.md | Cách tìm thiết kế/asset/nguồn lịch sử, giới hạn gói cũ |
| resources/history/ | Nguyên cây repo tài liệu tổng hợp tại commit nguồn; ảnh/logo/font/Stitch/DOCX/ZIP/rules/source tham khảo |
| provenance.json | SHA nguồn và phạm vi kiểm chứng |

## Nguồn và sự ưu tiên

- 01 và 02 được tách từ một file báo cáo đã cập nhật AI, không phải hai audit độc lập.
- Mốc ứng dụng đã review: 7ace3dab80c2473095cdef51c0cd3b35805b4143; agent phải fetch mới và nghiệm thu head thực sẽ deploy.
- Tài liệu 01/02 giữ nguyên giới hạn: reviewer chỉ đọc GitHub/probe JavaScript với doubles; chưa chạy Django/Node suite toàn dự án/Gemini thật/Zalo thiết bị.
- Quyền triển khai và yêu cầu tiếp tục sửa trong 03–05 là quyết định mới của Huy, thay hạn chế no-deploy/docs-only ở đúng phạm vi này trong báo cáo/snapshot cũ.
- resources/history/ chứa nguyên tree tài liệu nguồn, vì vậy tên nhánh/README/AGENTS/PROMPT/nhận định xung đột ở trong đó là LỊCH SỬ. Root gói mới là entry point; code thật tuân AGENTS ở checkout family-bridge.
- Không dùng snapshot thiếu tính năng cũ để ghi đè main, đặc biệt nhật ký F08 đã nâng cấp.

## Dùng ZIP

Giải nén một lần; folder root chứa prompt và docs. Không phải tải từng file .md riêng.
Nếu muốn đọc trên GitHub, mở đúng nhánh/commit gói. Có thể clone kho tài liệu, nhưng không dùng nó làm checkout ứng dụng.

QR chỉ có SAU KHI Antigravity deploy và xác minh trên Zalo. ZIP này không giả kèm QR ứng dụng đã chạy.
