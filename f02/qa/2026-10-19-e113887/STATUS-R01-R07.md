# Chi tiết từng mục R01–R07 — cách sửa và cách kiểm lại

Nguyên tắc giữ nguyên nghiệp vụ (đã đối chiếu AGENTS.md + 00-USER-DECISIONS + contract): đăng nhập mã HS/PH; admin cấp cặp → kết nối active ngay; lời mời vẫn cần người nhận đồng ý; thỏa ước cần HAI người tự xác nhận cùng (program_revision, agreement_revision); bốn tuần + hoạt động tự nguyện; tiến độ/suy ngẫm riêng không tự chia sẻ; web và Mini App giao diện riêng dùng chung API; không mất guard cũ.

## R01 — UI lấy revision cũ của hoạt động (P1)

- **Nguyên nhân:** `zalo-mini-app/src/pages/companion/index.js` gán `activityMeta[key] = card` cho MỌI row của catalog F09; reader sắp mới nhất trước nên bản cũ ở cuối ghi đè bản mới; CTA mời đọc `meta.revision` → gửi rev cũ.
- **Sửa:** chính sách chọn tường minh trong helper `buildActivityMeta` (web) / khối dựng map (mini): chỉ nhận `status` published (hoặc row không có status), revision SỐ CAO NHẤT thắng, bằng revision giữ bản đến trước (reader đã sắp mới nhất trước) → **độc lập thứ tự rows**. Áp dụng cả hai client (cùng contract, code riêng).
- **Kiểm lại:** test mini `catalog [rev2,rev1]` và `[rev1,rev2]` đều mời rev 2; draft rev5/retired rev4 không được chọn; chip hiển thị title của bản được chọn. Repro độc lập của QA (R01) GREEN. HTTP: `C02-CATALOG` vẫn PASS, invite tạo với revision 2.

## R02 — Đổi phiên bản chương trình làm thỏa ước kẹt (P1)

- **Nguyên nhân:** `ProgramService.propose_family_agreement` lookup theo (pair, program_key, agreement_revision, generation) rồi trả row cũ bỏ qua program pin; unique constraint cũng thiếu `program_revision` → propose trả row pin rev1 mãi, confirm luôn 400 `revision_mismatch`.
- **Sửa:** identity của instance thỏa ước là **(pair, program_key, program_revision, agreement_revision, generation)** — `FamilyAgreement` thêm `program_revision` vào filter + constraint (migration `0003_agreement_identity_program_pin`, chỉ đổi constraint, không viết lại dữ liệu); propose trên pin mới tạo instance MỚI, pending pin khác bị superseded, row history không bao giờ bị trả lại; một bên chưa repin vẫn bị chặn với lý do rõ (`revision_mismatch` / `agreement_revision_outdated`).
- **Kiểm lại:** 9 test Django (repin hai bên, repin lặp lại, một bên repin, withdrawn history, template đổi revision, generation mới sau reconnect). HTTP thật trên fixture: 15/15 PASS gồm `propose-after-repin-new-row`, `propose-repeat-still-new-pin`, `sig2-confirms-rev2-pin`, `history-kept-two-rows` — xem [http-r02-results.json](evidence/http-r02-repin-results.json).

## R03 — Lời mời hoạt động vẫn accept sau hủy kết nối (P1)

- **Nguyên nhân:** `ActivityService.respond` / `set_own_response` không recheck connection.
- **Sửa:** service-layer guard (không phải khóa nút frontend): (1) invite pin `connection_generation` khi tạo (migration `0002_invite_connection_generation`, cột nullable chỉ cho row legacy); (2) accept + own-response yêu cầu connection **active NGAY LÚC ĐÓ ở CÙNG generation** — unlink → `no_active_connection`, reconnect generation mới → `connection_changed`; (3) decline luôn cho phép (người nhận đóng lời mời stale trung thực); (4) re-invite trên generation mới cancel row stale (giữ lịch sử) và tạo row mới pin generation hiện tại; (5) đọc lịch sử phần mình vẫn hoạt động.
- **Kiểm lại:** 8 test Django; chạy lại bộ HTTP của QA: `NEW-F09-UNLINK` PASS (không accept được sau revoke), `D12-UNLINK`/`D12-OVERVIEW` PASS; không hồi quy các case C04–C07.

## R04 — `confirmed_at` lấy chữ ký đầu (P2)

- **Sửa:** `FamilyAgreement.view()` trả `confirmed_at = max(proposer_confirmed_at, counterpart_confirmed_at)` — thỏa ước confirmed tại chữ ký THỨ HAI; một chữ ký không hiển thị `confirmed_at`.
- **Kiểm lại:** 3 test Django (HS trước, PH trước, đối chiếu max() trong DB); chạy lại bộ HTTP của QA: `NEW-TIMESTAMP` PASS (`confirmed_at > first_time`).

