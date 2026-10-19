# Phát hiện F02 QA — c29469b, 19/10/2026

Đánh số độc lập với audit F07 và audit F02 cũ. P1 = cản luồng chính hoặc vi phạm trạng thái/quyền kết nối; P2 = đầu ra hoặc metadata chưa đúng. Kết luận theo nguồn và môi trường bên dưới, không suy dữ liệu production.

## F02-QA-R01 — P1: UI lấy revision cũ của hoạt động

**Tái hiện bằng UI thật + đọc dữ liệu server:** tạo hai ContentItem published cùng content_key, revision1 và2. F09 reader trả mới trước. HS903 vào Companion, bấm “Mời cùng làm hoạt động này” của tuần1. SharedActivityInvite thực tế có `content_revision=1`, dù revision2 đang published.

- Nguồn: `zalo-mini-app/src/pages/companion/index.js:360` gán map theo key cho mọi row, bản cũ ở cuối ghi đè bản mới. CTA đọc revision tại559.
- Nguồn thứ tự: `packages/family_bridge_features/f09_activities/wiring.py`, reader order `-published_at,-id`.
- Bằng chứng: phần tử đầu [version-results.json](evidence/version-results.json), DOM/ảnh sau tham gia. Test R1 cũ chỉ cung cấp một revision nên chưa bắt trường hợp này.
- Expected: policy chọn published revision phải rõ và ổn định. Với contract program hiện chỉ tham chiếu key, catalog trả nhiều version thì không tùy thứ tự lấy bản cũ. Nếu chuyển sang pin activity revision, cần contract rõ, không đoán.
- Fix gate: test catalog [rev2,rev1] và thứ tự đảo; nội dung preview và invite cùng revision; không gửi draft/retired; giữ đúng bản khi có pin hợp lệ.

## F02-QA-R02 — P1: đổi program revision làm thỏa ước không thể xác nhận

**Tái hiện HTTP với startup provider thật:**

1. Admin cấp cặp HS905/PH905; cả hai enroll program rev1.
2. HS propose agreement template revision1, chưa ai xác nhận.
3. Clone program thành rev2, chỉ sửa hướng dẫn tuần1; template/cam kết thỏa ước vẫn revision1 — lifecycle cho phép.
4. Cả hai chủ động enroll program rev2.
5. Propose lại trả201 nhưng cùng agreement_id và `program_revision=1`.
6. Confirm trả400 `revision_mismatch`, my_revision2, agreement_revision1. Lặp propose vẫn trả row cũ.

- Nguồn: `f02_program/services/program.py:338` lookup theo agreement revision/pair/generation rồi trả existing, không xử lý program pin; confirm so program revision ở412.
- Ràng buộc liên quan: `f02_program/models.py` unique pair + program_key + agreement_revision + generation, không bao gồm program_revision.
- Bằng chứng: hai phần tử cuối [version-results.json](evidence/version-results.json).
- Expected: người đã cùng chọn bản chương trình mới vẫn có cách hợp lệ hoàn tất thỏa ước cùng nội dung/version. Không tự chuyển về rev cũ hoặc tái dùng chữ ký trái phiên bản.
- Fix gate: quyết định rõ identity của snapshot/thỏa ước khi program mới nhưng template không đổi; test pending/confirmed/withdrawn, một bên repin và hai bên repin. Nếu đổi schema, migration có kế hoạch, giữ lịch sử/chữ ký, không chỉ xóa row hoặc nâng revision ảo để né.

## F02-QA-R03 — P1: lời mời hoạt động vẫn accept sau hủy kết nối

**Tái hiện HTTP thật:** HS901 mời PH901 hoạt động tuần2, pending. HS gọi revoke connection qua F01 thành200/revoked. PH gọi respond accept vào invite cũ, server trả200/accepted.

- Bằng chứng: `NEW-F09-UNLINK` trong [http-results.json](evidence/http-results.json).
- Nguồn: `f09_activities/services/activities.py:138` kiểm participant/status nhưng không recheck connection khi respond; `set_own_response` tại158 cũng cần audit. F02 sử dụng các API này từ Companion.
- Expected: sau unlink không kích hoạt/cập nhật hoạt động chung dựa trên kết nối đã thu hồi. Không lấy active generation mới để hồi sinh invite cũ.
- Đây là lỗi giao thoa F02–F09/F01/F15, không phải lý do cho phép sửa tất cả module. Phối hợp đúng owner, tránh chỉ disable nút frontend.
- Fix gate: mời→unlink→accept/cập nhật bị chặn/cancel đúng contract; kiểm reconnect generation mới, stale UI, race unlink/respond trên MySQL test nếu có. Quyền đọc lịch sử phần mình và quyền tiếp tục chia sẻ là hai chuyện riêng, không xóa lịch sử tùy tiện.

## F02-QA-R04 — P2: confirmed_at sai thời điểm

