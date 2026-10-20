# PROMPT CHO CHAT CODING — HOÀN THIỆN F02 SAU QA 19/10/2026

Bạn phụ trách hoàn thiện **F02 — Gợi ý kết nối trong bốn tuần** của Family Bridge, dựa trên kết quả QA độc lập và đầu ra Huy yêu cầu bên dưới. Phản hồi, UI và tài liệu cho Huy bằng tiếng Việt. Thực hiện đọc repo → tái hiện → sửa → kiểm thử → chạy local → bàn giao, không chỉ trả lời đã hiểu hoặc đưa kế hoạch.

## 1. Hai repo, hai nhiệm vụ — tuyệt đối phân biệt

**Repo ứng dụng:** https://github.com/huyhandsome6996/family-bridge

- Nhánh làm F02 hiện có: `tinh-nang/f02-dong-hanh-bon-tuan-us036-us044`.
- Head đã QA: `c29469b3d57f2c2cc53fe686fe7ec8f917f2dec6`.
- Main lúc QA: `ee1346a32bb5adaee7fdb7e842fceb7b9b8c32d0`.
- Đây chỉ là mốc đọc, phải fetch và kiểm head mới trước làm. Không reset về SHA cũ.
- Sửa code/test trên nhánh F02 hiện có, bảo toàn commit của owner. Không tự merge/push code vào main, không force push, không tự deploy.

**Repo tài liệu/ảnh/yêu cầu F02:** https://github.com/huyhandsome6996/f07-docx

- **CHỈ làm trên nhánh chính xác `F02-docx`**: https://github.com/huyhandsome6996/f07-docx/tree/F02-docx
- Main của repo này là tài liệu **F07**, không sửa/push/merge vào đó.
- Từ nay mọi prompt, ảnh QA, yêu cầu, báo cáo, hướng dẫn test và handover F02 phải lưu ở nhánh F02-docx, chủ yếu dưới `f02/`. Không đưa báo cáo mới vào main F07 hoặc lẫn với findings F07.
- Đọc `AGENTS.md` và `README.md` trên đúng nhánh F02-docx; không áp prompt F07 trong ZIP vào nhiệm vụ F02.
- Repo này là kho bằng chứng, không phải repo chạy ứng dụng. Không chép snapshot trong đó đè lên source app.

## 2. Đọc ngay gói QA hiện hành

Trên repo tài liệu, đọc:

1. `f02/00-USER-DECISIONS.md`.
2. `f02/qa/2026-10-19-c29469b/README.md`.
3. `FINDINGS.md` — R01–R07 của F02 ngày19/10.
4. `ACCEPTANCE.md`, `TEST-RESULTS.md`, `PROVENANCE.json`, `RESUME-HANDOVER.md`.
5. `evidence/http-results.json`, `version-results.json`, ảnh và DOM; đối chiếu log kiểm thử.
6. `f02/tools/` — runner độc lập, đọc guard trước chạy; chỉ fixture local.
7. `f02/reference/PROMPT-CLAUDE-QA-F02-2026-10-18.md` —51case chi tiết, bối cảnh lịch sử; các SHA/nhận xét cũ phải nhường dữ liệu QA19/10 và source mới.

Không coi file “handover PASS” trong app là bằng chứng đủ. Lượt QA mới chạy68backend +318MiniApp +38shared/mobile +231web đều pass, build/boundary pass, nhưng HTTP/UI thật vẫn phát hiện lỗi. Phải kiểm cả happy path lẫn dữ liệu/version/generation/quyền.

## 3. Cập nhật repo và điều phối trước sửa

