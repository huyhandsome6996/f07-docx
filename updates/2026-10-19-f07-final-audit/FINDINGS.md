# Finding còn mở ở 2ffd674

Ba finding mức P2 (ảnh hưởng chức năng/khả năng sử dụng; chưa thấy bypass quyền mới trong các ca này). Chúng chặn gate nghiệm thu đã giao dù suites hiện hữu xanh. Không hạ guard backend hoặc nới uniqueness để chữa lỗi UI.

## R08 — lưu thành công xong lại rơi về tạo mới (web + Mini App)

**Nguồn:** `web/src/pages/mood/index.js:295–306` và logic `saveEntry` tương ứng ở Mini App. Callback thành công bỏ payload, xoá nội dung và đặt `state.editing=null`, đổi nút về “Lưu tâm trạng hôm nay”. Lần bấm tiếp luôn POST thay vì sửa mục vừa lưu.

**Tái hiện qua UI thật:** đăng nhập HS chưa kết nối, vào mood, chọn emotion/note, lưu; nhập tiếp note khác, lưu ngay tại editor, không rời trang/không chọn lại history. Nhánh tạo: POST 201 → POST 400; nhánh sửa mục từ history: PATCH 200 → POST 400. Màn hiện “Ngày này đã có mục rồi — hãy sửa mục hiện có trong lịch sử”. Cả hai client đều sai; bốn kịch bản đều FAIL. Nháp sau lỗi vẫn còn, backend chặn duplicate đúng.

Bằng chứng: `evidence/repeat-save-complete/results.json`, 4 ảnh cùng thư mục, `evidence/repeat-save-complete.log`. Repro: `repro/seed_repeat.py`, `repro/repeat_save.mjs`.

**Tiêu chí sửa:** editor giữ đúng `entry_id`, date, revision, emotion/note theo server sau create/edit; lần lưu tiếp PATCH đúng mục đã chọn. Tạo hôm nay → sửa → sửa liên tiếp không duplicate, cùng entry và revision tăng. Sửa mục ngày cũ → lưu tiếp vẫn là mục đó hoặc chuyển chế độ tường minh; không âm thầm ghi vào ngày khác. Chỉ tạo mới khi thật sự chưa có mục ngày cần tạo. Không dùng ngày client làm nguồn chân lý; giữ nháp khi lỗi, lifecycle/session guards, one-entry/day và không auto-share.

Thêm regression trạng thái trong cả hai client và UI E2E không remount editor giữa hai lần lưu. Script E2E cũ bấm “Sửa mục này”/remount trước mỗi edit nên không bắt được lỗi này.

## R09 — nút Tải thêm hết trang vẫn hiện và nhân bản dữ liệu (cả hai)

**Nguồn:** `loadHistory` đặt `moreBtn.hidden = !state.historyNextCursor`; CSS button `.fb-btn`/shell có `display:flex` hoặc `inline-flex`, không có quy tắc phù hợp cho `[hidden]`. Browser vẫn hiển thị nút có `hidden=true`. Handler không chặn khi hết cursor, tải lại trang đầu với cursor null rồi append.

**Tái hiện:** tài khoản synthetic chỉ có một mục, GET trả `results.length=1`, không có trang tiếp. Nút vẫn nhìn thấy/click được. Bấm hai lần: gửi hai GET `/api/v1/mood/entries?page_size=20` không cursor; DOM tăng từ 1 → 3 dòng của cùng mục, trên cả Mini App và web. Đây là lặp UI, không phải DB tạo thêm mood.

Bằng chứng: `evidence/pagination/results.json`, `mini.png`, `web.png`, log. Repro: `repro/pagination.mjs` sau seed và repeat-save.

**Tiêu chí sửa:** nút hết trang thật sự không hiển thị/không nhận focus/click; handler cũng không gọi API nếu không có cursor hoặc đang tải. Không gọi lại first page/append duplicate; chặn double-click/race làm mất hoặc lặp trang. Kiểm tra history VÀ recipient list (cùng kiểu `hidden`/button), empty/one page/multiple pages/last page/retry. Nếu sửa CSS button dùng chung, xác minh tác động tối thiểu ở cả client, không phá control dùng hidden khác. Có thể sửa scoped F07 và guard state; không dùng CSS ẩn dữ liệu private thay authorization.

## R10 — preview đã cũ: API chặn đúng nhưng lỗi nằm ngoài dialog đang mở

**Nguồn:** `confirmShare` catch trong mood của cả hai client chỉ ghi `state._editor.feedback.textContent = errorText(error)`. Sheet vẫn mở (`aria-modal=true`), giữ preview/badge cũ và nút xác nhận; không có lỗi/đường phục hồi trong sheet. Các lỗi mạng/ghi share khác cũng đi qua nhánh này.

**Tái hiện hai chiều:** HS mở preview ở Mini App, HS sửa cùng mục ở web, quay lại Mini xác nhận; làm ngược lại. API trả **409 `preview_stale` đúng**, không cấp bản mới. Thông điệp “Mục này vừa đổi…” xuất hiện ở editor phía sau overlay; nội dung sheet không chứa thông điệp. Đây là lỗi trình bày/phục hồi, không phải backend làm lộ revision mới.

Bằng chứng: `evidence/stale-preview/results.json`, ảnh và log; field `backendProtectionPass` phân biệt phần bảo vệ đang đúng với `feedbackStale=false`. Repro: `repro/stale_preview.mjs`.

**Tiêu chí sửa:** thông báo lỗi đọc được ngay trong modal đang thao tác (live region phù hợp), kèm đường chủ động tải/xem lại bản mới; không để người dùng tưởng đang gửi. Stale phải yêu cầu xem preview mới và xác nhận lại, không tự retry/auto-share revision mới. Timeout/unknown outcome không khẳng định thành công hoặc tự gửi lại. Revoke lỗi cũng hiện ở vùng tương tác thích hợp; 401/session change gỡ private DOM theo guard hiện hành. UI test xác minh nội dung lỗi nằm TRONG dialog, không chỉ `body.innerText` có câu đó.

## Chất lượng gate/báo cáo cần chỉnh cùng đợt

Script `scripts/f07_cross_client_e2e.mjs:305` ghi `check(..., true, "NOT_RUN...")`: output “20/20 PASS” thực tế gồm 19 assertion đã chạy và 1 dòng X07 chưa chạy. Tách status khỏi pass; NOT_RUN không cộng PASS. Nhánh bật unlink thu hồi pair rồi X08 lại share cùng pair chưa reconnect; cần fixture/sequence riêng, không chỉ bật cờ là đủ. X08 prelogout dùng `note || revision`, phải kiểm tra cả nội dung VÀ revision; cả hai PH phải thật sự đang xem private detail trước logout. X05 cũ mới chứng minh list stale ẩn, chưa chứng minh preview 409 có feedback dùng được.

Hoàn thiện E2E X01–X10 theo gate hiện hành: X07 UI unlink/reconnect, X08 late response/đổi actor, X09 IDOR/admin/multi-owner và X10 MySQL có evidence đúng tầng. Không tuyên bố UI đã chạy từ test service. Không cần viết lại backend đang pass để sửa các finding UI này.
