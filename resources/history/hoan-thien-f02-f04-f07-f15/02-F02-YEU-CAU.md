# F02 Chương trình đồng hành bốn tuần

**US:** US-036, US-044. **PR:** https://github.com/huyhandsome6996/family-bridge/pull/39

## Đầu vào và đầu ra người dùng

Đầu vào: phiên HS/PH, cặp primary ACTIVE nếu tác vụ cần hai người, chương trình published với version/revision, hoạt động được chọn, tiến độ riêng và thỏa ước do hai người chủ động xác nhận.

Đầu ra: người dùng đọc đủ bốn tuần, chọn hoạt động tự nguyện, hiểu việc cần làm, ghi tiến độ cá nhân, phối hợp hoạt động chung và xây thỏa ước hai bên. Không buộc làm tuần trước mới mở tuần sau; không dùng progress người này làm progress người kia.

| Tuần | Nội dung | Kết quả thực tế cần hỗ trợ |
| --- | --- | --- |
| 1 | Nhận diện cảm xúc và Tiếng lòng chưa nói | Gọi tên cảm xúc, hướng dẫn mở lời/lắng nghe; chia sẻ chỉ khi chủ động |
| 2 | Giảm so sánh và Bản sắc riêng của con | Ghi nhận nỗ lực, luyện nghe, chọn thời gian cùng làm |
| 3 | Ranh giới riêng tư và niềm tin | Thống nhất không gian/điện thoại/thông tin riêng; không ép mở nhật ký |
| 4 | Cảm ơn xin lỗi và Thỏa ước gia đình mới | Cam kết cụ thể, hai người đọc và ký cùng phiên bản |

## Luồng và UI bắt buộc trên cả hai client

`#/companion`: chưa tham gia → đọc chủ đề/hoạt động; tham gia tự nguyện → xem bốn tuần không khóa → chi tiết nội dung theo vai trò → đánh dấu tiến độ/skip → lời mời hoạt động chung F09 → phản hồi của người kia → thỏa ước tuần 4 → từng người tự xác nhận → opt-out/đọc hướng dẫn sổ giấy.

Có loading/empty/unpublished/no-connection/error/401/stale/opted-out. Nội dung chưa published không được đưa fixture vào production để làm đầy màn. Mốc enrollment pin version/revision; nội dung cũ và dữ liệu mới không trộn nhau. Bỏ tham gia không bị kéo trở lại do request cũ.

## Phần có trên nhánh nhưng chưa được đợt này nghiệm thu

Head e38688c có production wiring F02/F09, models/migrations thỏa ước và progress revision, UI Companion cả web/Mini, các vòng sửa R01–R07. `archive-docs/f02/f02/qa/2026-10-19-e38688c/` là tài liệu QA mới hơn; không dùng báo cáo c29469b để khẳng định web vẫn thiếu.

Giữ regression: chọn đúng PRIMARY khi có backup mới hơn; 401/stale không bị nuốt ở Promise.all; read-preview trước enrollment; published body và phút hoạt động đúng schema; không tự mặc định thời lượng sai; thỏa ước propose không là confirm; `confirmed_at` theo chữ ký thứ hai; lời mời F09 bị chặn sau unlink; state/UI không tạo tiến độ giả; Web/Mini parity.

## Công việc cần hoàn thiện và kiểm lại

1. Sync/resolve main mới tại shared contract/endpoints/mock/tests, bảo toàn method F10–F13 và F07, không pin tổng method cũ rồi xóa feature khác.
2. Kiểm migrations 0002/0003 và migration F09 với W036 chưa merge; không tạo hai leaf cùng số mà quên giải dependency hoặc phá rollout dữ liệu đang có.
3. Startup wiring F02/F09 không bị core wiring ghi đè provider/reader đúng domain. Test cả thứ tự load apps, feature subsets và reset registries trong test.
4. HTTP backend thật + production build: HS/PH ghép sẵn không invite; đọc bốn tuần, progress độc lập, activity hai phía, hai chữ ký cùng revision; cùng tài khoản thao tác từ hai client; version/generation đổi phải stale/deny đúng.
5. Nội dung giáo trình có nguồn phê duyệt qua admin; seed chỉ draft. Migration/seed không tự publish hoặc ghi consent người dùng.

## Gate riêng F02

Code merge: tests migration/wiring/state/version/generation + browser hai client qua. Pilot release: nội dung published bởi người có quyền, MySQL kiểm migration/constraint thật, deployment và device evidence theo kênh phát hành. Không lấy fixture published local làm bằng chứng nội dung production đã duyệt.