- Xác minh origin, fetch main/F02/refs liên quan, fullSHA, git status, worktree list, PR mở và các owner đang làm.
- Dùng checkout/worktree riêng. Không reset/clean, stash hộ, sửa checkout đang chạy của Huy hay cherry-pick mù local patch của Codex.
- Nếu agent F02 còn sửa, nhận mốc bàn giao hoặc thống nhất file ownership; trong lúc đó review/repro độc lập. Không cạnh tranh push cùng nhánh, không ghi đè.
- Trước push phải fetch lại và tích hợp an toàn các thay đổi mới. Đưa main mới vào F02 có kiểm soát nếu cần; không merge F02 vào main.
- Đừng hứa mọi nhánh khác merge sẽ không conflict. Báo chính xác tương thích với SHA nào, file shared nào chạm và cách phối hợp.
- PR F02 từng là #39; tự xác minh head/base/trạng thái. Không cập nhật PR đóng như nơi review code mới. Không tự mở nhiều PR trùng.
- Tài liệu/ảnh mới ở F02-docx; commit/push app và docs tách riêng, ghi sourceSHA ứng dụng trong báo cáo docs.

## 4. Đọc kỹ dự án và call paths trước hành động

Trong checkout ứng dụng mới nhất, đọc `AGENTS.md`, nested instructions, `docs/project-scope.md`, README, security/DSA/UI/workflow skills và rules áp dụng; không bỏ qua vì chỉ sửa UI.

Đọc `docs/product/four-week-flow.md`, `user-flows.md`, `workflow-state-machines.md`, `access-sharing-matrix.md`, `workflow-acceptance.md`, `decision-register.md`, ERD, lifecycle nội dung/admin capabilities, ownership/branch reorganization/shared integration và handover web–MiniApp separation.

US-036: https://trello.com/c/rwjhkqP6/43-e05us-036-gia-%C4%91%C3%ACnh-ch%E1%BB%8Dn-g%E1%BB%A3i-%C3%BD-t%E1%BB%AB-ch%C6%B0%C6%A1ng-tr%C3%ACnh-4-tu%E1%BA%A7n-f02a

US-044: https://trello.com/c/Yu8mhNlV/44-e05us-044-gia-%C4%91%C3%ACnh-xem-ti%E1%BA%BFn-%C4%91%E1%BB%99-v%C3%A0-h%C6%B0%E1%BB%9Bng-d%E1%BA%ABn-s%E1%BB%95-gi%E1%BA%A5y-f02b

Truy vết thật:

- `zalo-mini-app/src/pages/companion/index.js` và router, session, production adapter.
- `web/src/pages/companion/index.js` và router/adapter riêng web; hiện chỉ placeholder.
- `packages/family_bridge_shared/src/adapter/`, API client và session contract.
- `packages/family_bridge_features/f02_program/`: models/migrations/api/urls/services/registry/wiring/apps/tests/seed.
- `packages/family_bridge_features/f09_activities/`: content reader, published catalog, invite/respond/my-response, connection reader.
- F01 Connection/session/revoke, F16 classroom admin provisioning, F15 quyền thu hồi, B16 content lifecycle.
- `backend/config/settings.py`, `urls.py`, feature registry và startup registration; test harness không đại diện toàn bộ runtime production.

Lập bảng ngắn UI → adapter → endpoint → service → dữ liệu/quyền. Nếu chưa đọc được nguồn bên ngoài, nói rõ; không bịa đã đọc.

## 5. Bối cảnh auth và nghiệp vụ mới nhất

- Đăng nhập đang dùng mã HS/PH +mật khẩu. Zalo SDK login cũ dormant, giữ nguyên để sau dùng khi có hạ tầng phù hợp. Không bắt QA F02 quay lại Zalo token/IP Singapore.
- **Admin cấp một hàng PH–HS là canonical primary Connection active ngay**, không bắt hai tài khoản xác nhận ghép đôi. Connection admin có inviteNULL là hợp lệ.
- Active connection không là bằng chứng giám hộ pháp lý, không cấp quyền đọc mọi mood/journal/AI.
- Admin không consent thay người dùng; nghiên cứu và AI riêng, từ chối vẫn dùng chức năng cơ bản.
- **Lời mời hoạt động F09 vẫn cần người nhận đồng ý; thỏa ước F02 vẫn cần HAI actor tự xác nhận cùng version. Propose không tính là ký.**
- Không suy100tài khoản production đã backfill từ việc code provisioning có mặt. Chỉ kiểm fixture giả, không chạm DBthật.

