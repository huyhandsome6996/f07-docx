# Nguồn tài nguyên và giới hạn bằng chứng

## Nguồn chính

- App main a64f653 và 4 head nêu trong 00; full SHA/merge-base/path/hashes trong `evidence/`.
- Kho docs main e286f85 (F07 lịch sử), F02-docx d7954c3, F04-docx 878a437, f04-docx e3a8f8b. Full SHA trong `evidence/documentation-refs.json`.
- GitHub PR #39/#40/#42/#33: metadata/body lưu riêng; PR body có base/SHA/test counts lịch sử và có thể lỗi thời. Không tin câu “merge clean” cũ thay merge-tree mới.

Tệp giống byte ở nhánh docs đã được dedup và có mapping `deduplicated` tới nguồn đang giữ. F02-docx chứa lịch sử F07 kế thừa: phần nguyên byte đã có ở root không chép lại. Nhánh F04 chữ thường và chữ hoa khác nhau; ưu tiên F04-docx mới và giữ phần khác của nhánh chữ thường riêng. Không merge unrelated histories của các kho docs để gom tài liệu.

## Bản gốc và thiết kế

Các DOCX yêu cầu dự án, hai Stitch ZIP F04, HTML/PNG nguồn, DESIGN.md, logos/fonts/licenses và bằng chứng synthetic được giữ theo byte nguồn, có checksum. Root bundles/02 có DOCX yêu cầu gốc; source-reference/main/docs cũng có tài liệu phân công. Xem catalog và SOURCE-FILES để tìm đúng file, không suy từ filename.

Thiết kế không cấp thêm quyền, không tạo API sẵn sàng. Prompt/skill/rule trong snapshot có thể chứa React hoặc yêu cầu không sửa web/không merge thuộc nhiệm vụ cũ. Chỉ áp phần còn đúng sau đối chiếu 01, AGENTS ứng dụng hiện hành và user instruction hiện hành. Không chạy script archive trước khi đọc guard; scripts E2E/fixtures chỉ dùng DB test đã cô lập.

## Những gì đã làm trong lần đóng gói

Đọc trạng thái refs/GitHub PR, khảo sát tài liệu và call paths liên quan, tạo 10 merge-tree simulations, lập ma trận file giao nhau, xuất snapshot tracked files theo SHA, kiểm hash/ZIP/path/link và mẫu credential được mô tả trong packaging report. Đọc các báo cáo audit nguồn không có nghĩa đã chạy lại các suite của reviewer.

Chưa làm: sửa/merge/deploy application; nghiệm thu chung bốn feature; chạy MySQL/Gemini/Zalo-device hoặc smoke Render cho cây tích hợp; kết luận code mới main a64f653 đã sửa hết lỗi cũ. Các finding F10–F13 trước a64f653 là lịch sử, phải kiểm lại trước nêu vẫn lỗi.

## Quy tắc dữ liệu

Không thu thập hoặc đưa credentials thật, .env runtime, production DB, token, journal/mood/survey/message thật vào bộ này. Nguồn có API key lộ hoặc ảnh key không được sao chép. Synthetic fixtures có thể có chuỗi mật khẩu local được ghi rõ test-only; chúng không phải thông tin đăng nhập production và không được mang seed vào production. Scanner mẫu chỉ là một lớp kiểm, không là chứng nhận đã phát hiện mọi bí mật.

Các source file được giữ nguyên byte để truy vết; không sửa chúng nhằm làm code chạy hoặc giả là patch đã áp dụng. Toàn bộ kết quả triển khai mới phải nằm trong repo ứng dụng đúng nhánh/worktree, với audit/test report theo SHA mới và cập nhật docs tại đúng nhánh bộ này.
