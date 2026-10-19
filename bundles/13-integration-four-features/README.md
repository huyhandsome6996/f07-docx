# ZIP13 Bộ tích hợp bốn tính năng

[Đọc hướng dẫn mới](../../hoan-thien-f02-f04-f07-f15/00-READ-FIRST.md).

[ZIP hướng dẫn](13-F02-F04-F07-F15-integration-kit.zip) chứa tài liệu điều phối, prompt, DOCX, provenance và inventories. Source snapshots và archive-docs dung lượng lớn nằm nguyên byte trong thư mục kit trên nhánh; ZIP13 không lặp lại các file đó. Clone toàn nhánh để có đủ tài nguyên. ZIP00–12 gốc F07 giữ nguyên ở bundles; clone toàn nhánh để có cả lịch sử.

Kiểm tra `python3 tools/bundles.py verify`; giải nén `python3 tools/bundles.py extract 13 --dest /tmp/family-bridge-integration-reading` vào thư mục đọc riêng. Không chép snapshot lên ứng dụng hoặc tự chạy script trong archive.
