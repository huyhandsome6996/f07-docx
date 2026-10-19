# Trạng thái xuất bản nhánh f04-docx — 19/10/2026

- Đã tạo nhánh **f04-docx tại local**, lịch sử gốc độc lập, có đầy đủ tài liệu/ảnh/prompt/bằng chứng F04 và catalog/checksum.
- Đã thử `git push -u origin f04-docx` bằng cơ chế credential có sẵn của môi trường. GitHub trả `Invalid username or token` / `Authentication failed`.
- **Chưa tạo hoặc push thành công nhánh f04-docx trên GitHub.** Local commit, thư mục và Git bundle không phải bằng chứng remote đã cập nhật.
- Không có lệnh push/merge/reset tới main. Main F07 chỉ được đọc để xác minh scope/provenance.
- Cần khôi phục kết nối/quyền GitHub sử dụng được cho repo `huyhandsome6996/f07-docx`. Không gửi token qua chat. Kết nối GitHub hoặc nhập credential qua cấu hình bảo mật của môi trường; nếu quyền đã có ở một chat khác, dùng chat đó để push bundle.

## Khôi phục từ Git bundle mà không đụng main

Bundle được bàn giao riêng ngoài repo. Tải nó vào môi trường có quyền GitHub, rồi dùng thư mục mới:

```bash
git clone -b f04-docx /duong-dan/f04-docx.bundle /tmp/f04-documents
cd /tmp/f04-documents
git remote set-url origin https://github.com/huyhandsome6996/f07-docx.git
python3 tools/catalog.py verify
git push -u origin f04-docx
```

Nếu remote f04-docx đã được người khác tạo sau đó, dừng để fetch/đọc diff và hợp nhất tài liệu đúng nhánh; không force-push. Không đổi target thành main. Sau push phải xác minh remote SHA đúng local HEAD, rồi mới cập nhật trạng thái publish và catalog ở nhánh f04-docx.