## 6. Đầu vào và đầu ra phải đạt

F02 biến giáo trình bốn tuần thành các việc dễ thực hiện cho học sinh, người chăm sóc và việc cùng làm. Chương trình, từng hoạt động và khảo sát đều tự nguyện.

| Chủ đề | Đầu ra cụ thể |
| --- | --- |
| Tuần 1 — Nhận diện cảm xúc / Tiếng lòng chưa nói | Học sinh gọi tên cảm xúc; phụ huynh có hướng dẫn lắng nghe; chỉ chia sẻ khi chủ động. |
| Tuần 2 — Giảm so sánh / Bản sắc riêng | Ghi nhận nỗ lực, giảm so sánh, luyện lắng nghe và dành thời gian chung. |
| Tuần 3 — Ranh giới / Niềm tin | Thống nhất tôn trọng không gian, điện thoại, thông tin riêng; không ép mở nhật ký. |
| Tuần 4 — Cảm ơn / Xin lỗi / Thỏa ước mới | Cùng chọn cam kết cụ thể; từng người đọc và xác nhận cùng phiên bản; không ký hộ. |

Đầu vào: phiên đã xác thực khi lưu dữ liệu cá nhân; vai trò từ backend; nội dung đã được duyệt và xuất bản; hoạt động được chọn; tiến độ do chính người dùng ghi nhận; kết nối và generation hiện hành khi thao tác cần một cặp.

Đầu ra phải đạt:

1. Người đã đăng nhập đọc được mọi chủ đề và hướng dẫn trước khi quyết định tham gia. Mở tuần 4 trước tuần 1 không bị khóa.
2. Trước khi mời, đọc được mục tiêu, thời lượng có nguồn, cách làm và điều gì sẽ chia sẻ. Không tạo con số thời lượng để lấp chỗ trống.
3. Tham gia, nghỉ và tham gia lại theo từng cá nhân; chọn phiên bản rõ ràng. Xuất bản bản mới không tự chuyển người đang tham gia.
4. Done/skipped/reset lưu và đọc lại đúng tiến độ riêng; không chấm điểm, xếp hạng hoặc tick hộ.
5. Hoạt động chung dùng F09, đúng người nhận, phiên bản và trạng thái. Không tiếp tục hoạt động chung dựa vào kết nối đã thu hồi.
6. Thỏa ước không bị kẹt khi chuyển phiên bản chương trình. Đề xuất đang chờ không làm mất bản đã có hiệu lực. Chỉ đủ hai người tự xác nhận cùng snapshot mới confirmed.
7. Sổ giấy luôn là lựa chọn; không buộc chụp hoặc upload. Suy ngẫm/nhật ký phối hợp F08/F15; không tự tạo kênh chia sẻ ngầm.
8. Trợ giúp không bị chương trình, bộ đếm hoặc khảo sát chặn.
9. Web và Mini App giữ hai cây giao diện riêng, dùng chung API và dữ liệu. Kiểm Mini App trong browser không chứng minh frontend web đã có F02.

## 7. Các việc sửa sau QA — có tái hiện và tiêu chí kiểm lại

Đọc FINDINGS đầy đủ để lấy các bước và bằng chứng. R01–R07 dưới đây là **F02 QA 19/10**, không phải các mã review F07.

### R01 — UI gửi revision cũ của hoạt động

Catalog có rev2 rồi rev1 cùng content_key. Map ở `companion/index.js:360` để bản cũ ghi đè bản mới. Lời mời gửi qua UI thật có content_revision=1 dù rev2 đang published.

