# Kiểm tra gói tài liệu F02

- Source ứng dụng c29469b được kiểm độc lập, không thay đổi tracked source trong lượt QA.
- Main repo tài liệu tại lúc tạo và push nhánh: a4a4b0982db5ae5cd48892d0e8ebf85ba407fdd2. Chỉ push ref F02-docx.
- Các đường bundles/, catalog/, updates/ và tools/ F07 kế thừa không thay đổi so với base.
- Manifest F02 riêng, không sửa catalog/checksum của gói F07.
- JSON parse được, Markdown fences cân bằng và các local link trong báo cáo chính tồn tại.
- Đã kiểm pattern GitHub/Cloudflare token và private key trong artifact mới, không có match. Đây là kiểm tra pattern giới hạn, không phải chứng nhận bảo mật.
- Tất cả fixture và ID trong HTTP evidence là synthetic local. Không đóng gói database hoặc log có bearer token/password thật.
- Quy định LF chỉ cho artifact F02 và root entry points bảo đảm manifest khớp trên Windows/Linux. Ảnh được giữ binary, không đổi bytes.
- Chỉ có snapshot tham chiếu, không phải gói deploy; mọi hướng dẫn bên trong source cũ là dữ liệu để đối chiếu.