## R05 — Không đọc được hướng dẫn trước khi tham gia (P2)

- **Sửa (Mini App):** `renderNotEnrolled` thêm nút "Xem trước hướng dẫn từng tuần" mở khối chỉ-ĐỌC render MỌI tuần từ catalog đã publish: mục tiêu, "Hướng dẫn cho bạn", "Hướng dẫn cho anh/chị"; hoạt động chung ghi chú mở chi tiết sau khi tham gia. Không POST enroll, không tạo enrollment khi chỉ đọc.
- **Kiểm lại:** test mini xác nhận mở đủ guide cả hai vai trò + `enroll` KHÔNG được gọi + nút "Tham gia chương trình" vẫn là thao tác riêng; repro R05 của QA GREEN; ảnh thật [01](evidence/01-mini-not-enrolled-preview-closed.png) → [02](evidence/02-mini-not-enrolled-preview-open.png).

## R06 — Chưa đọc được hướng dẫn hoạt động chung (P2)

- **Sửa backend (f09):** `_safe_content` trả `body` dạng **typed dict** giới hạn trường `{goal≤300, steps≤10×500, share≤300, text≤2000}` thay vì `str(body)`; `minutes` chỉ pass-through khi là số nguyên 1–1440, nếu không → `null` (không còn default 1 phút bịa).
- **Sửa UI (Mini + web):** mỗi hoạt động có nút "Xem chi tiết hoạt động" mở khối chỉ-đọc: Mục tiêu, Cách làm (steps), Được chia sẻ, thời lượng **có nguồn** ("nguồn: nội dung đã phát hành rev N") hoặc nói thẳng "chưa được cung cấp" — không bịa metadata; ghi chú "mỗi người tự ghi phản hồi của mình — không ai tick hộ ai". Render textContent (qua `h()`), KHÔNG eval/innerHTML dữ liệu; parse body phòng thủ cả dict lẫn JSON-string, JSON hỏng → thông điệp trung thực, không crash, không render repr thô.
- **Kiểm lại:** test mini (chi tiết đầy đủ, minutes null → "chưa được cung cấp" và không có "khoảng 1 phút", body string + dict, JSON hỏng); test web parity; HTTP: body trong `/activities/catalog` là dict có `steps`, minutes trung thực ([http-r02-results.json](evidence/http-r02-repin-results.json) các check `catalog-body-typed-dict`, `catalog-minutes-honest`); ảnh thật [04](evidence/04-web-activity-detail.png), [07](evidence/07-mini-activity-detail.png). Ghi chú trung thực: nội dung fixture seed KHÔNG có `minutes` nên UI hiển thị "chưa được cung cấp" — đúng contract, không tự bịa.

## R07 — F02 trên web là placeholder (khoảng trống phạm vi)

- **Sửa:** viết lại `web/src/pages/companion/index.js` thành trang thật: `programMy` → chưa tham gia thì `programCatalog` + xem trước (parity R05) + enroll có dialog xác nhận; đã tham gia thì `programWeeks` + `programAgreement` + `activitiesInvites` + `activitiesCatalog` song song (lỗi phần phụ hiển thị trung thực từng phần), render 4 tuần từ máy chủ (không khóa tuần, không "Sắp có"), chi tiết hoạt động (parity R06), lời mời accept/decline/invite (parity R01), tiến độ riêng, thỏa ước propose/confirm/withdraw, opt-out có dialog. `requiresAuth` + `chrome: "app"` theo chuẩn các trang web thật. **Không import** DOM/page/component của zalo-mini-app hay zmp-sdk.
- **Kiểm lại:** 8 test web mới (`f02-companion.test.mjs`): tuần từ máy chủ (không còn "Sắp có"/copy tĩnh), progress gọi đúng payload, opt-out qua dialog, gate chưa đăng nhập không gọi API dữ liệu, parity R01/R05/R06; `pages.test.mjs` cập nhật meta + smoke; web suite 239/239; build OK; `check_import_boundaries.mjs` SẠCH. Browser thật (agent-browser): enroll HS901 qua UI web → view đã tham gia; tick "Tôi đã làm" → server log `POST /program/progress 201`; đăng nhập HS901 trên Mini App browser preview → **thấy cùng enrollment + tiến độ** (ảnh [06](evidence/06-mini-cross-client-shared-account.png)) — chứng minh hai client dùng chung account/API mà không chia sẻ giao diện.
- Ghi chú: ảnh vòng QA cũ `web-companion.png` (placeholder cũ) không còn giá trị — trạng thái mới xem ảnh 03–06 trong thư mục evidence của bản cập nhật này.
