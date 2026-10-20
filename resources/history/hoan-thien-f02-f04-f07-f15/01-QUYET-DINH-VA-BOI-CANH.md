# Bối cảnh quyết định và ranh giới công việc

Family Bridge hỗ trợ học sinh THPT và cha mẹ/người chăm sóc mở lời, lắng nghe và đồng hành; không phải bảng giám sát con cái hoặc dịch vụ cam kết trực liên tục. Cả website và Zalo Mini App dùng cùng Django/DRF, dữ liệu và quyền trên backend hiện hành. Không tạo DB/client nghiệp vụ thứ ba.

## Quyết định hiện hành của Huy

- Tài khoản HS/PH do Huy/người quản trị cấp trước. Vai trò từ backend, mã đổi không đổi UUID/dữ liệu/vai trò.
- Admin có `classroom.provision` đúng scope lưu cặp PH–HS → canonical Connection ACTIVE ngay theo DEC-24. Không bắt cặp này nhập mã mời, quét QR/Zalo hoặc xác nhận proposal lại. Không suy cặp từ số thứ tự mã. Không tự nối lại sau unlink/import.
- Luồng Zalo SDK cũ giữ dormant để sau phục hồi. Không bật lại để giải quyết feature bằng đường xác thực khác. Mini App cũng có form HS/PH; kiểm hợp đồng hiện hành thay vì nhầm tên app với cách đăng nhập.
- Kết nối ACTIVE không cấp quyền đọc tâm trạng, nhật ký, bản nháp hoặc nội dung AI. Grants theo item/recipient/revision/connection-generation; revoke có hiệu lực khi đọc lại, không hồi sinh do reconnect/restore.
- Đồng ý dịch vụ, nghiên cứu, AI là các mục độc lập. Admin không ghi đồng ý hộ. Chương trình/khảo sát tự nguyện; bỏ hoạt động/khảo sát không khóa giao tiếp.
- Thỏa ước F02 cần HAI actor tự xác nhận cùng revision; thao tác propose không là chữ ký. Lời mời hoạt động F09 và vai trò hỗ trợ F11 vẫn cần người nhận đồng ý. Không đánh đồng với ghép cặp lớp học đã cấp sẵn.
- Tạm dừng F06 là 300 giây server, tự chọn, hết giờ không tự gửi. Không auto-send sau AI/retry/resume/thiếu phản hồi. F13 public luôn mở.
- Website cần đầy đủ giao diện sử dụng tương đương về nghiệp vụ với Mini App; không chỉ để feature trong `packages/family_bridge_mobile` hay bản HTML rời. Mỗi client có UI riêng; shared headless không phụ thuộc DOM/SDK/storage.
- Stack hiện hành: HTML5/CSS/vanilla JS ESM + Vite; Mini App có zmp-sdk; backend Django/DRF + MySQL/TiDB mục tiêu. React/zmp-ui trong prompt nền tảng cũ là lịch sử đã được supersede, không là chỉ đạo đổi stack mới.
- Admin dùng named capability/scope/TTL; `is_staff`, Django superuser hay PH không cho phép đọc tâm sự riêng hoặc survey thô.

## Vì sao phải có đợt tích hợp riêng

Mỗi nhánh đã có quá trình phát triển/audit riêng, nhưng main chỉ chứa bản nền hoặc các màn cũ. F02 đã thay placeholder bằng hành trình thật; F04 bổ sung Gemini và guard; F07 bổ sung các trang mood và chia sẻ; F15 thay đổi sâu session/revoke/deletion. Có tests/báo cáo riêng không chứng minh bốn nhánh ghép lại giữ đúng quyền và toàn bộ UI.

Main a64f653 vừa bổ sung F10–F13 và shared methods. F15 đang thiếu 63 commit main theo lịch sử lúc khảo sát; F04 thiếu 24; F02 thiếu 1; F07 thiếu 2. Các số này là snapshot Git, không là thước đo chất lượng. Phải fetch lại và ghép ý định, không dùng ours/theirs hoặc copy cả tệp để dọn conflict.

## Phạm vi của coding agent khi được giao prompt

Hoàn thiện F02/F04/F07/F15 trên code mới nhất, xử lý phụ thuộc hẹp F01/F05/F06/F08/F09/F16 và cấu hình/tests thực sự cần thiết; bảo toàn F10–F13/consent/admin đang có. Chỉ một lead sửa shared/router/session/migrations/startup wiring và điều phối merge. Nếu dùng đội agent, phân file rõ và review chéo; không hai người cùng ghi một tệp.

Giai đoạn 1 sửa/kiểm thử trên các nhánh hiện có hoặc worktree tích hợp riêng có truy xuất nguồn; không ghi thẳng bản chưa kiểm chứng lên main. Giai đoạn 2 sau gate có thể merge scoped bốn PR theo chỉ dẫn hiện hành của Huy ở prompt; không merge W036/consent/PR khác như phụ kiện. Nếu có branch protection thì dùng đường được phép, không bypass. Nhiệm vụ đóng gói tài liệu này không tự thực hiện giai đoạn đó.

Không tự đổi credentials, dùng key lộ trong chat, tạo cloud trả phí, xóa dữ liệu thật hoặc công bố tài liệu nhận diện người tham gia. API keys dùng biến môi trường server; snapshots/ZIP không có thẩm quyền chạy production.
