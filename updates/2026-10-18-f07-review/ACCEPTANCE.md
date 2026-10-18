# Đối chiếu lại 25 tiêu chí F07

Mốc kiểm `bb75b2c`, 18/10/2026. PASS local chỉ là phạm vi được nêu; không thay nghiệm thu MySQL/Zalo/production. Bảng này thay các tuyên bố PASS rộng hơn trong bàn giao nhánh tại cùng SHA.

| ID | Trạng thái mới | Bằng chứng / phần còn thiếu |
| --- | --- | --- |
| F07-01 | PASS local | HTTP login 3 actor; browser form HS thật; không kiểm Zalo SDK |
| F07-02 | PARTIAL | Route `/mood` hoạt động, wiring và client suite đạt; chưa click lại mọi đường home/profile navigation |
| F07-03 | PASS local | HTTP tạo 201, riêng tư mặc định; UI tải note từ DB |
| F07-04 | PASS local | Browser login mới đọc lại mục được HTTP lưu trước đó; không dựa state tab cũ |
| F07-05 | PARTIAL | Trùng ngày HTTP 400; MySQL xác nhận 1 row/created+InputInvalid nhưng race test FAIL do R04 |
| F07-06 | FAIL concurrency | Edit tuần tự đạt; R02 hai transaction tái dùng revision |
| F07-07 | FAIL format | R05 ngày sai suffix trả 201; enum/note/UUID checks hiện có đạt |
| F07-08 | PARTIAL | Own pagination 2/50 đạt; recipient list nhiều owner lỗi R03; query-count check cũ đạt trong case của nó |
| F07-09 | PASS tested cases | Module/integration admin/cross-user deny đạt; HTTP stranger 404 |
| F07-10 | PASS tested cases | Module share cần active connection; synthetic stranger vẫn tạo mục riêng |
| F07-11 | PASS local/MySQL integration | Admin-provisioned invite NULL dùng được trong test thật |
| F07-12 | PASS local basic | Sheet hiện đủ note và revision; HTTP chia sẻ đúng recipient; lifecycle sheet vẫn lỗi R01 |
| F07-13 | PARTIAL | Preview stale tuần tự 409 đạt; đồng thời cần sửa R02 và kiểm share boundary |
| F07-14 | FAIL concurrency | Grant tuần tự đúng; R02 làm nội dung chưa duyệt dùng cùng revision |
| F07-15 | FAIL multi-owner | R03 detail đọc được 2 mục nhưng list chỉ trả 1 |
| F07-16 | PASS tested cases | F07 revoke chặn read tiếp theo, HTTP và module tests |
| F07-17 | PASS tested cases | Re-share tường minh sau revoke hoạt động; giữ regression sau sửa concurrency |
| F07-18 | FAIL concurrency | Edit tuần tự ẩn grant cũ đạt; R02 vẫn có interleaving làm lọt bản chưa duyệt |
| F07-19 | PASS tested cases | Integration reconnect/generation và HTTP unlink đạt; bổ sung multi-owner khi sửa R03 |
| F07-20 | PARTIAL | Missing-reader test fail-closed đạt; chưa thử độc lập mọi exception/failure của provider |
| F07-21 | PASS tested cases | Provider thật + F15 revoke chặn F07 trong HTTP/MySQL integration |
| F07-22 | PARTIAL | Deletion hook thật/idempotent đạt; không chạy quy trình purge/backup/production |
| F07-23 | FAIL browser | R01 private preview còn trên trang help/login sau clearSession; late-response/actor-switch cần bổ sung |
| F07-24 | PARTIAL | Client suite đạt một số trạng thái; chưa kiểm độc lập mọi unknown write outcome, offline/resume và revoke error |
| F07-25 | FAIL browser text scaling | Bình thường 320/390/430 không tràn; CSS text 200% lỗi 320/390 (R06); device keyboard/safe-area NOT_RUN |

Không đổi trạng thái feature/US thành Done hoặc security control thành VERIFIED từ bảng này. Sau sửa, chạy lại cả positive/negative cases và ghi SHA mới cho từng bằng chứng. Không giữ PASS cũ cho code đã đổi mà chưa kiểm lại.
