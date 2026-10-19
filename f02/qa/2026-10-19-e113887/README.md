# F02 — Bản cập nhật sau khi sửa theo QA 19/10/2026 (nguồn e113887)

**Ngày:** 19/10/2026 · **Nguồn ứng dụng:** [family-bridge](https://github.com/huyhandsome6996/family-bridge), nhánh `tinh-nang/f02-dong-hanh-bon-tuan-us036-us044`, head **e113887** (commit cha trực tiếp là **c29469b3d57f2c2cc53fe686fe7ec8f917f2dec6** — đúng bản đã QA độc lập). Main của kho ứng dụng không bị đụng tới.

Đây là **bản cập nhật** của vòng QA [2026-10-19-c29469b](../2026-10-19-c29469b/README.md) — không ghi đè, không sửa bất kỳ tệp bằng chứng nào của vòng QA cũ. Bốn commit sửa lỗi trên nhánh F02:

| Commit | Nội dung |
| --- | --- |
| `ba244da` | Backend R02 + R04 + R03 + phần backend của R06 (+ 2 migration, 17 regression test) |
| `85ab7d1` | Mini App R01 + R05 + R06 (+ 8 regression test) |
| `652e29d` | Web R07: trang Companion web thật cùng API (+ 8 test, cập nhật pages.test) |
| `e113887` | Đính chính checklist thỏa ước trong `06-RESUME-HANDOVER` (propose không tính là chữ ký) |

## Trạng thái R01–R07 sau khi sửa

| Mục | Trạng thái | Bằng chứng chính |
| --- | --- | --- |
| R01 UI lấy revision cũ | **ĐÃ SỬA** (Mini + web parity) | policy "revision published cao nhất thắng, độc lập thứ tự, chặn draft/retired"; 3 test mini + 1 test web; repro R01 của QA GREEN |
| R02 đổi program revision kẹt thỏa ước | **ĐÃ SỬA** | identity `FamilyAgreement` thêm `program_revision` + migration 0003; 9 test Django; kịch bản HTTP thật 15/15 PASS ([http-r02-results.json](evidence/http-r02-repin-results.json)) |
| R03 accept lời mời sau hủy kết nối | **ĐÃ SỬA** | invite pin `connection_generation`; accept/own-response recheck; `NEW-F09-UNLINK` PASS khi chạy lại bộ HTTP của QA; 8 test Django |
| R04 `confirmed_at` sai thời điểm | **ĐÃ SỬA** | `max()` hai chữ ký; `NEW-TIMESTAMP` PASS khi chạy lại bộ HTTP của QA; 3 test Django (cả hai thứ tự actor) |
| R05 không đọc được hướng dẫn trước tham gia | **ĐÃ SỬA** | nút "Xem trước hướng dẫn từng tuần" chỉ-đọc, không POST enroll; ảnh [01](evidence/01-mini-not-enrolled-preview-closed.png), [02](evidence/02-mini-not-enrolled-preview-open.png); repro R05 của QA GREEN |
| R06 thiếu chi tiết hoạt động/thời lượng có nguồn | **ĐÃ SỬA** | backend trả body typed + minutes trung thực; UI có "Xem chi tiết hoạt động" (mục tiêu/cách làm/chia sẻ) + thời lượng kèm nguồn rev hoặc "chưa được cung cấp"; ảnh [04](evidence/04-web-activity-detail.png), [07](evidence/07-mini-activity-detail.png) |
| R07 web placeholder | **ĐÃ SỬA** | trang web thật gọi cùng API, dùng chung account/progress/agreement với Mini App (đã enroll + tick tiến độ trên WEB, đăng nhập MINI thấy cùng trạng thái — ảnh [06](evidence/06-mini-cross-client-shared-account.png)); không import DOM/zmp-sdk của mini (boundaries PASS) |

## Đọc tiếp

- [Chi tiết từng mục + cách kiểm lại](STATUS-R01-R07.md)
- [Kết quả tests, lệnh, môi trường và giới hạn](TEST-RESULTS.md)
- [Bàn giao cho agent/qa tiếp theo](HANDOVER.md)
- Bằng chứng: [http-results.json](evidence/http-recheck-results.json) (46/46), [http-r02-results.json](evidence/http-r02-repin-results.json) (15/15), ảnh UI `evidence/0*.png`, log test `evidence/*.txt`.

## Chưa xác minh (giữ trung thực như vòng QA cũ)

- **MySQL/TiDB race suites:** NOT_RUN (không có môi trường MySQL trong phiên làm việc này; SQLite chỉ chứng minh state machine). Các suite race vẫn skip đúng cơ chế gated.
- **Zalo thiết bị thật / Mini App trong host Zalo:** NOT_RUN. Mini App đã kiểm qua browser preview 3004 (browser preview, không phải host Zalo) và unit test happy-dom.
- **Production Render/Cloudflare/database:** KHÔNG đụng tới theo yêu cầu.
