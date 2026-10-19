# Trạng thái xuất bản nhánh f04-docx — 19/10/2026

- Đã tạo nhánh **f04-docx tại local**, lịch sử gốc độc lập, có đầy đủ tài liệu/ảnh/prompt/bằng chứng F04 và catalog/checksum.
- Credential có sẵn của môi trường không dùng được. Sau khi người dùng chủ động cung cấp PAT và cho phép sử dụng, đã thử xác thực refs bằng header tạm và askpass tạm (cả Git môi trường và /usr/bin/git). GitHub trả `Invalid username or token` / `Authentication failed`; không thể vượt qua bước xác thực để push. Không ghi PAT vào repo/config/archive/log.
- **Chưa tạo hoặc push thành công nhánh f04-docx trên GitHub.** Local commit, thư mục và Git bundle không phải bằng chứng remote đã cập nhật.
- Không có lệnh push/merge/reset tới main. Main F07 chỉ được đọc để xác minh scope/provenance.
- Cần kết nối/quyền GitHub hoạt động được cho repo `huyhandsome6996/f07-docx`. Có thể dùng môi trường/chat đã đăng nhập GitHub để push bundle. Không cần sửa hoặc gửi lại tài liệu.

## Khôi phục từ Git bundle mà không đụng main

ZIP bàn giao chứa thư mục tài liệu `f04-docx/`, Git bundle `f04-docx.bundle` và `RESTORE.md`. Giải nén, rồi dùng bundle trong môi trường có quyền GitHub:

```bash
git clone -b f04-docx /duong-dan/f04-docx.bundle /tmp/f04-documents
cd /tmp/f04-documents
git remote set-url origin https://github.com/huyhandsome6996/f07-docx.git
python3 tools/catalog.py verify
git push -u origin f04-docx
```

Nếu remote f04-docx đã được người khác tạo sau đó, dừng để fetch/đọc diff và hợp nhất tài liệu đúng nhánh; không force-push. Không đổi target thành main. Sau push phải xác minh remote SHA đúng local HEAD, rồi mới cập nhật trạng thái publish và catalog ở nhánh f04-docx.

## Xác minh sau lần xác thực bằng PAT

GitHub HTML trả 404 cho `/tree/f04-docx`; main vẫn `a4a4b0982db5ae5cd48892d0e8ebf85ba407fdd2`. Vì vậy trạng thái chính xác là **LOCAL_READY — REMOTE_AUTH_BLOCKED**, không phải đã xuất bản. Credential session tạm đã đóng.
