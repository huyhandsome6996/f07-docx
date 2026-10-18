# Kết quả kiểm tra mới

Tất cả kết quả dưới đây gắn với `bb75b2cee314bd5dfea3fff7928664dc68d3e2dd`, ngày 18/10/2026. Các lượt chạy không được cộng dồn thành một số tests duy nhất.

| Kiểm tra | Kết quả quan sát | Log / ghi chú |
| --- | --- | --- |
| Django check | PASS | Không issue |
| makemigrations --check --dry-run | PASS | Không drift |
| Migrate DB local sạch | PASS | `evidence/migrations.log` |
| Backend core/accounts sau cài MySQL driver | 46 tổng, 46 PASS, 0 skip | `backend-with-mysql-driver-tests.log`; deploy checks có W005/W021, không phải production acceptance |
| Full CI harness SQLite | 523 tổng, 512 PASS, 11 SKIPPED | `full-harness.log`; skips gồm MySQL-gated và middleware không mount trong harness |
| F07 harness SQLite theo script repo | 42 tổng, 40 PASS, 2 SKIPPED | `f07-sqlite-tests.log`; 2 MySQL race tests không chạy trong lượt này |
| F07 harness MySQL 8.4.11 | 42 tổng, 41 PASS, 1 FAIL, 0 skip | `f07-mysql-tests.log`; failure R04 do assertion thứ tự sai |
| Package mobile/core/shared JS | 98 PASS | `package-tests.log` |
| Mini App tests | 307 PASS | `miniapp-tests.log` |
| Web tests | 227 PASS | `web-tests.log` |
| Mini App build + asset/manifest check | PASS | `miniapp-build.log` |
| Web build | PASS | `web-build.log` |
| Import boundaries | PASS | `import-boundaries.log` |
| Agent documents | PASS | `agent-docs.log`; không chứng minh runtime/privacy |
| HTTP E2E có sẵn | 21/21 bước PASS | `http-e2e.log`; API thật, SQLite và tài khoản synthetic |
| Regression bổ sung trên SQLite | 3 tổng: 2 FAIL, 1 SKIPPED | `independent-sqlite-regressions.log`; R03/R05 fail, R02 cần MySQL |
| Regression bổ sung trên MySQL | 3 tổng: 3 FAIL | `independent-mysql-regressions.log`; R02/R03/R05 |
| Browser lifecycle + layout | 9 quan sát: 4 PASS, 5 FAIL | `browser-review.log` và `browser/browser-results.json`; 3 fail R01, 2 fail R06 |
| Zalo Android/iOS, OS text scaling, keyboard/safe-area | NOT_RUN | Không có runtime/quyền device |
| Production/Render, tài khoản thật, production backfill | NOT_RUN | Ngoài phạm vi; không deploy hoặc đụng dữ liệu thật |

## Lệnh suite chính

Tại checkout ứng dụng, dùng Python trong venv và dependency pin từ repo:

```bash
DJANGO_ENV=test DB_ENGINE=sqlite .venv/bin/python backend/manage.py check
DJANGO_ENV=test DB_ENGINE=sqlite .venv/bin/python backend/manage.py makemigrations --check --dry-run
DJANGO_ENV=test DB_ENGINE=sqlite .venv/bin/python backend/manage.py test core accounts --noinput
PATH="$PWD/.venv/bin:$PATH" bash tests/feature-lab/scripts/test_feature.sh f07_mood
node --test packages/family_bridge_mobile_core/tests/*.test.mjs packages/family_bridge_mobile/*/tests/*.test.mjs packages/family_bridge_shared/tests/*.test.mjs
node scripts/check_import_boundaries.mjs
python3 scripts/check_agent_docs.py
```

Chạy full harness theo danh sách feature/label trong `.github/workflows/tests.yml`. Từ `zalo-mini-app/` và `web/`, chạy `npm test` và `VITE_API_BASE_URL=http://127.0.0.1:8017 npm run build`.

MySQL chạy trong Docker local, image `mysql:8.4` digest ở PROVENANCE.json; service chỉ bind loopback. Driver `mysqlclient==2.2.8` được build với GCC và thư viện MariaDB client lấy qua metadata APT đã xác minh chữ ký. Server thật là MySQL 8.4.11; thư viện client MariaDB không biến server thành MariaDB. Không tắt TLS/checksum/signature verification. Credential local ngẫu nhiên được giữ ngoài repo và không đóng gói.

Hướng dẫn tái hiện bổ sung và biến MySQL: [repro/README.md](repro/README.md).

## Lệnh chẩn đoán sai ngữ cảnh đã được nhận diện

Đã thử gọi tests module F07 bằng `backend/manage.py test family_bridge_features.f07_mood`. Lệnh này trả **4 import errors**, vì tests module của repo cần `fixtures/labgrants` trong harness. Log giữ ở `evidence/f07-backend-tests.log` để minh bạch. Đây là lệnh chạy sai ngữ cảnh, không được ghi thành 4 lỗi sản phẩm hay 4 tests đã chạy nghiệp vụ. Sau đó đã chạy đúng harness trên SQLite/MySQL như bảng trên.

APT download ban đầu thiếu package lists; lần build driver đầu thiếu clang. Hai lỗi môi trường đã được khắc phục bằng metadata APT riêng trong workspace và `CC=gcc`; MySQL suite đã thực sự chạy. Chúng không còn là blocker.

## Giới hạn và phân tích tài nguyên

Kiểm tra này dùng 3 actor synthetic, 2 connections và tối đa 2 worker edit + 1 worker share trong regression mới. Không load/stress production. R03 tạo 2 grant, cùng page size 20; R05 gửi chuỗi ngày sai ngắn. Body/page/note bounds và grant revision/generation phải tiếp tục theo contract.

Không sửa algorithm/runtime ứng dụng trong đợt bàn giao này, nên phân tích độ phức tạp của một bản sửa là N/A. Với bộ kiểm tra, dữ liệu thử có giới hạn; browser và DB measurements chỉ có giá trị trong môi trường mô tả. Kết quả xanh của suite có sẵn không phủ định các regression đỏ mới.
