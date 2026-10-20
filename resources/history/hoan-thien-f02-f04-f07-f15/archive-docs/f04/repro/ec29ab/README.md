# Chạy lại audit ec29ab bằng dữ liệu tổng hợp

Đọc và kiểm tra script trước khi chạy; không dùng DB thật/Render. Không sửa assertion để làm xanh.

1. Tạo thư mục mới, đặt `F04_AUDIT_DIR` tới đó. Lấy archive chính thức tại full SHA `ec29abbb60bb5948fff2e87e63b0db5e0cdc4333` và giải nén an toàn vào `$F04_AUDIT_DIR/source`. Không checkout/reset app của người dùng.
2. Cài venv ở `$F04_AUDIT_DIR/venv` theo `source/backend/requirements.txt`; cài web/Mini bằng package-lock (`npm ci`). Lần audit đã so lockfile không đổi và tái dùng dependency đã cài. Không copy node_modules hoặc DB từ ZIP.
3. Copy các helper trong thư mục này vào `$F04_AUDIT_DIR`. `run_checks.py` chạy nhóm `backend`, `feature`, `web`, `mini`, `shared`, `probes`, lưu log/exit code và command JSON. Harness uses SQLite/test DB riêng.
4. Migrate DB development SQLite mới từ source/backend bằng venv với `DJANGO_ENV=development DB_ENGINE=sqlite`. Chạy prepare_browser.py với F04_AUDIT_DIR để tạo HS/PH941–945 synthetic. Helper tạo mật khẩu ngẫu nhiên ở file mode600; không đưa file này hoặc synthetic.csv/DB/token vào evidence/ZIP.
5. Khởi động audit_server.py bằng venv, F04_AUDIT_DIR trỏ đúng root. Provider là fake có nhãn LOCAL_SYNTHETIC_PROVIDER. Không dùng để kiểm Gemini thật. Backend bind127.0.0.1:8044. Web Vite5144, Mini Vite3044, cả hai `VITE_API_BASE_URL=http://127.0.0.1:8044`; dùng strictPort để không trỏ nhầm server. Không chạy cùng cổng của người dùng.
6. Chạy lần lượt browser_e2e.mjs → browser_layout_and_control.mjs → cross_client_recipient.mjs → preview_race.mjs → ui_state_audit.mjs → reply_e2e.mjs → responsive_audit.mjs → cross_client_draft_conflict.mjs. Dùng DB mới khi rerun toàn bộ; thứ tự tạo connections/consent dùng bởi ca sau. Script browser mới sử dụng Playwright default `/opt/codex/cua_node/lib/node_modules/playwright/index.mjs` và Chromium `/usr/bin/chromium`; nếu máy khác, thay đường dẫn helper local, ghi thay đổi vào evidence. Helper cũ hỗ trợ F04_PLAYWRIGHT_MODULE/F04_CHROMIUM.
7. Probe Python claim-reuse và deletion/pause dùng Django test runner tự tạo/hủy DB test; kết quả tại ec29ab PASS. N03/N06 script browser hoàn tất exit0 để ghi evidence, nhưng verdict FAIL được biểu diễn bằng `wrongRecipientReceived:true` / `overwroteOtherClientWithoutConflict:true`. Exit0 của helper không có nghĩa feature PASS.
8. Kiểm JSON/assert expected so với actual, thu ảnh và báo SHA. Tắt đúng server bạn vừa tạo. Không snapshot credential, DB hoặc dump bearer headers.

Lệnh kiểm thử backend/frontend đầy đủ nằm trong commands-*.json; source-integrity.json xác minh 899 original files không bị thay đổi sau audit. CORS.json là OPTIONS thật từ hai origin local; không phải Render. Text200 trong responsive_audit là font-only CSS doubling, không phải device/native zoom.
