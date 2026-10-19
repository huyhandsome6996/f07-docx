# Repro UI R08–R10

Đọc mã trước khi chạy. Chỉ development SQLite/local loopback, tài khoản synthetic. Không thay tests ứng dụng hay dependency/lockfile để dùng các helper này. Cần backend/API thật và Vite Mini + web từ cùng SHA, API base/CORS trỏ cùng backend. Playwright/Chromium đã cài trong môi trường reviewer; dùng đường dẫn dependency hợp lệ của môi trường bạn qua biến dưới, không giả định đường dẫn reviewer tồn tại ở máy khác.

## Chuẩn bị

Chạy migrations development theo repo. Fixture `scripts/f07_local_fixtures.py` tạo HSZE2E01/PHZE2E01/HSZE2E99; chỉ dùng trên DB local disposable. Nó RESET mood của các fixture đó; đọc guards trước khi chạy. Seed parity từ gói11 tạo HSPAR19/PHPAR19, không hồi sinh pair đã revoke.

Khởi động API `8019`, Mini `3019`, web `5179` (hoặc override biến); không coi các loopback này là URL Huy truy cập được. Ví dụ từ application root, dùng venv của bạn:

```bash
DJANGO_ENV=development DB_ENGINE=sqlite CORS_ALLOWED_ORIGINS=http://127.0.0.1:3019,http://127.0.0.1:5179 .venv/bin/python backend/manage.py runserver 127.0.0.1:8019 --noreload
# từ zalo-mini-app/: VITE_API_BASE_URL=http://127.0.0.1:8019 npm run start -- --port 3019 --strictPort
# từ web/: VITE_API_BASE_URL=http://127.0.0.1:8019 npm run dev -- --host 127.0.0.1 --port 5179 --strictPort
```

Các lệnh sau dùng đường dẫn placeholder đã thay bằng đường dẫn thật; `DOCS_DIR` là checkout tài liệu, `APP_DIR` là ứng dụng. Mật khẩu là fixture công khai local trong mã seed, không phải credential thật; không dùng tài khoản này ngoài local.

```bash
export DOCS_DIR=/path/to/f07-docx
export APP_DIR=/path/to/family-bridge
export REPRO_DIR="$DOCS_DIR/updates/2026-10-19-f07-final-audit/repro"
export PLAYWRIGHT_MODULE=/path/to/playwright/index.mjs
export CHROMIUM_PATH=/usr/bin/chromium
export F07_MINI_BASE=http://127.0.0.1:3019
export F07_WEB_BASE=http://127.0.0.1:5179
export PYTHONDONTWRITEBYTECODE=1
```

## R08: bốn chuỗi lưu liên tiếp

`seed_repeat.py` chỉ reset mood của hai actor HSR08M19/HSR08W19 có external_ref marker riêng, từ chối collision/connection bất thường/non-development/nonSQLite. Nó không thay fixtures parity hoặc người dùng khác. Không chạy seed trong lúc browser tests dùng cùng actor.

```bash
DJANGO_ENV=development DB_ENGINE=sqlite "$APP_DIR/.venv/bin/python" "$REPRO_DIR/seed_repeat.py" "$APP_DIR"
F07_REPEAT_OUTPUT=/tmp/f07-repeat-save node "$REPRO_DIR/repeat_save.mjs"
```

Trên baseline: exit1; mỗi client POST201→POST400 và PATCH200→POST400. Sau sửa cả 4 scenario pass, lần thứ hai PATCH2xx. Đối chiếu thêm entry ID/revision qua tests ứng dụng và UI history. Không chạy lại seed trước R09 vì nó xoá mood cần dùng bên dưới.

## R09: trang cuối không còn nhận click

Sau R08, hai actor mỗi người có một mục; không tự tạo duplicate DB.

```bash
F07_PAGINATION_OUTPUT=/tmp/f07-pagination node "$REPRO_DIR/pagination.mjs"
```

Baseline exit1; hiddenAttribute=true/display=flex/visible=true, hai request trang đầu, rows1→3 trên cả client. Sau sửa exit0, nút thực sự không hiển thị, rows không đổi. Helper này chỉ chứng minh one-page; tests mới của agent phải thêm nhiều trang/recipient/error/race.

## R10: xác nhận preview cũ ở client kia

Seed parity từ gói11, giữ pair HSPAR19/PHPAR19 active. Script sửa note synthetic hiện hành, tạo revision; không gửi share tự động ngoài hai lần bấm confirm preview đã cũ để xác minh API từ chối. Chạy tuần tự sau các test khác dùng cùng pair.

```bash
DJANGO_ENV=development DB_ENGINE=sqlite "$APP_DIR/.venv/bin/python" "$DOCS_DIR/updates/2026-10-19-f07-web-mini-parity/repro/seed_parity.py" "$APP_DIR"
F07_STALE_OUTPUT=/tmp/f07-stale-preview node "$REPRO_DIR/stale_preview.mjs"
```

Baseline exit1 do lỗi không có trong modal; `backendProtectionPass=true` vì HTTP409 đúng, `feedbackOutsideDialog=true`. Sau sửa lỗi stale cần có trong dialog; update helper nếu copy được phê duyệt thay đổi, giữ invariant nội dung rõ ràng +409/no-auto-share, không bỏ assertion. Ghi code/test diff nếu điều chỉnh selector, tránh nhận lỗi harness là lỗi sản phẩm.

Các helper xuất screenshot/JSON và exit1 khi assertion fail hoặc lỗi uncaught; không chứa token/request body/credential thật. Chạy lại HTTP21 cần reset fixtures phù hợp; nó kết thúc bằng unlink pair HSZE2E01, không dùng cùng pair để test share tiếp khi chưa tạo fixture mới đúng quy trình.

`home.mjs` là diagnostic bổ sung chạy web loopback5179, API8019, Chromium hệ thống, HSPAR19/HSR08W19 đã có mood hôm nay. Nó đợi chip thật render trước khi bấm, kiểm400 duplicate + link sửa và chỉ ghi metadata/screenshot synthetic. Override PLAYWRIGHT_MODULE/F07_HOME_OUTPUT; nếu khác port/browser thì đọc/chỉnh cấu hình diagnostic trước, không trỏ production. Nó không thay regression R08 trên editor.