- HTTP: sau chữ ký HS, chờ rồi PH ký. `status=confirmed` đúng nhưng `confirmed_at` bằng thời điểm chữ ký HS đầu tiên, nhỏ hơn updated_at của chữ ký thứ hai.
- Bằng chứng: `NEW-TIMESTAMP` trong http-results. Không phải lỗi ký hộ: hai timestamp và hai actor vẫn được yêu cầu đúng.
- Nguồn: `f02_program/models.py:234` dùng `min(...)`.
- Expected: nếu field tên confirmed_at là thời điểm thỏa ước đạt confirmed thì phải phản ánh lúc đủ hai chữ ký (hoặc có field transition authoritative tương đương).
- Fix gate: test với hai thời điểm khác nhau, cả hai thứ tự actor; không hiển thị có hiệu lực trước lần xác nhận cuối.

## F02-QA-R05 — P2, thiếu đầu ra: không xem hướng dẫn trước tham gia

- UI thật HS903 chưa enrollment: chỉ thấy một card, danh sách tiêu đề4tuần, nút “Tham gia chương trình”; không có nút đọc hướng dẫn/chi tiết tuần.
- [Ảnh](evidence/01-before-enroll.jpg), [DOM](evidence/01-before-enroll-dom.txt).
- Nguồn: `zalo-mini-app/src/pages/companion/index.js:383`, `renderNotEnrolled`.
- Expected: người dùng được đọc giáo trình/hướng dẫn nội dung đã phát hành trước khi quyết định tham gia; không ép ghi enrollment chỉ để đọc. Không yêu cầu mở dữ liệu riêng khi chưa xác thực; vấn đề này xảy ra với người đã đăng nhập.
- Fix gate: mở được mọi chủ đề/guide qua UI, không POST enroll khi chỉ đọc; chỉ hành động lưu tiến độ mới cần enrollment theo contract đã chốt.

## F02-QA-R06 — P2, thiếu đầu ra: chưa đọc được hướng dẫn hoạt động chung

- Sau enroll, UI chỉ hiện chip tên + “khoảng1phút”, nút mời và done/skipped/reset. Không có màn/nút chi tiết để đọc các bước `body.steps` của F09 published.
- Fixture có4bước cụ thể, ví dụ “Mỗi người chuẩn bị một điều chưa nói ra...”; các bước này không xuất hiện trong DOM, không có CTA mở activity.
- [DOM](evidence/02-enrolled-dom.txt), [ảnh](evidence/02-enrolled.jpg). Tuần2 còn hiển thị tên “nghe nhau10phút” nhưng nhãn thời lượng là1phút.
- Nguồn: Mini App `renderWeekCard` ở480+, dùng title/minutes nhưng không render body; F09 reader trả JSONbody thành dict; service `_safe_content` ép `str(body)` và default minutes1. Không coi default là thời lượng được thầy xác minh.
- Expected: người dùng biết mục tiêu, cách làm, thời lượng có nguồn (hoặc thông báo chưa cung cấp), điều gì được chia sẻ và mời ai trước khi hành động.
- Fix gate: adapter/payload có schema rõ, render text an toàn; không eval hoặc innerHTML dữ liệu. Có activity detail từ đúng revision, không tự bịa metadata. Phối hợp F09; không nhân kho content sang F02.

## F02-QA-R07 — khoảng trống web: trang F02 vẫn tĩnh, tuần2–4 “Sắp có”

- Nguồn được đọc: `web/src/pages/companion/index.js:1` mô tả rõ không gọi adapter, mảng WEEKS hardcode, available=false cho2–4.
- Toàn bộ web tests231pass và buildpass vẫn không kiểm chứng F02 web hữu dụng. Lượt này đọc source trang web và chạy suite/build; chưa thao tác F02web qua UI.
- Expected nếu nghiệm thu F02 cho web: có UI riêng web gọi cùng API, dùng cùng account/progress/agreement; không import Mini App DOM/page hoặc zmp-sdk.
- Phân biệt: bản Mini App chạy trong browser3004 là browser preview Mini App, không phải frontend `web/`. Không gọi việc Mini App hết placeholder là đã hoàn thiện web.
- Đây là gap phạm vi sản phẩm hai client, không phải regression do hai commit fix của Claude gây ra. Agent cần ghi rõ client nào đạt và phối hợp owner web. Nếu chỉ bàn giao Mini App, tuyệt đối không đánh dấu F02web Done.

## Tài liệu bàn giao cũ cần đính chính

- Checklist trong `docs/handover/f02-qa/06-RESUME-HANDOVER.md` ghi HS propose rồi PH confirm sẽ thành confirmed; thiếu bước HS tự confirm. Code hiện **đúng** khi vẫn proposed với một chữ ký. Sửa checklist, không sửa code để làm theo checklist sai.
- Full main SHA trong handover cũ có hai giá trị khác nhau cho ee1346a. SHA đọc lại đúng ở PROVENANCE của lần này.
- Nghi vấn concurrency MySQL, chọn/sửa cam kết1–3, suy ngẫm đi F08/F15, completed/paused chưa được xác minh đầy đủ trong lượt này. Không đánh dấu thành lỗi đã tái hiện; ghi gap/owner và đối chiếu requirements trước mở rộng schema.
