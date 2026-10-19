# Trạng thái xuất bản F04-docx — 19/10/2026

**LOCAL_READY — ENVIRONMENT_GIT_AUTH_BLOCKED. Chưa xác nhận tạo/push nhánh trên GitHub.**

## Tên và ranh giới

Yêu cầu mới nhất chọn chính xác `F04-docx`, thay cho tên chữ thường của lần chuẩn bị trước. Repo tài liệu: `huyhandsome6996/f07-docx`. `main` thuộc F07, không sửa/push/merge/reset và không đổi default branch. Nhánh tài liệu có gốc độc lập, không chứa tài liệu F07.

## Kết quả xác thực mới

Người dùng chủ động cung cấp PAT mới và cho phép sử dụng. Chỉ dùng credential trong session tạm, không ghi giá trị vào repo, Git config hoặc archive; đã đóng session sau kiểm tra.

- Git refs với askpass tạm và /usr/bin/git: HTTP 401 / Invalid username or token.
- HTTP smart-Git kiểm tra với và không gắn PAT: đều 401, request ID khác nhau.
- Đối chứng public repo git/git không gắn PAT: cũng 401 / Invalid username or token.
- api.github.com: proxy từ chối CONNECT 403.

Các kết quả này xác nhận đường xác thực Git trong môi trường chưa hoạt động; chưa đủ cơ sở kết luận riêng PAT mới sai/thiếu quyền. Cần khôi phục kết nối GitHub/credential routing của môi trường, không tiếp tục yêu cầu tạo token dựa riêng vào lỗi trên. Cấu hình draft không tự áp dụng lên runtime.

## Xuất bản từ Git bundle ở môi trường có GitHub hoạt động

ZIP bàn giao có thư mục `F04-docx/`, `F04-docx.bundle` và `RESTORE.md`. Giải nén rồi chạy trong thư mục mới:

```bash
git clone -b F04-docx /duong-dan/F04-docx.bundle /tmp/F04-documents
cd /tmp/F04-documents
git remote set-url origin https://github.com/huyhandsome6996/f07-docx.git
python3 tools/catalog.py verify
git ls-remote --heads origin refs/heads/main refs/heads/F04-docx
# Nếu remote F04-docx đã tồn tại, fetch và đọc diff trước; không force-push.
git push -u origin HEAD:refs/heads/F04-docx
git ls-remote --heads origin refs/heads/F04-docx
git rev-parse HEAD
```

Chỉ gọi đã xuất bản khi remote SHA đúng local HEAD. Sau đó cập nhật báo cáo/cấu trúc catalog đúng nhánh F04-docx. Không đổi target sang main để né lỗi.
