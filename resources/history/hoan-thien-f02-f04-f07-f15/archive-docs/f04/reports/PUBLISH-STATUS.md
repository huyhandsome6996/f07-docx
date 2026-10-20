# Trạng thái xuất bản F04-docx — 19/10/2026

**PUBLISHED — ĐÃ push ff-only và xác minh `git ls-remote` remote = local.**

- Lần 1: môi trường audit publish nhánh `F04-docx` @ `42b4b42` (bao gồm báo cáo ec29abb N01/N02).
- Lần 2 (phiên này): sync toàn bộ bộ lưu trữ audit ZIP (nguồn 788152c — 277 file: reports ec29ab + UI matrix, evidence 113 file, repro/ec29ab, references/family-bridge-ec29ab) lên nền 42b4b42 bằng commit mới; giữ `reports/2026-10-19-ec29abb.md` làm lịch sử; thêm `reports/2026-10-19-d33b250.md` (vòng fix N03–N06). KHÔNG force-push; main F07 không đụng.
- Code ứng dụng đi kèm: `huyhandsome6996/family-bridge` nhánh `tinh-nang/f04-ai-ho-tro-dien-dat-us029-us033` @ `d33b250f16cab362cb3d93908274ea1df2967351` (đã verify ls-remote).

Tên nhánh: `F04-docx` (F viết hoa), repo tài liệu `huyhandsome6996/f07-docx`. Main thuộc F07, không sửa/push/merge/reset, không đổi default branch. Lịch sử nhánh local độc lập để không trộn F07.

Lịch sử chẩn đoán lần trước (giữ để đối chiếu): Git smart-HTTP của môi trường audit trả 401 với credential người dùng cung cấp và cả không gắn credential; public control git/git cũng 401; api.github.com CONNECT 403. Phiên làm việc sau này với PAT khác đã push thành công — ghi nhận đây là vấn đề môi trường audit, không phải PAT sai. Không lưu token trong repo/archive.

Bộ ZIP audit mới có đầy đủ cây tài liệu, catalog, ảnh, ZIP Stitch gốc, báo cáo và repro, **không chứa .git/Git bundle** để tránh nhân đôi toàn bộ ảnh/ZIP và giữ file bàn giao nhỏ. Các bundle/ZIP lần trước là lịch sử riêng, không là nguồn audit mới và không cần để triển khai F04. SHA và Git metadata không thay thế evidence mới.

Khi có GitHub hoạt động, clone repo vào thư mục riêng, kiểm tra remote F04-docx:
- Nếu đã có nhánh, checkout/fetch nhánh đó, đọc diff và hợp nhất các tài liệu mới; không force-push.
- Nếu chưa có, tạo orphan branch F04-docx trong checkout riêng không có dữ liệu chưa lưu, rồi đặt cây tài liệu F04 từ ZIP vào nhánh; không copy F07 vào F04.
- Build/verify tools/catalog.py, git diff --check, commit và push CHỈ HEAD:refs/heads/F04-docx.
- Xác minh remote SHA trùng local HEAD và main không đổi. Chỉ sau đó báo xuất bản thành công, cập nhật provenance và catalog.

Không đổi target sang main để né lỗi. Không chờ xuất bản tài liệu mới sửa/test app trong family-bridge. ZIP chỉ là dữ liệu bàn giao, không là quyền chạy script/deploy/merge application.