- Định nghĩa chính sách chọn phiên bản theo contract, không dựa vào thứ tự row.
- Viết test có hai bản cùng key, đảo thứ tự, revision lớn hơn 1 và retirement.
- Nội dung xem trước và lời mời phải cùng phiên bản. Nếu có pin rõ ràng thì tôn trọng pin; không đoán hoặc hardcode revision.
- Khi nội dung thay đổi sau xem trước, xử lý việc xem và xác nhận lại theo contract; không âm thầm gửi bản khác.

### R02 — Thỏa ước bị kẹt khi program đổi nhưng template giữ revision

Rev1 có pending agreement template1. Clone program thành rev2 chỉ sửa guide; cả hai chủ động chuyển sang rev2. Propose trả lại row program_revision=1; confirm trả400 revision_mismatch. Lặp propose vẫn bị kẹt.

- Làm rõ identity và tính bất biến của snapshot thỏa ước so với program_revision. Template giữ revision không có nghĩa có thể tái dùng mù row đang pin chương trình cũ.
- Sửa lookup, state và schema phù hợp thiết kế; giữ lịch sử, chữ ký và bản confirmed đang hiệu lực.
- Không xóa row, ký lại hộ, repin người kia hoặc tăng revision giả để che lỗi.
- Test các trạng thái pending/confirmed/withdrawn, một người chuyển bản/hai người chuyển bản, template giữ nguyên/đổi mới và generation sau reconnect.
- Nếu cần migration: có kế hoạch bảo toàn dữ liệu, kiểm DB test mới và DB test nâng cấp. Không chạy vào production trong nhiệm vụ này.

### R03 — Lời mời F09 vẫn accept được sau unlink

Invite pending → F01 revoke thành công → F09 respond accept vẫn trả200/accepted.

- Phối hợp owner F09/F01/F15 để enforce backend trên respond/my-response và các transition liên quan.
- Không chỉ khóa nút. Kiểm tra lại canonical connection và generation trong transaction phù hợp.
- Invite cũ không được hồi sinh sau reconnect. Giữ lịch sử phần mình hợp lệ; không xóa hàng loạt để né quản lý quyền.
- Test unlink trước accept, stale client, reconnect, actor ngoài và race unlink/respond trên MySQL test nếu có.

### R04 — confirmed_at dùng thời điểm chữ ký đầu

`f02_program/models.py:234` dùng min. Field thời điểm confirmed phải phản ánh lúc đủ hai chữ ký hoặc một transition timestamp có ý nghĩa tương đương.

- Test hai thời điểm khác nhau và cả hai thứ tự actor.
- Giữ nguyên guard hai người xác nhận vốn đang đúng; không sửa thành propose được tính là chữ ký.

### R05 — Không đọc được guide trước enroll

Trang chưa tham gia chỉ có tiêu đề bốn tuần và nút tham gia, không có cách mở nội dung. Xem guide phải là hành động đọc, không tạo enrollment.

- Cho xem trước mọi chủ đề và hướng dẫn phù hợp từ nguồn published.
- Không mở dữ liệu riêng ra public để xử lý giáo trình đọc trước.
- Test rằng chỉ xem không POST enroll; các hành động lưu tiến độ vẫn theo điều kiện enrollment đã chốt.

### R06 — Thiếu chi tiết hoạt động và metadata có nguồn

F09 body có các bước, nhưng Mini App không render và không có đường mở. UI hiển thị default1phút ngay với hoạt động có tên “nghe nhau10phút”.

- Có schema bounded, typed cho body/steps/minutes/phạm vi chia sẻ. Không eval Python repr, string hoặc dùng innerHTML cho dữ liệu không tin cậy.
- Có màn hoặc sheet chi tiết từ đúng published revision: tên, mục tiêu, thời lượng có nguồn hoặc thông báo chưa cung cấp, các bước, điều chia sẻ, người nhận và hành động tường minh.
- Phối hợp F09; không nhân catalog hoặc hardcode hướng dẫn trong UI để né backend.
- Test malformed content, catalog lỗi, chuỗi có HTML, phiên bản cũ và giới hạn payload.

