# F04 AI hỗ trợ diễn đạt cho học sinh và người chăm sóc

**US:** US-029, US-033. **PR:** https://github.com/huyhandsome6996/family-bridge/pull/40

## Đầu vào và đầu ra

Đầu vào: nội dung tác giả chủ động viết và chọn nhờ AI, đồng ý xử lý AI còn hiệu lực, UUID/session/revision hiện hành, cấu hình provider hợp lệ ở backend. Không lấy toàn bộ lịch sử/mood/journal gửi AI.

Đầu ra: gợi ý diễn đạt giữ cảm xúc/nhu cầu/ý chính, giảm công kích; tác giả đọc, sửa, dùng hoặc bỏ. Áp dụng gợi ý chỉ đổi ô soạn, không tự gửi. Câu gốc và lịch sử trao đổi AI không đi kèm thư cho người nhận. Khi AI tắt/hỏng, viết tay và help vẫn hoạt động.

## UI và tài nguyên

Luồng ở `#/compose` và phản hồi thư phù hợp: soạn → thông báo xử lý/đồng ý nếu cần → người dùng yêu cầu AI → loading/cancel → đọc/sửa gợi ý → chủ động áp dụng/bỏ → chọn người nhận → preview bản được duyệt → xác nhận gửi; pause 300s tự chọn, không ép chờ để dùng AI.

`archive-docs/f04/designs/original/` có hai ZIP Stitch gốc. `designs/extracted/` chứa web và Mini App frames; kiểm ma trận nguồn trong `reports/2026-10-19-ec29ab-ui-matrix.md` và cập nhật parity theo code cuối. Mọi state phải có counterpart hợp lý ở cả hai client; keyboard/mobile/desktop là biến thể của luồng, không tạo route giả. Không dùng ảnh thiết kế làm ảnh nghiệm thu implementation.

## Trạng thái nguồn

Head d33b250 có các vòng sửa N01–N06. Báo cáo mới `archive-docs/f04/reports/2026-10-19-d33b250.md` ghi CODE_VERIFIED_LOCALLY và RELEASE_BLOCKED_EXTERNAL; đây là kết luận được lưu của reviewer tại thời điểm ấy, chưa phải kết quả chúng ta vừa chạy lại. Không làm lại các lỗi đã sửa nếu không tái hiện được trên source mới.

Giữ regression: preview snapshot bất biến khi edit đang bay; claim AI identity/khóa lượt gọi chống provider charge trùng; recipient bind liên client; copy theo vai PH/HS; vùng chạm 44px; F06 expected_revision phát hiện edit conflict; session/actor switch không áp gợi ý của tài khoản cũ. Không kết luận tất cả đã chạy live Gemini.

## Công việc tích hợp cần kiểm

1. Giữ Gemini allowlist/timeout/quota, network ngoài transaction; claim operation bền vững và idempotency; thiếu/tắt provider phải fail-closed trung thực.
2. Consent AI được kiểm trước gửi provider và trước finalize; rút qua F15 phải chặn kết quả/request cũ. Không auto-consent hoặc dùng Zalo login để vượt gate.
3. F15 deletion hook AI phải đồng nhất với registry/provider ownership sau merge; yêu cầu xóa/withdraw có kết quả thật, không chỉ đổi nhãn UI. Không đăng ký hai hook cùng category rồi vô tình bỏ một hook.
4. Giữ F06 send transport và expected_revision, optional pause; bảo toàn F10–F13 shared methods trên main. CSS conflict ghép theo component scope, không ghi đè toàn bộ components.css.
5. Các biến `GEMINI_API_KEY`, `GEMINI_MODEL`, `FB_AI_ENABLED`, timeout/token budget chỉ tên/placeholder trong docs. Key từng lộ phải được rotate qua kênh bảo mật; không sao chép ảnh lộ key.

## Gate riêng F04

Merge code chỉ khi tests provider doubles, validation/claims/concurrency, consent withdrawal, stale/recipient/revision, UI hai client và cấu hình OFF an toàn đạt. Nếu chưa có Gemini live thì giữ feature OFF, ghi NOT_RUN/BLOCKED; không đánh dấu AI sử dụng thực tế hoàn tất. Release AI cần key hợp lệ chưa lộ, cấu hình/chi phí/retention đã chốt, smoke live với dữ liệu giả và chứng minh có thể tắt an toàn.
