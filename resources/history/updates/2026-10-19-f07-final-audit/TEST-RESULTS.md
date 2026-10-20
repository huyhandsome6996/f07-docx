# Kết quả kiểm thử độc lập — 19/10/2026

Source thực chạy: **2ffd674243c5063f95123010498bc9cc60cf441e**, cùng remote F07 và PR42 lúc kiểm tra. Fast-forward từ bb75b2c; không sửa file tracked ứng dụng. Môi trường: Python3.12.14, Django5.2.18, Node24.19.0/npm11.9.0; Chromium154; backend production mount với development SQLite local, hai Vite client; MySQL8.4.11/InnoDB thật qua Docker loopback. Không chạy trên production hoặc participant data.

**Kết luận: NOT_READY_FOR_HUY.** Suites hiện hữu xanh nhưng tám scenario UI bổ sung FAIL, tương ứng ba finding R08–R10 trên hai client. Không cộng các suite overlap thành tổng độ phủ.

## Runner đã hoàn tất

| Phép kiểm | Kết quả thực tế | Exit | Bằng chứng trong evidence/ |
| --- | --- | ---: | --- |
| Backend check + makemigrations check + core/accounts | check OK, không migration mới; 46 PASS | 0 | backend.log |
| F07 feature-lab SQLite | 53 tổng = **49 PASS + 4 SKIP**, 0 FAIL | 0 | f07-sqlite.log |
| F07 MySQL8.4.11 | **53 PASS, 0 SKIP**, gồm create/share/2 edit race (4 test) | 0 | f07-mysql.log |
| Repro độc lập R02/R03/R05 SQLite | 3 tổng =2 PASS +1 SKIP (R02 cần MySQL) | 0 | independent-sqlite.log |
| Repro độc lập MySQL | **3 PASS**; revision3, unapproved_readable=false; list2/2; date suffix400 | 0 | independent-mysql.log |
| Full harness (harness, labgrants, 17 feature labels) SQLite | 534 tổng = **521 PASS +13 SKIP**, 0 FAIL | 0 | full-harness.log |
| Mini suite + build/manifest verify | **313 PASS**, build và assets verify OK | 0 | mini.log |
| Web suite + build | **243 PASS**, build OK | 0 | web.log |
| Shared headless adapter | **37 PASS** | 0 | boundaries.log |
| Mobile core + mobile modules | **61 PASS** | 0 | mobile-packages.log |
| Import boundaries + agent-doc checker | OK, không cross-UI/SDK web | 0 | boundaries.log |
| HTTP E2E API thật | **21/21 PASS**, gồm F15 và unlink | 0 | http-e2e.log |
| Browser R01/R06 Mini | **9/9 PASS** | 0 | browser-mini.log + browser-mini/ |
| Browser R01/R06 Web | **9/9 PASS** | 0 | browser-web.log + browser-web/ |
| Parity smoke login/adapter/route/navigation | **10/10 assertion PASS**; không phải full UI E2E | 0 | parity.log + parity/results.json |
| Cross-client UI E2E của ứng dụng | **19 assertion thực chạy PASS + 1 X07 NOT_RUN** (runner lưu cả20 dòng pass=true) | 0 | cross-client.log + cross-client/results.json |
| Home web duplicate → link sửa, pair active + HS chưa kết nối | **2/2 PASS**, POST400 đúng, link tới mood thật | 0 | home.log + home/ |
| R08 same editor, create/edit rồi lưu tiếp | **4 scenario FAIL** trên web/Mini | 1 | repeat-save-complete.log + repeat-save-complete/ |
| R09 hết trang vẫn click/append first page | **2 scenario FAIL**, rows1→3 | 1 | pagination.log + pagination/ |
| R10 preview cũ ở client kia | **2 scenario UI FAIL**; riêng backend409 bảo vệ đúng ở cả2 | 1 | stale-preview.log + stale-preview/ |
| Health/ready/auth guard/CORS hai origin | **5/5 PASS** | 0 | service-readiness.json |

## Diễn giải việc đóng finding cũ

| Finding | Bằng chứng mới | Phạm vi kết luận |
| --- | --- | --- |
| R01 overlays/private DOM | Chromium9/9 mỗi client: navigation gỡ sheet, session clear không còn preview; cross-client logout qua nút thật | Lỗi overlay cũ không còn tái hiện; chưa phủ mọi late response/actor/device |
| R02 revision race | Independent MySQL: final_revision=3, unapproved_readable=false; 4 race trong suite MySQL đều OK | Lịch interleaving đã thử an toàn, không tuyên bố mọi lịch đồng thời được chứng minh |
| R03 nhiều owner một recipient | Independent list2/2 và tests mới của ứng dụng | Không còn tái hiện mất owner thứ2 |
| R04 assertion race/count | F07 MySQL53/53, không skip | Assertion create/share đã qua; lỗi cộng NOT_RUN trong báo cáo UI là việc riêng cần chỉnh |
| R05 ngày bị cắt suffix | API thật trong harness trả400, regression full-string qua | Không còn tái hiện nhập chuỗi rác thành ngày hợp lệ |
| R06 chữ lớn tràn ngang | Cả hai client320/390/430, thường và CSS font/line-height200%: contentWidth bằng viewport | Chỉ Chromium/CSS simulation; không phải native scaling/device |
| R07 thiếu F07 web | Route/navigation, real API adapter; UI chéo tạo/sửa/share/read/revoke dùng cùng backend | Đã có chức năng web thực; không đồng nghĩa toàn UI đạt vì R08–R10 còn mở |

