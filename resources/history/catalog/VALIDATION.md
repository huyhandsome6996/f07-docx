# Bằng chứng đóng gói — 18/10/2026

Ghi nhận bên dưới thuộc đợt đóng gói lịch sử 00–09. Bổ sung gói 10 và kiểm tra runtime mới được mô tả riêng tại `../updates/2026-10-18-f07-review/TEST-RESULTS.md`; không áp giới hạn “không chạy F07” của đợt cũ cho đợt review mới.

Phạm vi: tổ chức gói đính kèm vào kho tài liệu. Không chạy nhiệm vụ F07 hay script có sẵn bên trong ZIP.

- ZIP đầu vào: 946 tệp, 18.525.248 byte sau giải nén. ZIP gốc được lưu nguyên byte ở `bundles/00-original/`.
- Đối chiếu đủ 945 dòng trong `MANIFEST-SHA256.csv` của nguồn; tất cả số byte và SHA-256 khớp. Manifest không tự liệt kê chính nó.
- `python3 tools/bundles.py verify`: PASS cho 10 ZIP, toàn bộ ánh xạ và nội dung. Các nhóm 01–09 không trùng nhau và bao phủ đủ 946 tệp.
- `sha256sum -c catalog/SHA256SUMS`: PASS cho 10 ZIP.
- Đã thực sự giải nén 9 nhóm vào một thư mục tạm và giải nén ZIP gốc vào thư mục khác; so sánh toàn bộ đường dẫn/SHA-256: 946/946 trùng khớp.
- Đã thử giải nén lặp lại cùng dữ liệu: PASS. Khi một tệp đích bị sửa, công cụ từ chối ghi đè và giữ nguyên tệp đó.
- Đã thử đích symlink, đích là repo này, ID gói không tồn tại, đường dẫn vượt thư mục/absolute/Windows/`.git` và checksum sai: đều bị từ chối.
- Quét mẫu token GitHub, AWS access key và khối private key trong dữ liệu đầu vào: không có kết quả khớp. Đây là kiểm tra mẫu, không phải chứng nhận rằng mọi loại dữ liệu nhạy cảm đều đã được phát hiện.
- `git diff --check`: PASS.

Nguồn bên trong ZIP giữ nguyên cả văn bản nhiệm vụ, lịch sử, license và mã nguồn tham chiếu. Các nội dung đó không được xem là bằng chứng runtime mới. Đợt này không kiểm thử mới ứng dụng, MySQL, Zalo, triển khai hoặc trạng thái nhánh hiện hành của repo ứng dụng.