### R07 — Frontend web F02 vẫn là placeholder

`web/src/pages/companion/index.js` dùng WEEKS tĩnh, available=false cho tuần2–4 và không gọi adapter. 231 web tests pass không thay thế việc nghiệm thu tính năng.

- Nếu bàn giao F02 dùng trên web: cần trang web riêng gọi API thật cho đọc nội dung, enrollment, tiến độ, lời mời, thỏa ước và opt-out.
- Không import trang/DOM/CSS nội bộ Mini App vào web hoặc đưa SDK Zalo sang web. Phần shared chỉ chứa contract và logic không phụ thuộc giao diện.
- Chỉ sửa phạm vi F02 và wiring/test cần thiết; phối hợp bạn của Huy đang làm web. Không refactor màn khác hoặc deploy thay.
- Nếu ownership chưa đồng bộ, tiếp tục phần độc lập và ghi rõ web BLOCKED/owner; không đánh dấu F02 trên cả hai client là Done.

### Đính chính tài liệu và các gap khác

Checklist cũ nói HS propose rồi PH confirm sẽ confirmed, thiếu bước HS tự confirm. Code hiện đúng; sửa hướng dẫn trong báo cáo mới ở F02-docx. Đính chính full SHA, cổng và test counts theo nguồn mới.

Các gap về lựa chọn/sửa 1–3 cam kết cụ thể, suy ngẫm qua F08/F15, paused/completed cần đối chiếu đầu ra, contract và owner. Không tự mở rộng schema vì suy đoán; cũng không hợp thức hóa phần thiếu bằng test sẵn có.

## 8. Những phần đúng phải giữ

- c262428/63341de: primary thắng backup, inviteNULL hợp lệ, không nuốt401 từ các request song song, response phiên cũ không ảnh hưởng actor mới.
- Các sửa lịch sử tại689531e: HTTP weeks dùng activities đúng shape; pending/effective agreement tách nhau; revision pin cũ có exact lookup; mutation có lỗi rõ, chống bấm lặp và stale session guard.
- Không khóa tuần, không tự khảo sát/consent, tiến độ riêng tư, thu hồi và generation, không tự gửi, trợ giúp ngay.
- Không xóa test hoặc đổi expectation để che regression của các guard này.

## 9. Kiểm thử thật trước bàn giao

Chọn exact SHA cuối, DB test riêng và fixture giả. Không dùng100tài khoản thật; không dùng demo1 làm bằng chứng.

- Có ít nhất hai cặp độc lập, một backup và một stranger. Admin cấp active qua service/API thật, không SQL bypass.
- Login HS/PH qua class-session; mỗi người một browser context riêng. Có lượt backend config/registries thật ngoài harness.
- Dữ liệu: draft/published/retired/malformed, program rev1/rev2, template giữ và đổi revision, nhiều activity revision cùng key, bản pin nằm ngoài catalog window.
- UI: home → F02 → xem trước → tự enroll → mở tuần4 → lưu tiến độ và đọc lại → mời/nhận → hai người xác nhận → opt-out → trợ giúp.
- Negative: user_id/role giả, cặp khác đoán ID, bấm lặp, offline/timeout/JSON hỏng, một request con trả401, logout/đổi actor khi GET hoặc mutation đang treo, generation/revision thay đổi.
- Chạy regression consumer web khi thay shared/backend; giữ biên giới import hai frontend.
- Chạy backend check, migration diff, migrations trên DB test; feature suites, shared/mobile, Mini App, web, import boundaries, builds và verify manifest.
- MySQL/TiDB transaction và race chỉ trên DB test được xác nhận riêng. Thiếu môi trường thì NOT_RUN, không suy PASS từ SQLite.
- Zalo thiết bị: Antigravity/Huy kiểm sau khi có nhiệm vụ deploy Testing riêng. Bạn không tự publish, deploy production hoặc merge main.

