# Ma trận nghiệm thu ứng dụng tích hợp

Mỗi dòng phải có source SHA, actor, client, backend/DB, expected/actual, evidence, PASS/FAIL/SKIP/NOT_RUN/BLOCKED. Bản này là tiêu chí, không là test đã chạy trong nhiệm vụ đóng gói.

## Ma trận chức năng và riêng tư

| ID | Kịch bản bắt buộc | Kết quả cần đạt |
| --- | --- | --- |
| A01 | HS/PH cấp sẵn + cặp admin ACTIVE, login trên cả hai client | Đúng role/UUID/counterpart; không mã mời/proposal; consent riêng |
| A02 | Đổi mã/tên/mật khẩu theo luồng hiện có | UUID, cặp và dữ liệu giữ nguyên; không suy role từ tiền tố |
| A03 | Logout, session expired, disabled user, request trả muộn | Không ghi/render dữ liệu actor cũ; help vẫn truy cập |
| P01 | F02 preview chưa enroll và đọc đủ bốn tuần | Chủ đề/hoạt động đúng published revision, không khóa tuần sau |
| P02 | Hai actor cập nhật progress và skip | Tiến độ riêng, revision pin, tự nguyện; opt-out không auto-resurrect |
| P03 | Thỏa ước propose + HS ký + PH ký cùng revision | Propose không là ký, đủ hai chữ ký mới confirmed; backup không đọc/ký |
| P04 | F09 invite/respond và unlink/reconnect | Đúng người tự đồng ý, generation mới không mở hoạt động cũ sai quyền |
| AI01 | Không đồng ý AI, AI off/provider lỗi/quota | Không gọi provider; giữ nháp; viết tay/help vẫn dùng |
| AI02 | Bấm AI hai lần/retry/timeout, đổi actor | Claim/idempotency đúng, không charge/call trùng hoặc áp gợi ý cũ |
| AI03 | Edit/đổi recipient trong khi preview/AI đang chờ | Không gửi bản chưa duyệt hoặc cho người khác bản preview |
| AI04 | HS/PH viết và trả lời, dùng/bỏ gợi ý | Cả hai vai có UI; câu gốc/prompt không gửi cho người nhận |
| M01 | Tạo tâm trạng rồi lưu liên tiếp; sửa ngày cũ | Một POST, các PATCH cùng entry/revision; nháp giữ khi lỗi |
| M02 | History/shared-list rỗng, một/nhiều trang, hết trang | Nút hidden thật; không request/append trùng, bounded và dedup |
| M03 | Share preview ở web, sửa ở Mini rồi confirm và ngược lại | 409, lỗi TRONG dialog, GET bản mới, tự confirm lại; không auto-share |
| M04 | PH đọc cả hai client, owner revoke qua F15 | List/detail không đọc được; private DOM/sheet cũ gỡ |
| M05 | Provider thiếu, grant stale, unlink/reconnect | Fail-closed cả body lẫn metadata; không hồi sinh grant |
| V01 | Rút research/AI/service từng purpose | Có hiệu lực đúng mục; không đồng ý hộ, help không bị khóa |
| V02 | Xóa category, scope khác/cutoff/crash/retry | Không xóa nhầm/mới hơn cutoff; checkpoint/hook honest |
| V03 | Restore replay/revocation/consent tombstone | Latest ledger áp trước serve; thiếu hook/provider fail-closed |
| V04 | Stranger/admin/sai school gọi list/detail/process/export | Không có private-data bypass, không scope leakage |
| X01 | HS web lưu mood → PH Mini đọc → revoke web | Một nguồn state, current grant/revision/generation |
| X02 | HS Mini tham gia F02 → PH web ký thỏa ước | Không lệch version/role/cặp; xác nhận hai phía đúng actor |
| X03 | Rút AI qua privacy ở Mini khi web đang gọi AI | Provider/finalize guard và UI xử lý trung thực |
| X04 | Đang pause F06, mở F13 hoặc gửi F10 | Help/tín hiệu không delay; hết timer không tự gửi |
| C01 | F10–F13 mới trên main sau ghép bốn feature | Routes/methods/wiring không mất, private auth và public help đúng |
| C02 | Admin-provision/consent/settings/cards/inbox cũ | Không regression do router/session/CSS/adapter union |

## Môi trường và bằng chứng

1. Backend unit/domain/feature-lab hỗ trợ kiểm logic, nhưng bài chứng minh tích hợp phải dùng `backend/config/settings.py`, URL thật, class-session thật, F01/F05/F15 thật và DB test; không `force_authenticate`/transport giả để gọi production wiring pass.
2. SQLite chỉ là local evidence. MySQL/TiDB test cô lập cho migrations/unique/row-lock/races của source tích hợp; ghi phiên bản thật, skips, constraints warnings, không silenced checks để xanh.
3. Chạy shared/mobile/web/mini suites và production build + verify manifest/import boundaries. Quét route và request semantics thay vì chỉ đếm adapter methods.
4. Serve chính `web/dist` và Mini build/preview hợp lệ; browser thật hai context/actor, không chỉ dev HTML rời. UI screenshot phải từ implementation, không Stitch PNG.
5. Viewports 320/390/430px và desktop/tablet; touch/focus/dialog/keyboard/reduced motion; text 200%/zoom theo công cụ phù hợp, không tự ghi browser CSS scaling là Zalo OS scaling.
6. Synthetic users có 1 primary + 1 backup + stranger + scoped admin; fixture riêng cho từng case destructive/unlink. Không dùng tài khoản lớp thật hoặc mật khẩu công khai; input bounds rõ và không logging nội dung riêng.
7. Gemini live, Render production, Zalo Android/iOS ghi đúng NOT_RUN khi không có quyền/môi trường; mô phỏng không thay thế. Không cộng SKIP/NOT_RUN vào PASS.

## Lệnh kiểm tra gợi ý

Kiểm lại script/settings/dependencies từ checkout nguồn trước chạy. Không thực thi file archive chỉ vì được đóng gói.

```bash
python scripts/check_agent_docs.py
node scripts/check_import_boundaries.mjs
node --test packages/family_bridge_shared/tests/*.test.mjs
git diff --check
# Trong web và zalo-mini-app, lần lượt npm ci, npm test, npm run build.
# Backend thật và feature-lab: theo CI hiện hành, dùng DB test cô lập.
```

Báo cáo suite cần tổng tests, PASS/FAIL/SKIP riêng; cross-client case có UI unlink/reconnect phải chạy bằng fixture đúng, không lấy tầng API thay bằng chứng nút UI. Nếu chưa đạt, giữ report rõ blockers và tiếp tục sửa phần đã được giao.
