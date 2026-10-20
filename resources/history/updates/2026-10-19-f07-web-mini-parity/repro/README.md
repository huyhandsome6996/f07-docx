# Chạy smoke web/Mini App và tái hiện finding

Chỉ dùng local development và dữ liệu synthetic. Đọc scope/provenance trước; tests đỏ là finding, không đánh expected-failure để báo đã nghiệm thu. Cài requirements/locked npm dependencies của checkout ứng dụng; dùng công cụ browser ngoài checkout để giữ lockfiles nguyên vẹn.

## Local setup hai client cùng API

Ví dụ đường dẫn, thay theo máy:

```bash
APP_DIR=/workspace/family-bridge-f07-review
DOC_DIR=/workspace/f07-docx
REVIEW_DIR="$DOC_DIR/updates/2026-10-19-f07-web-mini-parity"
```

Migrate SQLite local theo README repo. Tạo fixture parity riêng (script từ chối ngoài development/SQLite, không reset account khác hoặc hồi sinh fixture connection đã revoke):

```bash
DJANGO_ENV=development DB_ENGINE=sqlite "$APP_DIR/.venv/bin/python" "$REVIEW_DIR/repro/seed_parity.py" "$APP_DIR"
```

Script tạo HS HSPAR19 và PH PHPAR19 synthetic, connection active invite NULL và một mục private hôm nay để smoke đọc. Mật khẩu test-only mặc định cùng fixture E2E của repo; không phải credential thật và không in ra khi seed. Không chạy trên participant DB.

Ba terminal riêng, từ working directory được nêu:

```bash
# Gốc ứng dụng
DJANGO_ENV=development DB_ENGINE=sqlite CORS_ALLOWED_ORIGINS=http://127.0.0.1:3019,http://127.0.0.1:5179 .venv/bin/python backend/manage.py runserver 127.0.0.1:8019 --noreload

# APP_DIR/zalo-mini-app
VITE_API_BASE_URL=http://127.0.0.1:8019 npm run start -- --port 3019 --strictPort

# APP_DIR/web
VITE_API_BASE_URL=http://127.0.0.1:8019 npm run dev -- --host 127.0.0.1 --port 5179 --strictPort
```

Các địa chỉ loopback chỉ để validation nội bộ. Đây không phải URL giao cho Huy từ máy khác hoặc bản đã deploy.

## Parity smoke

Với Playwright cài ngoài app và Chromium sẵn có:

```bash
npm install --prefix /tmp/f07-review-browser --ignore-scripts --no-audit --no-fund playwright
PLAYWRIGHT_MODULE=/tmp/f07-review-browser/node_modules/playwright/index.mjs \
CHROMIUM_PATH=/usr/bin/chromium \
F07_API_BASE=http://127.0.0.1:8019 \
F07_MINI_BASE=http://127.0.0.1:3019 \
F07_WEB_BASE=http://127.0.0.1:5179 \
F07_PARITY_OUTPUT=/tmp/f07-parity-results \
node "$REVIEW_DIR/repro/client_parity.mjs"
```

Runner mặc định dùng HSPAR19; F07_PARITY_CODE/F07_SYNTHETIC_PASSWORD có thể override bằng fixture local thích hợp, không log giá trị. Trên bb75b2c: 12 quan sát, 9 PASS + 3 FAIL, exit 1. Auth và list/detail adapter thật đạt; 3 FAIL là web routes/navigation. Quick card legacy chỉ là diagnostic transport; runner không bắt buộc giữ quick card nếu agent thay bằng entry point F07 đúng. Navigation có thể là button hoặc link với nhãn tiếng Việt phù hợp; nếu UI hợp lệ dùng nhãn/route khác cần cập nhật mapping/test có giải thích, không bỏ coverage.

Runner này không thay thế E2E UI đầy đủ X01–X10; các adapter calls trực tiếp được ghi riêng là chẩn đoán. Agent bổ sung tests cho các thao tác thực tế trên web/Mini App sau khi triển khai.

## R01–R06

Dùng các runner trong `updates/2026-10-18-f07-review/repro/`; xem README tại đó. Regression MySQL cần instance disposable loopback, driver và FB_MYSQL_* bindings an toàn; không in hoặc đóng gói mật khẩu. Test runner tạo/hủy test DB, không dùng browser DB.

Mini browser lifecycle runner cũ dùng HSZE2E01 và cần mục có note synthetic để mở preview. Chuẩn bị fixture/E2E riêng theo repo, không lấy participant account. Nếu fixture không đủ, ghi lỗi setup và khắc phục trước khi kết luận test sản phẩm.
