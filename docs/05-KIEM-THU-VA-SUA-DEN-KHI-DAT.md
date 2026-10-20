# Kiểm thử và sửa đến khi đạt

## Chu trình làm việc

Tái hiện lỗi → viết regression test đúng hành vi → sửa nguyên nhân → chạy targeted tests → kiểm thử tích hợp hai actor → build → deploy Testing → thử bản vừa deploy → sửa tiếp nếu phát hiện lỗi.

Không dừng ở kế hoạch, mock API hoặc “local đã chạy”. Không giới hạn một vòng sửa chỉ để tiết kiệm thời gian. Sau mỗi vòng lỗi ghi nguyên nhân và bằng chứng rồi tiếp tục cho đến khi các gate đã giao đạt.

Không chạy vòng lặp vô hạn với cùng một lệnh không tiến triển. Nếu thực sự thiếu token/quyền, key Gemini/quota, thiết bị, người thử nghiệm hoặc thao tác xác nhận từ chủ tài khoản:
- Hoàn thành tất cả công việc không phụ thuộc.
- Ghi BLOCKED/NOT_RUN chính xác, thu hẹp tới bước cần người dùng làm.
- Không giả PASS, không lách cổng xác thực/quyền hoặc downgrade bảo mật.
- Có thể deploy Testing sớm để kiểm trên thiết bị, nhưng bản bàn giao cuối phải chỉ rõ lỗi/gate còn lại.

## Các lớp kiểm tra tách riêng

1. Static/contracts: đúng direction, actor, DTO, errors, permissions, current generation, cleanup.
2. Regression UI web + Mini: sent không composer, received vẫn composer, AI apply không send, unknown-outcome/key/state.
3. Backend service/API: own/recipient/third actor/admin, wrong recipient reply, unlink/revoke, double-send, idempotency.
4. Production wiring local/cô lập: session HS/PH thật qua auth runtime, không chỉ test doubles.
5. MySQL/TiDB: constraint/concurrency/migration phù hợp phần đổi; SQLite không chứng minh DB mục tiêu.
6. Build: đúng Mini manifest/chunks/assets/base URL, không lẫn web artifact.
7. Provider thật: status/refine/accept, lỗi quota/timeout, input revision; không dùng mock Gemini làm kết quả thật.
8. Deployed Render + Zalo Testing: đúng SHA/version, API thật, QR/deep link, HS/PH hai phiên.
9. Thiết bị: Android/iOS, safe area, bàn phím/back/resume, text lớn/offline. Thiết bị thiếu ghi rõ; không suy từ simulator.
10. Audience access: tester ngoài chủ app mở QR; ghi đúng phạm vi ai dùng được.

## Bộ ca phải có

Thực hiện T01–T22 trong docs/01, AI01–AI10 trong docs/02 và route matrix F01–F15 trong docs/03. Thêm:
- Không người nhận/không kết nối; hết phiên; consent bị rút.
- F11 gửi và người nhận đọc được, role hết hạn bị chặn.
- F12 người khác trường hoặc không assigned không được đọc/nhận hẹn.
- F13 danh bạ thật đã duyệt và fallback hợp lệ.
- F14 tự nguyện, không bị bắt khảo sát để gửi thư; admin không raw survey.
- F15 revoke/unlink làm mất quyền ở mọi đường đọc, không lưu private body trong cache công khai.
- Nháp/AI/300s/resume không tự gửi.
- Router/back/tabbar đưa tới mọi luồng HS/PH, không trang chết hoặc placeholder che thiếu tính năng.
- Direct URL mở sau login đúng trang được phép, không loop login/role-select/proposal.

## Lệnh tham khảo (phải đối chiếu repo hiện hành)

```bash
git diff --check
python scripts/check_agent_docs.py
bash tests/feature-lab/scripts/test_feature.sh f05_inbox
bash tests/feature-lab/scripts/test_feature.sh f04_ai
bash tests/feature-lab/scripts/test_feature.sh f10_signal
npm --prefix web test
npm --prefix web run build
npm --prefix zalo-mini-app test
npm --prefix zalo-mini-app run build
```

Đây là yêu cầu cho agent, không phải kết quả đã chạy khi đóng gói. Dùng dependencies/lockfile và phiên bản runtime của checkout hiện tại; chạy thêm shared và backend integration suites theo phần ảnh hưởng.

Mỗi kết quả ghi command, code SHA, actor synthetic, environment, expected/actual, output sạch, PASS/FAIL/NOT_RUN/BLOCKED. Không copy tổng test PASS cũ của repo thành kết quả mới.

## Gate bàn giao cuối

- Không còn finding chưa xử lý trong scope mà agent có thể tự sửa.
- Không có regression gửi/nhận/AI/quyền.
- API/backend/client contracts đồng nhất; hai UI tree giữ đúng.
- Build và test liên quan qua; bản deploy Testing đúng commit đã kiểm.
- QR/deep link/version thật được bàn giao, có kiểm audience access.
- Các phần chưa kiểm được do phụ thuộc bên ngoài nêu cụ thể; không gọi “toàn diện hoàn tất” khi còn gap quan trọng.