## Giới hạn và sai số của công cụ cũ

- Cross-client output “20 PASS” có một X07 NOT_RUN. Không lấy dòng đó làm bằng chứng UI unlink/reconnect. Backend/HTTP bảo vệ generation/F15 đã chạy ở tầng khác. Nhánh X07 optional và các assertion X08 cần chỉnh theo FINDINGS.
- Parity helper gói11 có diagnostic quick-card optional chạy trước khi home render xong: log INFO nói “no legacy quick-mood card” **không chứng minh card bị xoá**. Screenshot thực tế có card. Vì vậy đã kiểm riêng home: hai ca400 + link sửa đều PASS; smoke này có10 assertion, không lấy con số12 từ báo cáo agent.
- Một lần browser R01 đầu tiên không có mood do fixture vừa reset; đã tạo dữ liệu qua HTTP E2E21 rồi chạy lại, 9/9 mỗi client. Đây là fixture prerequisite, không ghi thành lỗi sản phẩm. Một bản helper stale ban đầu chờ option visible (option native không visible độc lập); đã đổi chờ attached, chạy lại bằng UI thật. FAIL R10 cuối cùng dựa trên409 + lỗi ngoài dialog, không dựa timeout selector.
- Tests `f07-r06-reflow.test.mjs` dùng happy-dom không có layout thực; kiểm `scrollWidth` ở đó không tự chứng minh reflow. Bằng chứng layout lấy Chromium trong browser-mini/web.
- MySQL harness có4 warning model conditional unique của F01/F09/F11 liên quan; không che warning, không suy cả schema MySQL production được chứng nhận. Core/accounts suite có warning readiness/deploy trong ca test âm tính; runner46/46 OK. Đây không phải deployment check production đầy đủ.
- **NOT_RUN:** Zalo Android/iOS, native keyboard/safe area/OS text scaling/TalkBack/VoiceOver, UI reconnect đầy đủ X07 và mọi late response/actor permutation. Không có user-accessible URL của đúng bảnF07 được xác minh; **BLOCKED** cho bước bàn giao Huy từ máy riêng. Không deploy trong phạm vi này.
- Source snapshot25 file là tham chiếu, không dependency cài đặt. Log/ảnh chỉ chứa synthetic; không có token, secret/DB/participant data.

## Lệnh đã dùng (từ checkout đúng SHA)

Từ application root, dùng `.venv/bin` trong PATH cho helper:

```bash
PATH="$PWD/.venv/bin:$PATH" bash tests/feature-lab/scripts/test_feature.sh f07_mood
DJANGO_ENV=test DB_ENGINE=sqlite .venv/bin/python backend/manage.py check
DJANGO_ENV=test DB_ENGINE=sqlite .venv/bin/python backend/manage.py makemigrations --check --dry-run
DJANGO_ENV=test DB_ENGINE=sqlite .venv/bin/python backend/manage.py test core accounts --noinput
node scripts/check_import_boundaries.mjs
.venv/bin/python scripts/check_agent_docs.py
node --test packages/family_bridge_shared/tests/*.mjs
node --test packages/family_bridge_mobile_core/tests/*.test.mjs packages/family_bridge_mobile/*/tests/*.test.mjs
python3 scripts/f07_local_e2e.py --base http://127.0.0.1:8019
```

Web/Mini từng thư mục: `npm test`, rồi `VITE_API_BASE_URL=http://127.0.0.1:8019 npm run build`. F07 MySQL dùng harness.settings +FB_TEST_DB=mysql +FB_MYSQL_* local, không lưu giá trị secret; test label `family_bridge_features.f07_mood`. Full harness dùng toàn FB_FEATURES/labels theo startup AGENTS của repo, log ghi534 đã chạy. Independent repro dùng `run_review.py --repo APP_DIR --database sqlite|mysql` trong gói10; MySQL qua cùng local bindings. Browser gói10 dùng F07_UI_BASE3019/5179, gói11 parity dùng hai origin/API8019. Runner mới và scope/reset hướng dẫn trong [repro/README.md](repro/README.md). Không gọi adapter qua console thay bằng chứng UI E2E; parity smoke có diagnostic adapter riêng được đánh dấu.
