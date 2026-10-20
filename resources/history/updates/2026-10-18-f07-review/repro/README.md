# Chạy bộ tái hiện

Chỉ dùng checkout ứng dụng và DB test/local synthetic. Không copy `branch-snapshot` lên ứng dụng, không chạy với DB production. Ghi SHA thực tế trước khi chạy; kết quả cũ không tự áp dụng khi nhánh đã tiến.

## Regression Django mới

Dùng Python venv của ứng dụng (đã cài requirements pin), còn tests ở kho tài liệu. Thay đường dẫn bên dưới theo máy:

```bash
APP_DIR=/workspace/family-bridge-f07-review
REVIEW_DIR=/workspace/f07-docx/updates/2026-10-18-f07-review
"$APP_DIR/.venv/bin/python" "$REVIEW_DIR/repro/run_review.py" --repo "$APP_DIR" --database sqlite
```

Trên baseline bb75b2c: R03/R05 FAIL, R02 SKIPPED. Runner dùng test-only harness, test database do Django tạo và hủy, không dùng DB ứng dụng đang phục vụ browser.

Với MySQL local disposable đã tạo và driver `mysqlclient` đã cài, cung cấp các binding `FB_MYSQL_DB`, `FB_MYSQL_USER`, `FB_MYSQL_PASSWORD`, `FB_MYSQL_HOST`, `FB_MYSQL_PORT` qua môi trường an toàn; không in giá trị. User cần quyền tạo/drop database test tương ứng. Chạy:

```bash
"$APP_DIR/.venv/bin/python" "$REVIEW_DIR/repro/run_review.py" --repo "$APP_DIR" --database mysql
```

Trên bb75b2c: cả 3 FAIL. Một test điều phối 2 worker edit và 1 share bằng các event có timeout; DB, reader và service đều thật. Cách sửa dùng row lock hoặc stale rejection hợp lệ có thể cần tinh chỉnh assertion theo contract đã chốt; không bỏ invariant **nội dung chưa duyệt không đọc được** và không đổi test thành xfail/skip để báo PASS.

Để chạy module MySQL có sẵn, dùng cùng biến `FB_TEST_DB=mysql`/`FB_MYSQL_*` tại `tests/feature-lab`, chọn đủ feature như CI rồi chạy `manage.py test family_bridge_features.f07_mood --noinput -v 2`. Không gọi module tests này từ `backend/manage.py` vì thiếu harness fixtures.

## Browser lifecycle và text scaling

Chuẩn bị DB SQLite riêng, migrate và tạo fixture bằng script local của ứng dụng; script fixture có reset dữ liệu của chính các tài khoản e2e synthetic. Không chạy nó trên DB thật. Sau đó chạy backend và Mini App với cùng API base, chẳng hạn backend loopback 8017 và Mini App loopback 3017; thêm origin client vào CORS_ALLOWED_ORIGINS của backend.

Để có mục lịch sử cho browser: chạy `scripts/f07_local_e2e.py --base http://127.0.0.1:8017` từ repo ứng dụng. Trên baseline hiện tại, luồng này đạt 21 bước; để lại mục synthetic phục vụ kiểm tra browser. Không đưa API base production vào lệnh.

Cài Playwright ngoài checkout ứng dụng để giữ lockfile nguyên vẹn, ví dụ:

```bash
npm install --prefix /tmp/f07-review-browser --ignore-scripts --no-audit --no-fund playwright
PLAYWRIGHT_MODULE=/tmp/f07-review-browser/node_modules/playwright/index.mjs \
CHROMIUM_PATH=/usr/bin/chromium \
F07_UI_BASE=http://127.0.0.1:3017 \
F07_REVIEW_OUTPUT=/tmp/f07-browser-results \
node "$REVIEW_DIR/repro/browser_review.mjs"
```

Script mặc định dùng tài khoản fixture HSZE2E01 và mật khẩu synthetic có sẵn trong `scripts/f07_local_fixtures.py`, không phải tài khoản/mật khẩu thật. Có thể override bằng `F07_SYNTHETIC_PASSWORD` qua môi trường; không log giá trị.

Trên bb75b2c: 9 quan sát, 5 FAIL và 4 PASS. Ba FAIL chứng minh sheet/private preview không được gỡ khi navigation/clearSession; hai FAIL còn lại là tràn ngang ở 320/390 sau CSS text scaling 200%. Script ghi kết quả JSON và screenshot; exit 1 khi còn lỗi. Text scaling này là mô phỏng browser, không phải bằng chứng Zalo/OS accessibility.

Không thay thế regression test tích hợp vào ứng dụng bằng script ngoài repo. Agent phải bổ sung tests phù hợp code cuối cùng, gồm logout qua nút thật, actor switch, late response, sheet cleanup, nhiều owner và MySQL concurrency.
