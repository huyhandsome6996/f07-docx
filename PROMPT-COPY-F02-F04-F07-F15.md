# PROMPT CHO CODING AGENT HOÀN THIỆN F02 F04 F07 F15

Bạn là lead coding agent của Family Bridge. Hãy đọc kỹ các repo/nhánh hiện hành, hoàn thiện F02/F04/F07/F15 trên cả WEBSITE và Zalo Mini App, kiểm thử độc lập cây kết hợp, xử lý xung đột theo ý định và chỉ merge vào main khi gate an toàn đạt. Không chỉ trả kế hoạch hoặc báo cáo test mock. Phản hồi/bàn giao bằng tiếng Việt.

## A. Hai repo và quyền thực hiện

**Ứng dụng:** https://github.com/huyhandsome6996/family-bridge

**Bộ tài liệu tổng hợp:** https://github.com/huyhandsome6996/f07-docx/tree/tai_lieu_hoan_thien_F02_F04_F07_F15_docx

Clone/fetch đúng nhánh tài liệu **`tai_lieu_hoan_thien_F02_F04_F07_F15_docx`**, đọc `AGENTS.md`, `README.md`, `hoan-thien-f02-f04-f07-f15/00-READ-FIRST.md`, rồi các tài liệu 01–09 và `prompts/02-MERGE-AN-TOAN.md`. Chạy `python3 tools/validate_integration_kit.py` và `python3 tools/bundles.py verify`. Mọi báo cáo mới của nhiệm vụ tích hợp lưu đúng nhánh docs tổng hợp này, không ghi vào main F07 hay các nhánh docs riêng của người khác.

**Huy giao nhiệm vụ triển khai:** sửa code/tests/docs trong phạm vi bốn feature và phụ thuộc dùng chung thực sự cần, commit/push các nhánh reviewable và merge kết quả vào main ứng dụng khi đã đạt gate, CI/review phù hợp và không có protection chặn. Không xin lại phép chỉ vì prompt/tài liệu lịch sử ghi “không merge” cho đợt cũ. Nhưng không tự bypass bảo vệ nhánh hoặc merge khi còn lỗi/P1/P2/xung đột/chưa đủ bằng chứng. Không merge PR ngoài phạm vi, không xóa nhánh, không đổi secret, không tạo cloud trả phí, không thay backend/DB/domain.

Nhiệm vụ mặc định này không tự phát hành Zalo production hoặc chạy tác vụ destructive trên dữ liệu thật. Render web auto-deploy sau main có thể có: phải chuẩn bị tương thích/flags/release plan trước merge. Nếu Huy có chỉ dẫn deploy riêng trong phiên hiện hành thì áp dụng đúng kênh và kiểm live, không suy từ archive.

## B. Bối cảnh và quyết định không được đổi

Family Bridge giúp học sinh THPT và cha mẹ/người chăm sóc mở lời, lắng nghe và đồng hành. Website và Mini App dùng cùng backend Django/DRF; frontend hiện hành vanilla JS ESM/Vite, Mini có zmp-sdk, shared headless. Không chuyển stack từ prompt React cũ.

- Tài khoản HS/PH được cấp trước; admin lưu cặp → canonical Connection ACTIVE theo DEC-24. Dùng ngay cặp sẵn, không mã mời/proposal/QR/Zalo login bắt buộc. Mã/tên đổi không đổi UUID/quan hệ. Không suy cặp từ số mã; unlink không tự hồi sinh.
- Zalo SDK login cũ dormant được bảo toàn, không bật lại để lách lỗi feature.
- Active connection không mở mood/journal/AI riêng. Grants từng item/recipient/revision/connection-generation, revoke có hiệu lực server, restore không hồi sinh.
- Consent service/AI/research độc lập, không admin nhận hộ. Chương trình/hoạt động/survey tự nguyện; không khóa giao tiếp vì bỏ qua.
- Thỏa ước F02 cần hai actor tự xác nhận cùng revision; propose không là chữ ký. Invite hoạt động F09 vẫn cần người nhận đồng ý, khác với cặp lớp đã ghép sẵn.
- F06 pause 300s server tự chọn; không auto-send sau AI/retry/resume/timeout. Help public không bị khóa bởi auth/consent/Connection/pause/API lỗi.
- Admin chỉ named capability/scope/TTL; không is_staff/superuser/private-data bypass. Tài liệu nghiên cứu không raw survey/nhận diện.

## C. Nguồn và trạng thái tại lúc đóng gói

Main app đã pin `a64f6531e627a9163b98d5a4fe8d6787ea45e36e`, mới tích hợp F10–F13, core wiring và shared methods. Bốn head:

