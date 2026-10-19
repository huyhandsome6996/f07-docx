# Trạng thái xuất bản F04-docx — 19/10/2026

## ĐÃ XUẤT BẢN THÀNH CÔNG (cập nhật phiên làm việc sau)

- Nhánh **F04-docx (F viết hoa) đã tồn tại trên GitHub** `huyhandsome6996/f07-docx`, push từ bundle bằng PAT hoạt động trong môi trường phiên này (môi trường trước gặp 401/403 toàn đường Git — xác nhận là vấn đề đường xác thực môi trường, không phải PAT).
- Xác minh bằng `git ls-remote`: remote `F04-docx` = `767be5c32f0d12d4914eeacffb9ca956eb3107f3` = local HEAD (bundle nguyên bản). Commit cập nhật sau đó (báo cáo sửa N01+N02 + catalog): xem `git rev-parse HEAD` sau khi fetch.
- `main` @ `a4a4b0982db5ae5cd48892d0e8ebf85ba407fdd2` không bị đụng (không push/merge/reset/đổi default). Không force-push.
- Ghi chú: nhánh chữ thường `f04-docx` @ `e3a8f8b` từ lần bàn giao trước vẫn tồn tại trên remote; quyết định hiện hành dùng `F04-docx` (viết hoa). Việc dọn nhánh cũ thuộc quyền chủ repo.

## Lịch sử: lần chuẩn bị trước (giữ để rõ provenance)

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
