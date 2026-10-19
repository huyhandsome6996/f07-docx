# Phát hành và khôi phục sau tích hợp

## Ranh giới ủy quyền

Nhiệm vụ hiện tại chỉ tạo bộ tài liệu và nhánh trong kho f07-docx; không merge hoặc deploy app ngay. Khi Huy dán prompt cho coding agent, phạm vi mặc định là hoàn thiện, kiểm thử và merge bốn feature khi gate đạt. Deploy production/submit Zalo chỉ thực hiện khi có chỉ dẫn hiện hành cho đúng kênh; không suy quyền từ tài liệu cũ đã trích. Ghi nhớ Render web auto-deploy có thể chạy sau merge main, nên merge phải có release plan và cấu hình an toàn từ trước.

## Render

- Backend hiện có: https://family-bridge-backend.onrender.com/
- Web hiện có: https://family-bridge-web.onrender.com/
- Giữ cùng DB/backend, không đổi domain hoặc dựng DB mới. Web build từ `web/` ra `web/dist`; VITE_API_BASE_URL là build-time, chỉ public API origin; CORS exact origin/headers theo hợp đồng.
- Main a64f653 có F10–F13/core wiring mới; phải kiểm backend live SHA và release độc lập hai service, không suy chúng tự cùng deploy.
- Migration additive có plan/dữ liệu cũ/backfill/backup/quyền chạy; không sửa migration đã triển khai. Render Free không mặc định có preDeployCommand. Không chạy migrate DB thật từ môi trường chưa được phép.
- Feature flags không giả tạo tính năng. AI chưa đủ key/policy thì default-off; F02 chưa published thì empty/unpublished honest; deletion thiếu operator/policy thì pending/failed-needs-action đúng.
- Chuẩn bị thứ tự backend/schema/client tương thích trước merge. Nếu web auto-deploy main không thể kiểm soát và thay đổi phá tương thích, đây là release risk phải giải trước, không merge để chờ tính sau.

## Zalo Mini App

Build/manifest đúng không đồng nghĩa đã lên bản Testing/production. Khi được giao phát hành: đọc tài liệu Zalo chính thức hiện hành, kiểm App/Mini App ID qua cấu hình bảo mật, phiên HS/PH, domain API, network permissions, safe area/native keyboard, Android/iOS, logout/reopen/cold start. Không dùng credential từng lộ. Bàn giao version/testing URL/QR hợp lệ khi thực sự tạo được; không gửi localhost container thành đường dẫn người dùng mở được.

## Giữ dữ liệu và rollback

- Trước merge lưu full SHA main/4 heads/CI/release artifacts bằng refs hoặc record có thể khôi phục. Không force hoặc rewrite lịch sử main.
- Revert code/restore deployment artifact qua đường hợp lệ; không drop DB để rollback, không inverse migration mất dữ liệu tự động, không rollback sổ cái revoke/deletion.
- Consumer cũ không được đọc schema nháp mới theo quyền rộng hơn; current revocation/deletion ledger phải tiếp tục áp trước serve sau khôi phục.
- Runtime incident: tắt feature hỏng nếu có flag đã được thiết kế, giữ help/login an toàn; logs khử secrets, audit rõ. Không giảm auth/CSRF/TLS/CORS để thông luồng.
- Kiểm tra sau merge nếu regression: báo ngay, khoanh vùng commit/source, chạy canary, revert có kiểm soát phần sai. Không tuyên bố merge an toàn tuyệt đối vì đã qua tests.

## Bàn giao phát hành

Code SHA/PR/head đã merge, required checks, snapshot trước/sau; migration applied thực tế; deploy ID/SHA từng service; URL và actor/case live đã test; flags/nội dung/operator đã hoặc chưa sẵn; MySQL/Gemini/device gaps; rollback cụ thể. Không gắn nhãn “Done” cho dữ liệu/policy/phát hành chưa được xác minh.