| Feature | Nhánh | Head | PR |
| --- | --- | --- | --- |
| F02 | `tinh-nang/f02-dong-hanh-bon-tuan-us036-us044` | `e38688c8bbcd1848aca727630f0fe79cb98ce992` | #39 |
| F04 | `tinh-nang/f04-ai-ho-tro-dien-dat-us029-us033` | `d33b250f16cab362cb3d93908274ea1df2967351` | #40 |
| F07 | `tinh-nang/f07-tam-trang-va-chia-se-us015-us026` | `3fe66cd6b30fd4e1b905e243f272f13823a52ab1` | #42 |
| F15 | `tinh-nang/f15-quyen-rieng-tu-va-xoa-du-lieu-us012-us017-us023` | `aeae32124a00bd05fc39802f662370df60ebea93` | #33 |

Phải fetch và pin lại refs thực tế; không reset code về các mốc cũ. Cả bốn head đều có conflict với main a64f653; xem `evidence/branch-and-conflicts.json`. PR body có SHA/count/mergeable cũ, không thay refs và kiểm Git mới. Snapshots là reference, không source để chép đè checkout app.

F02/F04/F07 đã có các vòng fix mới, không bắt agent làm lại từ scaffold. F07 findings R08–R10 ở 2ffd674 đã được nhánh 3fe66cd báo sửa; F04 N01–N06 đã được d33b250 báo sửa. Hãy tái kiểm trên cây mới, giữ regression, không gọi lỗi cũ còn mở nếu chưa tái hiện. F15 xa main nhất, cần đặc biệt giữ HS/PH session và UI/API mới.

## D. Đọc và điều phối trước chỉnh sửa

Đọc AGENTS/nested instructions hiện hành trong repo app, project-scope, DSA/security/UI/workflow skills/rules; ERD/contracts/state machines/access matrix/decision register/admin capabilities/content lifecycle; ownership/shared integration; handover web-mini separation; feature docs/API/migrations/tests và yêu cầu US tương ứng.

Xác nhận worktree sạch, remote đúng, owner đang làm, PR/head/CI và paths shared. Dùng worktree riêng; không reset/clean/stash hộ người khác, không overwrite dirty files. Nếu dùng sub-agents, phân domain files độc lập, một lead sở hữu session/shared/router/CSS/migrations/startup; reviewer không lấy báo cáo của implementer làm bằng chứng duy nhất. Không hai agent cùng sửa một tệp.

Lập ma trận UI → adapter → endpoint → service → provider/model → authorization. Phân biệt mã nền cũ/main, bản nâng cấp trên nhánh và nội dung/policy bên ngoài chưa có.

## E. Yêu cầu đầu ra từng feature

**F02 US-036/044:** web/Mini `#/companion` đầy đủ bốn tuần: nhận diện cảm xúc, giảm so sánh/bản sắc, ranh giới/niềm tin, cảm ơn/xin lỗi/thỏa ước. Đọc preview khi chưa enroll; tham gia tự nguyện, activity body/minutes đúng schema; progress riêng pin revision; primary pair đúng dù có backup; F09 invite/respond kiểm current generation; thỏa ước hai actor cùng version, confirmed_at đúng; opt-out, sổ giấy, lỗi/401/empty trung thực. Content seed DRAFT, không tự publish production. Kiểm F02/F09 wiring không bị main core wiring ghi đè.

**F04 US-029/033:** cả HS/PH soạn/nhờ AI/đọc/sửa/dùng hoặc bỏ, rồi preview/confirm send; original không gửi kèm; AI OFF/consent/quota/error/cancel rõ, viết tay vẫn dùng. Gemini backend allowlist/timeout/budget, network ngoài transaction, operation claim/idempotency chống charge trùng, consent check trước call và finalize, generation/actor fences. Giữ recipient-bind/preview snapshot/F06 expected_revision/optional pause. Ghép F15 AI deletion hook đúng registry. Dùng toàn bộ khung thiết kế gốc và parity matrix, không bỏ state bắt buộc hoặc dùng ảnh Stitch làm ảnh kết quả.

**F07 US-015/026:** web/Mini routes mood + mood-shared, home/profile links; tạo/sửa theo ngày server, history/cursor, note riêng; preview đầy đủ item/revision/recipient rồi share; PH list/detail recheck current grant/connection; revoke qua F15 chặn ngay. Kiểm editor lưu liên tiếp đúng entry PATCH, nút Tải thêm hidden thật/không GET lặp, lỗi stale hiện trong sheet và recovery GET không auto-share. Hai chiều cross-client, unlink/reconnect, late response/logout/đổi actor; giữ backend bounds/MySQL race. Không chỉ có module ngoài router.

