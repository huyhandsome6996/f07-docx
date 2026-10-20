# Kết quả kiểm tra bộ bàn giao

Ngày: 19/10/2026. Scope: tài liệu và tài nguyên cho F02/F04/F07/F15; runtime ứng dụng N/A trong lần đóng gói.

## Đã thực hiện

- GitHub plugin xác minh repo f07-docx, quyền push và default main; tạo nhánh `tai_lieu_hoan_thien_F02_F04_F07_F15_docx` từ docs main e286f85. Chưa sửa hoặc merge repo ứng dụng.
- Fetch các refs ứng dụng và docs; pin app main a64f653, F02 e38688c, F04 d33b250, F07 3fe66cd, F15 aeae321. Full SHA có trong branch-and-conflicts.json; docs source refs trong documentation-refs.json.
- Mười phép `git merge-tree --write-tree --name-only`: bốn nhánh với main và sáu cặp feature; đều exit 1 với textual conflicts. Không thay worktree/ref ứng dụng, không giải conflict hoặc chạy runtime từ cây ghép.
- 1.511 tệp nguồn được sao chép theo full SHA và giữ byte, size, hash trong SOURCE-FILES.csv; source-exclusions.json không có tệp bị loại ở snapshot này. Các tệp dedup theo Git blob có mapping đến tài liệu kế thừa hoặc F04-docx.
- Thêm yêu cầu chi tiết, bối cảnh HS/PH prelinked, prompt hoàn thiện, prompt merge, conflict decisions/test matrix/release rollback và mẫu log. Prompt root bằng byte với prompt lead trong kit.
- Word hướng dẫn 4 trang được render bằng renderer và kiểm trực quan đủ 4 PNG cuối; không clipping/overlap/mất dấu hoặc đường màu dưới tiêu đề. QA PNG chỉ dùng nội bộ, không đưa vào gói.
- `python3 tools/package_integration_kit.py`: tạo ZIP13 và inventory, bảo toàn ZIP00–12. `python3 tools/validate_integration_kit.py`: kiểm coverage/size/SHA nguồn và kit, CRC/đường dẫn member ZIP, prompt equality, PASS.
- `python3 tools/bundles.py verify`: 14 ZIP, 946 file gốc/945 hash manifest gốc giữ nguyên; các partition không trùng và khôi phục đúng byte. Tất cả supplement gồm ZIP13 được kiểm inventory. ZIP13 là gói hướng dẫn/provenance, không lặp source-reference/archive-docs; các file này được lưu trực tiếp trên nhánh và kiểm bởi CHECKSUMS/SOURCE-FILES. Số file cụ thể của kit cuối xem catalog/INTEGRATION-CONTENTS.csv; report này tự nằm trong inventory sau lần rebuild cuối.
- Đối chiếu riêng 13 ZIP kế thừa với catalog main docs: SHA256 nguyên vẹn. Không repack archive gốc.
- Quét mẫu credential GitHub/Gemini/AWS/private-key trên 1.666 plain file và nested members của kit ở lượt trước khi thêm chính report này: 0 findings. Không in giá trị secret. Đây là kiểm mẫu, không chứng nhận phát hiện mọi loại bí mật.
- 15 tệp Markdown tác giả mới/entry point có local Markdown link được kiểm: không missing link. Snapshot/archive giữ nguyên context đường dẫn nguồn, không sửa link lịch sử để giả là checkout hiện hành.
- Kiểm whitespace cho phần tác giả mới và catalog (loại source-reference/archive-docs giữ nguyên byte) PASS. Full `git diff --cached --check` ghi cảnh báo whitespace/new-EOF có sẵn trong snapshot code/HTML/log/patch nguồn; cố ý không sửa byte lưu trữ hoặc hạ checks ứng dụng. Kiểm staged content/remote/branch trước push; đối chiếu remote SHA sau push ghi trong báo cáo trả Huy.

## Giới hạn và gate

Chưa chạy lại suites app trong lần đóng gói; mọi test counts/PASS runtime của source report là bằng chứng lưu của reviewer tại source SHA, không là kết quả mới của bộ này. Chưa audit đầy đủ commit a64f653 hay bốn nhánh tích hợp, MySQL/Gemini/live Render/Zalo device NOT_RUN ở nhiệm vụ này. Chưa có bản hợp nhất ứng dụng để tuyên bố MERGE_READY hoặc RELEASE_READY.

Các script mới dùng Python chuẩn, input là repo paths/CSV/ZIP đã định, bounds 20.000 files và 100 MiB/file, không network hoặc thực thi script bên trong archive; packaging tool chỉ ghi kit manifests/ZIP13/catalog ở đúng nhánh được giao. Chi phí đọc/hash tuyến tính tổng bytes, bộ nhớ theo một file hoặc ZIP được kiểm; không là performance benchmark ứng dụng. Không thay đổi skill logic nguồn; chỉ lưu snapshot SKILL/rule với provenance.