Lấy lệnh chính xác từ CI và package scripts ở head mới. Không hardcode số test. Windows core.autocrlf có thể làm checker Taste hash lệch bytes: QA này hash LF và git blob đúng, raw CRLF lệch. Không sửa Skill/LICENSE hoặc thay manifest hash để ép PASS.

Mỗi fix có test fail trước/pass sau hoặc state repro rõ. Báo exact SHA, lệnh, exit code, số pass/fail/skip thật, DB, log, ảnh và phần NOT_RUN. Không dựng fixture sai raw payload để làm consumer test xanh.

## 10. Runner QA tham khảo

Đọc source trước chạy; chúng tạo dữ liệu và chỉ dành fixture local.

- `f02/tools/local_fixture.py`: tạo DB SQLite MỚI tại backend/db.sqlite3 của checkout được chỉ định; từ chối DB hoặc backend/.env đã có. Mật khẩu giả từ F02_QA_PASSWORD.
- `http_qa.py`: loopback8004, chạy một lần trên trạng thái sạch. Cuối test hủy cặp901 để kiểm revoke; không chạy lại vào DB đã mutate rồi gọi mọi failure là regression.
- `version_probe.py`: sau HTTP QA và UI HS903 đã mời tuần1; kiểm fixture marker, tạo cặp905, clone programrev2, tái hiện R01/R02. Đọc trước khi đổi port/path.
- `miniapp_repro.test.mjs`: đặt F02_APP_ROOT đến checkout cần kiểm. Ba test tái hiện R01/R05/R06; exit1 trên c29469b là bằng chứng lỗi, không phải test đã pass.

HTTP/version probes hiện lưu kết quả pass/fail rõ trong JSON nhưng không tự exit1 khi assertion fail. Chuẩn hóa exit policy nếu đưa vào CI. Không gọi exit0 là tất cả assertions pass.

Không commit DB hoặc credentials thật. Mã HS901/903/905 và mật khẩu thử trong checklist chỉ dành fixture local, không dùng trên Render.

## 11. Bàn giao để Huy dùng và Codex tiếp tục

Trên F02-docx thêm thư mục mới có ngày/SHA, không ghi đè bằng chứng19/10:

- README: đạt/chưa đạt từng đầu ra; phân biệt kỹ thuật local và readiness cho người dùng thật.
- REQUIREMENTS/ACCEPTANCE: mapping F02/US và từng client.
- FINDINGS: từng R01–R07 fixed/open/retest, repro, test và commit.
- TEST-RESULTS: sanitized logs, HTTP responses, ảnh và DOM.
- PROVENANCE: full app/main SHA, nhánh tài liệu, runtime/DB, dirty files và owner.
- HUY-TEST: URL thật đã mở thành công; tối đa8bước theo dạng trang → thao tác → pass khi.
- RESUME-HANDOVER: file đọc tiếp, commands/process/cổng/cwd, phần dở, ba bước kế tiếp, owner và môi trường thiếu.
- Manifest/checksum và kiểm secret trước khi push kho tài liệu public.

Nếu gần hết lưu lượng: lưu bằng chứng, cập nhật handover, commit/push tài liệu sạch vào F02-docx; code đã được kiểm lên nhánh F02 theo quyền sở hữu. Không đánh dấu code chưa kiểm là hoàn thành hoặc để mất công việc dở.

Cuối cùng gửi Huy kết luận ngắn, URL đã xác minh, checklist, link báo cáo trên F02-docx, SHA và blockers. **Không merge main của cả hai repo, không tự deploy, không tuyên bố thầy đã duyệt nội dung hoặc Zalo/MySQL đã pass nếu chưa có bằng chứng.**