**F15 US-012/017/023:** quyền riêng tư có UI tương đương trên web/Mini: grants từng item/status/recipient, revoke, unlink, purpose consent withdrawal, category deletion request/receipt/status/cancel. Session HS/PH phải tiếp tục hoạt động; mutation+ledger atomic, cutoff/replay/restore fail-closed, no resurrection và owner/capability/scope đúng. F07/F08 providers cùng nguồn, F04 AI hook đồng nhất; hook/policy thiếu không báo completed. Gửi yêu cầu khác hoàn tất xóa. Không tự bật admin private-data access hoặc retention tùy ý.

Đọc tiêu chí chi tiết tại tài liệu 02–05; đầu ra phải có UI thật cả hai client, không HTML rời/fake-success/mock production.

## F. Tích hợp an toàn

Một nhánh tích hợp tạm từ latest main; đề xuất F15 → F07 → F02 → F04, nhưng xác minh dependencies mới và ghi lý do nếu đổi. Mỗi bước pin head, resolve từng hunk, chạy regression, ghi commit/evidence. Không ours/theirs toàn tệp, không force-push, không squash/cherry-pick mù hay merge kho docs unrelated histories.

Hợp adapter method/DTO/error contracts của bốn feature VÀ F10–F13 main; không sửa số test expected bằng cách xóa method. Giữ router/consent/admin-provision/F01/F16. Review apps.ready/core wiring thứ tự load: không để provider của F15/F07/F02 bị ghi đè. Giữ nhánh W036/consent ngoài scope, phối hợp phụ thuộc thật thay vì kéo vào tự động. Migrations additive, graph MySQL/TiDB đúng; không sửa migration phát hành hay silenced checks.

Sau khi đã có cây kết hợp, tests phải chạy trên chính SHA đó. Nếu main/head tiến phải fetch, đọc diff và tái kiểm phần ảnh hưởng; shared/session/migrations thay thì full gate. Review final diff và bảo toàn contributor changes.

## G. Gate kiểm thử

Áp toàn bộ ma trận A/P/AI/M/V/X/C trong `07-NGHIEM-THU-HAI-CLIENT.md`:

- Backend thật config.settings + class-session và các service/provider DB thật trong môi trường test; không force_authenticate/lab-resolver/transport giả cho chứng minh wiring.
- Unit/harness/negative/authorization/state/race, migrations drift + MySQL/TiDB test cô lập cho constraint/concurrency cần thiết. SQLite không là MySQL.
- Shared/mobile/web/mini tests, boundary checker, agent-docs, production builds + Mini manifest. Browser thật từ artifact build với HS/PH synthetic, primary/backup/stranger/scoped-admin.
- UI/cross-client đầy đủ, revoke/consent/unlink/late response và version conflict; mobile/tablet/desktop, focus/keyboard/dialog/reflow. Screenshot implementation thật với dữ liệu giả; không ảnh thiết kế làm evidence.
- Canaries F10–F13, admin-provision, login/settings/cards/inbox/F06 cũ sau từng phần và cuối cây.
- PASS/FAIL/SKIP/NOT_RUN/BLOCKED tách riêng, không cộng NOT_RUN vào PASS. Không mark Done vì suite cũ xanh.

Gemini live/Render/Zalo device chưa chạy phải ghi riêng. Code có thể merge với flag default-OFF và UI honest khi phần provider/policy bên ngoài chưa có, nếu gate code/an toàn đạt; không tuyên bố chức năng live hoặc pilot hoàn thiện. Nếu thiếu MySQL để chứng minh migration/race đang là rủi ro chưa giải quyết, chưa MERGE_READY.

## H. Merge và bàn giao

Khi source tích hợp đã đạt gate và required checks/review, thực hiện `prompts/02-MERGE-AN-TOAN.md`: merge đúng approved head có expected SHA, không bypass protections/merge commit chưa test; fetch/check final main và regression. Nếu còn blocker thì giữ Draft/branch, báo cụ thể và tiếp tục phần sửa độc lập; không merge để đạt hình thức.

Trả: baseline/head/source PRs và final integration/main SHA; conflict decisions từng file; changes/DSA/bounds/security; tests+environments+evidence; UI routes web/Mini và cách Huy thử; code-merge vs release gate; migration/flags/content/operator/Gemini/device gaps; rollback. Tất cả docs mới commit/push vào nhánh tài liệu tổng hợp được giao, khử secrets. Không tuyên bố đã merge/deploy khi chỉ tạo commit/push nhánh hoặc mở PR.
