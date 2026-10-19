# Test results — F02 c29469b, 19/10/2026 UTC+7

## Nguồn và môi trường

- Full app SHA `c29469b3d57f2c2cc53fe686fe7ec8f917f2dec6`, detached worktree `work/qa-f02-c29469b-20261019`.
- Windows, Python3.12 (test-venv đã có), Django5.2.18, DRF3.17.2; Node24.19.0, Vite8.3.4, happy-dom20.14.6.
- Dependency đúng lockfile đã có, dùng junction node_modules từ checkout local. Không nâng dependency, không commit node_modules.
- Backend runtime dùng `backend/config/settings.py`, toàn bộ startup providers/session resolvers production, API HTTP loopback8004, SQLite **mới riêng checkout**.
- Frontend Mini App Vite3004; browser thật, khôngdemo1, tài khoản synthetic HS903. Web suite/build được chạy riêng.
- Không realsecret, không database Render/TiDB, không thao tác100tài khoản thật. Adminfixture không tạo consent thay user; consent dịch vụ test do từngactor gửi khi cần.

## Kết quả lệnh

| Kiểm tra | Actual | Exit / bằng chứng |
| --- | --- | --- |
| Backend harness F02+F16admin+F09 | 68tests OK,0fail | exit0, [backend.log](evidence/backend.log) |
| Mini App fullsuite | 318pass,0fail | exit0, [miniapp.log](evidence/miniapp.log) |
| Shared+F02mobile | 38pass,0fail | exit0, [shared-mobile.log](evidence/shared-mobile.log) |
| Web fullsuite | 231pass,0fail | exit0, [web.log](evidence/web.log) |
| MiniApp build+verify | Built; allassets referenced | exit0, [miniapp-build.log](evidence/miniapp-build.log) |
| Web build | Built | exit0, [web-build.log](evidence/web-build.log) |
| Import boundary | CLEAN | exit0, [boundaries.log](evidence/boundaries.log) |
| Backend check |0issues | exit0; CLI direct observed |
| makemigrations --check --dry-run |No changes detected | exit0; CLI direct observed |
| migrate fresh fixture / showmigrations |0001,0002 applied; startup successful | fixture runner; NOT a MySQL upgrade test |
| Independent HTTP |44PASS,2FAIL /46 assertions | [http-results.json](evidence/http-results.json), [http.log](evidence/http.log) |
| Follow-up UI/version probe |3FAIL /3 assertions | [version-results.json](evidence/version-results.json);2assertions describe same R02 |
| Independent DOM regressions |0PASS,3FAIL | expectedRED on source; exit1, [log](evidence/independent-dom-regressions.log) |
| Agentdocs rawWindows |Taste checksum mismatches SKILL/LICENSE | exit1, lineending explanation below |

Hai lần gọi CLI QA đầu có lỗi đường dẫn/dependency: chạy Node trước khi junction đúng nên thiếuhappy-dom, gọi rootchecker từcwdMiniApp nên thiếufile. Đã sửa môi trường/cwd và chạy lại. Các kết quả pass ở bảng là lượt chạy lại thành công, không lấy lần lỗi môi trường làm finding sản phẩm.

### Agentdocs và CRLF

Windows `core.autocrlf=true` đổi bytes. Cả SKILL.md và LICENSE: rawhash khôngkhớpmanifest, nhưng hash khi normalizeCRLF→LF **và gitblob HEAD** đều khớp. Diff main...F02 không thay tastefiles.

Đây là giới hạn checker theo bytes trên checkoutWindows, không bằng chứng F02 sửa skill sai. Không sửa hash/skill để épPASS. Lượt này không chạy lại checker trên một checkoutLF hoàn chỉnh; ghi NOT_RUN cho lượt đó, không che exit1.

## Commands chính (tái tạo trong môi trường phù hợp)

Đọc CI mới nhất và runner trước chạy. Từ rootapp:

