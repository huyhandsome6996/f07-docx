# Đặc tả giao diện Mini App — nguồn triển khai

Đây là đặc tả màn đích, KHÔNG phải xác nhận màn đã code/test. Có thể dùng tab/sheet/detail để tránh tăng route hình thức. Không bắt buộc tạo đúng 40 route.

## Hệ thiết kế

- Màu coral/vàng ấm/nền kem theo tokens hiện hành Family Bridge; không đổi sang nâu chủ đạo.
- Ưu tiên font hệ thống đọc tiếng Việt tốt trên Zalo; asset font cũ là tham khảo, không ép tải font nặng.
- Vùng chạm >=44×44 CSS px, ưu tiên 48; copy dễ đọc, label thật; text lớn không mất thao tác.
- Trang 320/360/390/430 CSS px; layout một cột, sections/cards vừa phải. Không sidebar desktop hay khung điện thoại giả trong ứng dụng.
- Action bar/back/menu của host Zalo: không vẽ nút chồng menu góc phải; tránh inset cộng hai lần. Back không làm mất lời đang soạn.
- Bottom navigation ít mục; ưu tiên 4 tab theo khuyến nghị Zalo hiện hành; phân nhóm chức năng khác bằng menu rõ.
- Khi bàn phím mở: textarea/nút lỗi/preview/gửi vẫn cuộn tới; không fixed bar che.
- Animation nhẹ/phản hồi trạng thái, tôn trọng reduced motion. Không loop trang trí/emoji dày.
- Loading/empty/error/expired/revoked/success hiện riêng, không success giả.
- Chi tiết thư sent và received khác chức năng, không chỉ đổi màu bong bóng.

Nguồn chính thức: https://docs.zaloplatforms.com/docs/MA/intro/zalo-mini-program-design-guidelines
Đã đối chiếu khi đóng gói; agent đọc lại trước triển khai.

## Các màn/trạng thái đích

| # | Màn | Nội dung/chức năng chính |
| --- | --- | --- |
| 01 | Chào mừng | Nhận diện, mục đích, bắt đầu/đăng nhập; không giả số người tham gia |
| 02 | Cách sử dụng | Bước ngắn theo HS/PH cấp sẵn, không yêu cầu mã mời lớp học |
| 03 | Đăng nhập | Mã HS/PH, mật khẩu, lỗi dễ hiểu, bàn phím không che nút |
| 04 | Đồng ý sử dụng | Từng mục đích/chính sách, không tick sẵn |
| 05 | Trang chủ học sinh | Lối vào mood, gửi lời, đồng hành, nhật ký, tín hiệu |
| 06 | Trang chủ người chăm sóc | Thư/tín hiệu nhận, đồng hành, hoạt động và phản hồi |
| 07 | Người đồng hành | Cặp đúng danh tính, trạng thái active/unlink rõ |
| 08 | Đồng hành bốn tuần | Bốn chủ đề, tự nguyện, không khóa tuần |
| 09 | Chi tiết tuần | Nội dung/chủ đề/hoạt động riêng và chung |
| 10 | Chi tiết hoạt động đồng hành | Hướng dẫn, tham gia/chọn phần mình, tiến độ thật |
| 11 | Thỏa ước | Cùng revision, hai người tự chấp nhận; không ký hộ |
| 12 | Thẻ cảm xúc | Danh mục có hình minh họa, chọn một thẻ |
| 13 | Xem trước thẻ | Recipient + nội dung cuối, sửa lựa chọn rồi preview lại |
| 14 | Soạn lời nhắn | Nội dung riêng, recipient, AI, lưu nháp, preview/gửi |
| 15 | Danh sách nháp | Nháp của mình, mở/sửa/xóa theo quyền |
| 16 | Tạm dừng năm phút | Mốc server, hết giờ vẫn chờ xác nhận; help ngay |
| 17 | AI gợi ý | Consent, đang tạo/hủy chờ, bản gốc/gợi ý, dùng/bỏ/stale |
| 18 | Hộp thư | Phân biệt gửi/nhận/hồi âm, pagination có giới hạn |
| 19 | Chi tiết thư nhận | Tác giả thật, body, composer phản hồi + AI, read đúng actor |
| 20 | Chi tiết thư đã gửi | Body mình gửi, recipient thật; không tự phản hồi |
| 21 | Ghi tâm trạng | Chọn cảm xúc/note riêng, lưu có xác nhận server |
| 22 | Lịch sử tâm trạng | Cá nhân, phân trang, sửa/chia sẻ từng mục |
| 23 | Tâm trạng được chia sẻ | Chỉ grant hợp lệ, không mặc định xem cả lịch sử |
| 24 | Sổ nhật ký | Trang của mình, riêng/song hành, không placeholder |
| 25 | Viết/đọc trang nhật ký | Body an toàn, save/revision, chia sẻ từng trang |
| 26 | Trang nhật ký được chia sẻ | Grant/revision, phản hồi context và revoke |
| 27 | Hoạt động kết nối | Danh sách thật, lọc/empty, mở chi tiết |
| 28 | Bài học ngắn | Đọc nội dung đầy đủ, không chỉ title trên home |
| 29 | HS phát tín hiệu | Nhu cầu + người nhận + preview + explicit send |
| 30 | PH nhận tín hiệu | Mục received, ack đúng người, mở thư/viết hồi âm |
| 31 | Danh sách điểm tựa | Mời/chấp nhận/trạng thái/expiry, tự chọn người |
| 32 | Chi tiết điểm tựa | Liên hệ/gửi tin/đọc thật, quyền đúng vai trò |
| 33 | Lịch hẹn | Yêu cầu của mình/được giao, trạng thái thật, hủy có guard |
| 34 | Đặt lịch hẹn | Đầu mối trường thật, thời gian, ghi chú chỉ đúng người |
| 35 | Tìm trợ giúp | Danh bạ đã xác minh, giờ/số, nút mở gọi chủ động |
| 36 | Danh sách khảo sát | Tự nguyện, trước/sau, chưa làm/đã gửi |
| 37 | Làm khảo sát | Form thật, review/submit, không khóa tính năng khác |
| 38 | Quyền riêng tư | Đồng ý, unlink, yêu cầu xóa, trạng thái rõ |
| 39 | Chia sẻ từng mục | Đúng nội dung/recipient/revision, thu hồi có xác nhận |
| 40 | Cài đặt tài khoản | Tên/mật khẩu/mã đăng nhập theo contract, logout sạch |

## Cách dùng tài nguyên gốc

Toàn bộ cây tài liệu lịch sử từ nhánh tổng hợp đã được nhúng dưới resources/history/.
- Tìm hình/frame/code bằng tên zalo_/mini; F04 có nguyên bộ Stitch dành riêng Zalo.
- Tìm logo/ảnh/font trong các thư mục assets/designs của gói; catalog và các ZIP lịch sử được giữ nguyên.
- Web frames để đối chiếu tính năng; không copy desktop shell hoặc CSS web sang Mini nguyên trạng.
- Dùng asset hiện có với giấy phép đi kèm; không tạo nội dung user giả.
- Snapshot source là tham khảo theo SHA, không thay current checkout hay bằng chứng runtime.
