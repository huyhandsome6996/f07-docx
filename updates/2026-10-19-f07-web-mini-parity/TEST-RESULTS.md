# Kết quả lượt kiểm tra 19/10/2026 (UTC+7)

Commit F07/PR #42: bb75b2cee314bd5dfea3fff7928664dc68d3e2dd. Không đổi source tracked ứng dụng. Các số sau thuộc lượt này; full backend/harness và HTTP 21 bước của 18/10 là lịch sử, không được cộng/gán thành kết quả mới.

| Kiểm tra | Kết quả | Bằng chứng |
| --- | --- | --- |
| Regression bổ sung MySQL R02/R03/R05 | 3 tổng, 3 FAIL | `evidence/mysql-regressions.log` |
| Create-race assertion R04 | 1 tổng, 1 FAIL | `evidence/mysql-create-race.log`; row/outcome đúng nhưng assertion thứ tự sai |
| Mini lifecycle + layout R01/R06 | 9 quan sát, 4 PASS + 5 FAIL | `evidence/mini-browser.log` và ảnh/JSON trong mini-browser/ |
| Browser smoke hai client + API thật R07 | 12 quan sát, 9 PASS + 3 FAIL | `evidence/client-parity.log` và client-parity/results.json |
| Mini App suite | 307 PASS | `evidence/mini-tests.log` |
| Web suite | 227 PASS | `evidence/web-tests.log` |
| Mini build + manifest/assets | PASS | `evidence/mini-build.log` |
| Web build | PASS | `evidence/web-build.log` |
| E2E UI web/Mini X01–X08 đầy đủ | BLOCKED_R07 | Web thiếu màn F07, không coi các adapter calls là UI E2E |
| Zalo thiết bị thật/production | NOT_RUN | Không có phạm vi/runtime; không deploy hoặc thử participant data |

## Phân biệt các quan sát

- Parity smoke xác nhận form login HTTP 200 và adapter list/detail HTTP 200 ở cả hai client. Web có đủ 8 method F07 được thêm qua shared factory. Đây là phần transport, không phải toàn bộ tính năng UI.
- 3 FAIL là web `/mood`, `/mood-shared` vào not-found và profile không có navigation F07. Mini App các phép kiểm tương ứng PASS.
- 2 phép PASS của quick mood web chỉ xác nhận click thực sự gọi backend và nhận HTTP 400 duplicate theo fixture đã có mục hôm nay. Không tuyên bố đã test tạo mới thành công, edit, share hoặc revoke qua UI web.
- R02 vẫn `final_revision=2 unapproved_readable=True`; R03 list 1 thay vì 2 grant; R05 ngày sai suffix vẫn HTTP 201.
- Text scaling 200% là tăng CSS font/line-height trong Chromium, không phải OS/device setting. Width 395px ở viewport 320/390 vẫn tái hiện.

## Môi trường, fixture và setup đã chẩn đoán

Backend Django dùng SQLite local trên port 8019; Mini App dev port 3019 và web dev port 5179 cùng trỏ đúng backend này. Backend được khởi động với CORS_ALLOWED_ORIGINS gồm cả hai origins. Không dùng proxy giả, mock response hoặc production backend. Ports chỉ phục vụ validation nội bộ, không phải URL giao cho Huy truy cập từ máy khác.

MySQL 8.4.11 Docker disposable loopback và mysqlclient 2.2.8 đã chuẩn bị từ review trước; credential random nằm ngoài repo. Regression dùng Django test database tự tạo/hủy. Browser dùng HSZE2E01 synthetic cho lifecycle, HSPAR19/PHPAR19 synthetic riêng cho parity, connection active admin_provisioned invite NULL. Không seed/reset/xóa dữ liệu người thật.

Lượt smoke đầu dùng fixture cũ đã unlink nên home không hiện quick card và bước chờ chip timeout. Đã xác định điều kiện fixture, tạo cặp parity riêng active và chạy lại thành công đến cuối (vẫn exit 1 do 3 finding R07). Timeout setup đó không được tính thành lỗi mới hoặc một phép PASS. Source home đang gate nội dung theo connection; UI F07 đầy đủ mới phải cho phép ghi riêng tư khi chưa kết nối.

Ban đầu exec transport tạm ngắt; kiểm tra shell tối thiểu với login=false thành công và các lệnh tiếp theo chạy được. Không còn blocker môi trường này.

## Lệnh tái hiện

Xem [repro/README.md](repro/README.md). Các runner ghi mã thoát thật: regression, race và browser smoke đều exit 1 trên baseline chưa sửa. Các suite npm/build exit 0. Logs không chứa auth headers/token/response body; API metadata đã thay UUID trong path bằng `<id>`.

Source-reference chỉ gồm tệp chọn lọc và hashes trong PROVENANCE.json; không thể dùng làm runnable checkout. Độ phức tạp của bản sửa runtime là N/A ở lượt cập nhật tài liệu này. Dữ liệu regression có giới hạn (2 edit workers + 1 share worker, 2 owners/1 recipient, page 20), không chạy stress hoặc khai thác production.
