# Kiểm tra bản cập nhật kho tài liệu

- `python3 tools/bundles.py verify`: xác minh đủ ZIP gốc, 9 partition lịch sử và gói review 10. Gốc vẫn có 946 tệp, 945 checksum manifest ban đầu khớp; 01–09 không đổi.
- `sha256sum -c catalog/SHA256SUMS`: toàn bộ ZIP đạt.
- Đã giải nén 00, 01 và 10 vào cùng thư mục tạm. Dữ liệu gốc và review cùng tồn tại; từng tệp plain trong `updates/2026-10-18-f07-review/` khớp byte với tệp trích xuất từ ZIP 10.
- Manifest mới được kiểm tra từng số byte và SHA-256, không tự liệt kê chính manifest.
- Khi sửa một `FINDINGS.md` tại thư mục giải nén rồi extract 10 lần nữa, công cụ từ chối ghi đè và giữ nguyên chỉnh sửa.
- Liên kết Markdown mới tại kho tài liệu được kiểm tra đích tồn tại; không áp phép kiểm này cho liên kết lịch sử trong partial branch-snapshot.
- Quét mẫu token GitHub/AWS access key/private-key block trong plain files và ZIP members: không có kết quả khớp. Không coi đây là chứng nhận mọi loại dữ liệu nhạy cảm đều được phát hiện. Mật khẩu fixture synthetic vốn có trong source tham chiếu không phải credential production.
- Đã chạy chính `repro/run_review.py` đã đóng gói trên SQLite và MySQL: exit 1 như kỳ vọng trên baseline còn lỗi, không biến test đỏ thành PASS.
- Công cụ đóng gói chỉ đọc cây review local và dựng ZIP/catalog; công cụ đọc ZIP không thực thi tài liệu, script hoặc branch snapshot.

Sau khi sửa tài liệu review, dựng lại bằng `python3 tools/package_review.py`, rồi chạy verify/checksum và kiểm tra diff. Không dùng công cụ này để thay đổi archive gốc hay các partition 01–09.