```bash
node --test packages/family_bridge_shared/tests/*.test.mjs packages/family_bridge_mobile/f02_program/tests/*.test.mjs
node scripts/check_import_boundaries.mjs
python scripts/check_agent_docs.py
```

Harness cwd `tests/feature-lab`, `DJANGO_ENV=test`, `DJANGO_SETTINGS_MODULE=harness.settings`, featurelabels đủ theoCI:

```text
f01_identity,f15_privacy,f05_inbox,f03_cards,f04_ai,f06_drafts,f07_mood,f08_journal,f10_signal,f11_supporters,f13_help,f12_appointments,f09_activities,f02_program,f14_surveys,admin_core,f16_classroom
```

```bash
python manage.py test family_bridge_features.f02_program family_bridge_features.f16_classroom.tests.test_admin_provision family_bridge_features.f09_activities -v 1
```

Trong từng frontend chạy tests theo package.json và build; MiniApp có verify-build.mjs.

Runner độc lập ở `f02/tools/` trong repo tài liệu:

1. Tạo **checkoutapp mới, khôngdb.sqlite3/.env backend**. Đặt F02_QA_PASSWORD giả dài>=12.
2. `python f02/tools/local_fixture.py --app-root <fresh-app-checkout>`.
3. Run backend8004 với DJANGO_ENV=development,DB_ENGINE=sqlite,FB_ZALO_LOGIN_ENABLED=false, CORS3004.
4. `python f02/tools/http_qa.py --out <new-evidence/http-results.json>`.
5. Run frontend3004 VITE_API_BASE_URL=loopback8004, loginHS903; enroll1, mời activitytuần1 bằngUI.
6. `python f02/tools/version_probe.py --app-root <same-app> --out <new-evidence/version-results.json>`.
7. `F02_APP_ROOT=<app> node --test f02/tools/miniapp_repro.test.mjs` (PowerShell dùng cú pháp env tương ứng).

HTTP và version runners là probe tạo dữliệu, chạy một lần theo fixture/state đã mô tả. Runner lúc phát hiện đã in FAIL và JSON rõ nhưng exit0 vì khôngthrow; **không dùng exit0 để kết luận assertionpass**. DOMregressions cóexit1 đúng khiFAIL.

## UI bằng chứng

- Browser login/consent/home xác nhận HS903 thấy PH903 active, không ghépđôi lại.
- Trước enroll chỉtitles+nútThamgia, không guidepreview.
- Enroll qua dialog, xem đủ4tuần; guideHS, nhãnrev1, paperalternative.
- Mời tuần1 qua UI; DB đọc lại content_revision1 dù source publishedrev2.
- Tôiđãlàm → serverrefetch → Đãlàm/Đặtlại; đềxuất → Chờhaibênxácnhận, không tựký.
- Width390 cóclientWidth=scrollWidth=390, khôngtrànngang trong trạng thái đãchụp. Chưa kiểm mọi viewport/keyboard/screenreader.
- Lời mời hai phía, signature haiactor, quyềnstranger, optout/rejoin vàunlink được kiểm quaHTTP; không gọi đó là tấtcả thao tác2actor đã thử quaUI/Zalo thật.

## NOT_RUN / chưa chứng minh

- MySQL/TiDB migrations nângcấp/cạnhtranh/locks; không có environment testđượcxác nhận trong lượt này.
- ZaloAndroid/iOS thật, deployTesting; SDK không được kiểm bởi browserlocal.
- ProductionRender đang chạySHA/nội dungphiênbản nào; backfill100accounts.
- Phêduyệtchuyênmôn nộidung; syntheticpublish chỉfixture.
- End-to-end UIweb F02; sourceđọc thấyplaceholder, tests/build không thay thế.
- Toàn bộ51caseởprompt18/10 không chạy hết; chỉcase cóevidence mới gắnPASS/FAIL. Không chuyển phầnbỏtrống thànhPASS.
