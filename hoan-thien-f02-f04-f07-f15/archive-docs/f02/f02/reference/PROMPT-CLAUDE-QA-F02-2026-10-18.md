# FAMILY BRIDGE — GIAO CLAUDE QA ĐỘC LẬP F02 VÀ BÀN GIAO CÓ THỂ TIẾP TỤC

Ngày soạn: 18/10/2026, múi giờ Việt Nam (UTC+7).

**Cách dùng:** gửi nguyên file này cho Claude/coding agent có quyền đọc repo và chạy chương trình. Đây là nhiệm vụ thực hành kiểm thử, không phải yêu cầu viết kế hoạch rồi dừng. Tất cả trao đổi với Huy, nội dung sản phẩm và báo cáo phải bằng tiếng Việt. Không cần trình bày chuỗi suy nghĩ nội bộ; cần quyết định, quan sát và bằng chứng.

---

## 1. Nhiệm vụ của bạn

Bạn là QA độc lập phụ trách **F02 — Gợi ý kết nối trong bốn tuần** của Family Bridge. Một coding agent khác đang hoàn thiện F02. Huy muốn bạn kiểm thử sản phẩm nó bàn giao, xác định còn lỗi gì, và đưa được một bản chạy local để Huy tự trải nghiệm.

Mục tiêu cuối cùng: F02 đáp ứng **đầu ra nghiệp vụ người dùng cần**, chạy qua giao diện Mini App chính thức và backend thật, không chỉ có module/test harness hoặc một trang minh họa. Nếu có lỗi, tái hiện, xác định nguyên nhân, viết regression test hữu ích và xử lý theo quyền sở hữu tại mục 5. Không được kết luận hoàn thành chỉ vì CI xanh hoặc một script có nhiều dòng PASS.

Nếu gần hết hạn mức sử dụng, phải cập nhật tài liệu bàn giao và lưu bằng chứng trước khi ngừng. Chat Codex trước sẽ tiếp tục từ đó. Không để toàn bộ kết quả chỉ nằm trong trí nhớ hội thoại của bạn.

## 2. Hoàn cảnh và những quyết định hiện hành

Family Bridge giúp học sinh THPT và cha mẹ/người chăm sóc mở lời, lắng nghe và đồng hành. Dự án có 15 tính năng, backend chung, hai frontend riêng. Huy đã mất nhiều thời gian với đăng nhập Zalo, vì thế không được đưa hệ thống trở lại một luồng cũ chỉ vì thấy tài liệu lịch sử.

### 2.1. Đăng nhập hiện hành

- Tài khoản lớp học có mã HS/PH và mật khẩu, do hệ thống/admin cấp. Đây là luồng cần dùng để kiểm thử F02 hiện nay.
- ID, vai trò và quyền thực tế do backend xác định; không tin role/user_id/is_admin do client tự chọn.
- Luồng SDK đăng nhập bằng tài khoản Zalo cũ được giữ lại ở trạng thái dormant theo cấu hình/thiết kế hiện hành. Đừng xóa code cũ hoặc ép người thử quay lại đăng nhập Zalo để làm F02.
- Zalo từng từ chối truy vấn thông tin từ IP ngoài Việt Nam với mã -501. Region MySQL/TiDB không quyết định IP máy chủ gọi Zalo. Đây là bối cảnh lịch sử, không phải nhiệm vụ sửa lại hạ tầng xác thực trong QA F02.

### 2.2. Ghép cặp lớp học đã đổi

**Quyết định mới nhất của Huy: admin gán một phụ huynh và một học sinh trong cùng hàng là tạo quan hệ active ngay; người dùng không phải xác nhận ghép đôi lớp học thêm lần nữa.** Main đã có code admin provisioning, provenance `admin_provisioned`, `invite` có thể NULL. Chỉ admin có capability `classroom.provision` và đúng scope mới cấp được cặp.

Điều này KHÔNG có nghĩa là:

- App chứng minh quan hệ cha mẹ/người giám hộ pháp lý.
- Cả 100 tài khoản thật đã được backfill active ở database đang chạy. Phải đọc bằng chứng runtime trước khi khẳng định.
- Admin tự đồng ý điều khoản dịch vụ/nghiên cứu/AI thay người dùng.
- Người thân/admin được đọc nhật ký, tâm trạng riêng, lời gốc gửi AI hoặc dữ liệu nghiên cứu cá nhân.
- Lời mời hoạt động chung hoặc thỏa ước tuần 4 được tự chấp nhận.

**Phân biệt bắt buộc:** kết nối lớp học admin cấp active ngay; lời mời F09 vẫn cần người nhận chấp nhận; thỏa ước F02 vẫn cần HAI người tự xác nhận trên cùng phiên bản. Đừng bỏ xác nhận thỏa ước vì đã bỏ xác nhận ghép đôi.

### 2.3. Frontend và công việc song song

- `zalo-mini-app/`: giao diện Mini App, hiện cũng có thể chạy trong trình duyệt local để QA phần HTTP/DOM.
- `web/`: giao diện web độc lập cho laptop/điện thoại, có người khác làm. Không sửa web để che lỗi Mini App và không import giao diện của hai bên vào nhau.
- `packages/family_bridge_shared/`: hợp đồng/headless code dùng chung; thay đổi có thể ảnh hưởng cả hai frontend, cần phối hợp.
- Backend Django/DRF dùng chung; MySQL/TiDB là database triển khai. SQLite chỉ chứng minh các tình huống local đã chạy, không chứng minh hành vi khóa/giao dịch MySQL.
- F07 hiện do chat/agent khác phụ trách. Không chuyển nhiệm vụ thành hoàn thiện F07/F09/F15/B16 hoặc làm lại toàn bộ app.
- Consent và role-select từng có giao diện cũ, Huy đã yêu cầu thiết kế lại. Có nhánh Consent riêng. Một màn Consent chưa đẹp không đủ để kết luận F02 sai; nhưng lỗi Consent chặn trải nghiệm phải được ghi rõ và phân owner.

## 3. Repo, nhánh, baseline và độ tin cậy thông tin

Repo chính thức: https://github.com/huyhandsome6996/family-bridge

Nhánh F02 chính thức: `tinh-nang/f02-dong-hanh-bon-tuan-us036-us044`.

Không dùng nhánh lịch sử `feat/f02-four-week-program` làm đầu giao việc hiện hành, dù nó còn trong refs/tài liệu cũ.

Thông tin được người soạn **fetch và đọc Git thực tế ngày 18/10/2026**:

| Mục | Giá trị tại lần đọc |
| --- | --- |
| origin/main | `571abcb7916954964d82e0aa27e7661e7d7efd83` |
| origin/F02 chính thức | `689531e06a593d39462041329c0581b4ec1b0aba` |
| F02 implementation trước đó | `ae837b33c62882452c9e235cbee2144e79cf97d9` |
| Handover F02 trước đó | `b482c5c1485dc1d1a381c11dfc4c29391e678785` |
| Vòng sửa R1–R4 | `689531e` |
| Worktree QA riêng của Codex | nhánh local `codex/f02-completion-20261018`, HEAD `3409921` |

**Các SHA trên là mốc tham khảo, không phải yêu cầu quay lại code cũ.** Coding agent đang làm có thể chưa push hoặc sẽ push sau thời điểm này. Trước khi kiểm thử phải fetch và xác định bản bàn giao MỚI NHẤT thực sự cần QA. Ghi full SHA, trạng thái dirty và nguồn của artifact đang chạy. Nếu chưa có bản bàn giao mới, làm baseline audit đọc/test độc lập; không lặng lẽ chiếm nhánh người đang sửa.

PR F02 từng được nhắc là #39: https://github.com/huyhandsome6996/family-bridge/pull/39 . Hãy xác minh metadata, head/base/trạng thái hiện tại trước dùng; đừng suy trạng thái PR từ file này. Không dùng PR đã đóng để đại diện cho commit mới.

Đường dẫn môi trường Huy trước đây:

```text
C:/Users/PC/Documents/Codex/2026-10-14/https-github-com-huyhandsome6996-family-bridge/
  work/f02-completion-20261018/       # QA local của Codex, KHÔNG phải nguồn chính đã push
  work/local-f02-689531e/             # snapshot local cũ đang/đã phục vụ cổng 3002/8002
  outputs/                          # artifact, báo cáo và prompt đã bàn giao
```

Trên máy/cloud khác, tự tìm checkout tương ứng; không hardcode đường Windows vào sản phẩm.

### 3.1. Đặc biệt: có thay đổi QA local CHƯA PUSH, CHƯA BÀN GIAO HOÀN CHỈNH

Codex đã dừng sửa F02 khi Huy thông báo coding agent khác đang làm. Tất cả ở worktree riêng bên trên, không phải main/remote F02:

1. Commit local `3409921` merge main mới vào F02. Hai conflict nằm ở bài test đếm số hàm adapter; đã giữ đủ cả hàm admin và program, tổng tại mốc đó là 86 hàm. Số này có thể thay đổi, không được xóa API thật chỉ để đạt một con số hardcode.
2. Sửa local `f02_program/wiring.py`: chọn connection `primary` cho thỏa ước gia đình, tránh lấy nhầm backup có UUID lớn hơn.
3. File test mới `f02_program/tests/test_current_connections.py`: connection admin cấp không có invite vẫn dùng được; primary thắng backup; backup đơn lẻ không thành cặp thỏa ước.
4. Sửa local `zalo-mini-app/src/pages/companion/index.js` và test: 401 từ các request song song không bị nuốt; thêm guard generation khi tải dữ liệu.
5. Hai script `scripts/f02_local_fixture.py` (mới) và `scripts/f02_e2e_flow.mjs` (sửa): đang chuyển sang fixture admin gán cặp và hạn chế chạy vào loopback. **Chưa chạy xác minh hoàn chỉnh sau lần sửa cuối. Không coi chúng là runner đã pass.**

Nếu cùng máy, chỉ đọc `git diff` để đối chiếu. Đừng reset, clean, commit hộ, sửa hoặc cherry-pick mù toàn bộ worktree này. Báo owner về phần trùng; bản của coding agent mới nhất có thể đã sửa tốt hơn. Nếu máy khác không có worktree này, vẫn tái hiện các case tương ứng từ mục 10; không phụ thuộc patch chưa push.

### 3.2. Bằng chứng đã có, chỉ là tham khảo lịch sử

- 63 tests backend F02 + admin provision + F09 pass trong harness trên worktree tích hợp; lượt này bắt đầu trước khi thêm file 3 test mới.
- 3 test connection mới sau sửa primary/backup pass riêng.
- 17 test Mini App companion tập trung pass sau sửa 401.
- Full Mini App suite pass 314 test tại thời điểm đó.
- Shared + F02 mobile pass 38 test sau merge main local.
- Các số trên KHÔNG chứng minh E2E của code agent mới, MySQL thật, bản deploy, Zalo thiết bị, hoặc nội dung đã được thầy phê duyệt. Bạn phải kiểm lại đúng SHA/artifact của mình và báo số mới thật.

## 4. Đầu ra nghiệp vụ F02 Huy yêu cầu — nguồn nghiệm thu

### 4.1. Nhiệm vụ

Biến giáo trình đồng hành bốn tuần thành chủ đề dễ chọn, có hướng dẫn riêng cho học sinh, người chăm sóc và hoạt động chung. Tham gia tự nguyện, chọn hoạt động phù hợp hoàn cảnh, không ép hoàn thành đủ một chương trình.

### 4.2. Đầu vào

- Phiên người dùng đã được backend xác thực khi lưu lựa chọn/tiến độ cá nhân.
- Vai trò của người dùng từ nguồn backend hiện hành.
- Bộ nội dung bốn tuần đã được người phụ trách chuyên môn duyệt và xuất bản qua lifecycle nội dung.
- Hoạt động người dùng chọn; tiến độ do chính người đó chủ động đánh dấu.
- Kết nối chính đang active khi thực hiện nghiệp vụ cần cặp; generation và revision đúng tại thời điểm thao tác.

### 4.3. Bốn chủ đề bắt buộc

| Tuần | Nội dung và ví dụ đầu ra |
| --- | --- |
| 1 — Nhận diện cảm xúc và “Tiếng lòng chưa nói” | Nhận biết cảm xúc; HS có thể chia sẻ điều khó mở lời; PH có hướng dẫn lắng nghe. |
| 2 — Giảm so sánh và “Bản sắc riêng của con” | Ghi nhận cố gắng; giảm so sánh; HS nhận diện điều mình đã cố gắng; PH luyện ghi nhận và dành thời gian. |
| 3 — Ranh giới riêng tư và niềm tin | Thảo luận tôn trọng không gian cá nhân, điện thoại và thông tin riêng; không biến thành giám sát/chia sẻ bắt buộc. |
| 4 — Cảm ơn, xin lỗi và “Thỏa ước gia đình mới” | Cùng lựa chọn việc cụ thể sẽ tiếp tục thực hiện; từng người xác nhận cùng phiên bản; không tự ký thay. |

### 4.4. Trải nghiệm mong muốn

1. Mở trang chương trình, xem cả bốn chủ đề. Mở tuần bất kỳ, bỏ qua/quay lại hoạt động; tuần 4 không bị khóa bởi tuần 1–3, lịch hay bộ đếm tiến độ.
2. Đọc phần phù hợp vai trò hoặc việc chung; biết mục tiêu, thời lượng (nếu hoạt động có), cách làm và điều gì được chia sẻ.
3. Hoạt động chung đi qua mời/chấp nhận F09, không đồng nhất việc mời với việc hai người đã làm xong.
4. Sau thực hiện, tự đánh dấu hoặc suy ngẫm theo chức năng được xác nhận trong contract. Chỉ nội dung chủ động chọn chia sẻ mới tới người đồng hành.
5. Xem được tiến độ của chính mình, không xếp hạng/streak gây áp lực, không cho PH/HS kia xem suy ngẫm riêng.
6. Hướng dẫn dùng sổ giấy rõ, không buộc chụp/upload nội dung sổ, không ép nhập tất cả vào app.
7. Có thể nghỉ chương trình/tham gia lại. Bỏ qua hoạt động, nghỉ chương trình hoặc từ chối khảo sát/nghiên cứu vẫn dùng được chức năng cơ bản.

**Ví dụ nghiệm thu:** mẹ xem phần giảm so sánh tuần 2, con xem phần ghi nhận cố gắng của mình, một người mời người kia trò chuyện 5 phút; người nhận tự chấp nhận; trạng thái riêng từng người không bị tick hộ. Đây phải là dữ liệu API thật, không chỉ card bấm đổi màu.

### 4.5. Ranh giới

- F02 sở hữu khung bốn tuần, enrollment/tiến độ, hướng dẫn sổ giấy và phần thỏa ước theo contract hiện hành.
- F08 sở hữu nhật ký; F09 sở hữu hoạt động/lời mời/bài học; F14 sở hữu khảo sát; F15 sở hữu quyền chia sẻ/thu hồi và quyền dữ liệu.
- Nếu yêu cầu suy ngẫm/chia sẻ chưa có màn hoặc API đúng owner: ghi GAP cụ thể, xác định đường đi tới F08/F15 và đầu ra còn thiếu. Không tự tạo thêm kho dữ liệu riêng tư trong F02 hoặc tuyên bố “không cần” để hợp thức hóa thiếu tính năng.
- F02 không tự mở quyền đọc dữ liệu riêng khi cặp đã active.
- Nhánh F02 là nơi hoàn thiện chính thức; không gộp tính năng vào main chỉ để dễ demo.

## 5. Cách làm việc an toàn khi đang có agent khác sửa

### Giai đoạn A — nhận bản bàn giao và đóng băng baseline QA

Chạy/read tương đương:

```bash
git remote -v
git status --short
git worktree list
git fetch origin
git rev-parse origin/main
git rev-parse origin/tinh-nang/f02-dong-hanh-bon-tuan-us036-us044
git log --oneline --decorate -12 origin/tinh-nang/f02-dong-hanh-bon-tuan-us036-us044
git diff --stat origin/main...origin/tinh-nang/f02-dong-hanh-bon-tuan-us036-us044
```

- Không in token trong URL remote; redact nếu môi trường có embedded credentials.
- Nếu agent triển khai còn làm: kiểm thử baseline/snapshot đã biết, gửi phát hiện rõ SHA và giữ patch/test ở chỗ riêng; đừng push/chỉnh file nó đang sửa.
- Khi có head bàn giao cuối: kiểm lại trên SHA đó. Không coi kết quả snapshot cũ là kết quả bản cuối.
- Dùng worktree riêng, ưu tiên detached worktree tại exact SHA cho QA. Trước tạo worktree phải xem inventory và giữ checkout của người khác.
- Nếu main mới hơn, báo tương thích/behind thực tế. Chỉ đồng bộ main vào F02 khi bạn là owner sửa đã được giao; không merge giữa chừng khi người khác đang ghi nhánh.

### Giai đoạn B — xử lý lỗi có giới hạn

- Nhiệm vụ mặc định là QA. Phải có báo cáo, test tái hiện và đề xuất fix cụ thể, không chỉ nêu chung chung.
- Nếu agent triển khai đã bàn giao và Huy giao bạn xử lý: sửa những lỗi F02 tái hiện được, giữ contract/owner; commit nhỏ, test fail trước/pass sau, push bình thường vào nhánh F02 hiện có sau fetch lại và kiểm tra không mất commit.
- Nếu chưa nhận quyền viết vì agent còn làm: bàn giao patch/test hoặc hướng sửa; không tự nhận độc quyền nhánh. Có thể tiếp tục kiểm thử phần độc lập.
- **Không push code F02 vào main, không merge PR, không force push, không reset/clean thay đổi của người khác.**
- Không hứa “mọi nhánh sau này merge main đều không conflict”; chỉ báo đã kiểm tương thích với các SHA nào, những file shared nào có nguy cơ.
- Không sửa `web/**` hoặc refactor shared trên diện rộng. Nếu lỗi chung thật sự cản F02, nêu tác động, test cả consumer web và phối hợp owner trước sửa nguồn chung.
- Không tự deploy Render/Cloudflare/Zalo; không apply migrations lên DB đang chạy. Antigravity phụ trách deploy Testing sau khi được giao. Được tạo DB/fixture/server local riêng để QA.

## 6. Đọc repo trước khi chạy/sửa

Lập bản đồ toàn repo bằng danh sách tracked files, cấu trúc và entry points. Đọc đầy đủ các tài liệu/code first-party liên quan đến luồng F02 và các ranh giới dưới đây. Không tuyên bố đã đọc mọi byte của repo nếu chỉ search tên. Không cần đọc binary/font, node_modules, build artifacts, dữ liệu nhạy cảm để đáp ứng câu “đọc kỹ”.

### 6.1. Quy tắc và sản phẩm

- `AGENTS.md`, nested `AGENTS.md` nếu có.
- `docs/project-scope.md`, `README.md`, `SECURITY.md`.
- `.agents/skills/family-bridge-dsa/SKILL.md`, `docs/engineering/dsa-rules.md`.
- `.agents/skills/family-bridge-security/SKILL.md`, `docs/security/security-rules.md`, threat model/control register/verification plan áp dụng.
- `.agents/skills/family-bridge-ui/SKILL.md`, `docs/engineering/ui-rules.md` và Taste skill/provenance nếu đánh giá UI.
- `.agents/skills/family-bridge-workflow/SKILL.md`, `docs/engineering/workflow-rules.md`.
- `docs/product/four-week-flow.md`, `user-flows.md`, `workflow-state-machines.md`, `access-sharing-matrix.md`, `workflow-acceptance.md`, `decision-register.md`.
- `docs/data/erd.md`, `docs/product/admin-capabilities.md`, lifecycle/config catalog và quy định publish liên quan.
- `docs/project/branch-reorganization/branches.json`, `shared-integration.md`, ownership và các supersede notes.
- `docs/handover/web-miniapp-separation/architecture.md` và handover admin pairing/Consent nếu có ở head mới.

US liên quan (đọc qua quyền truy cập thực, nếu không đọc được phải nói rõ):

- US-036: https://trello.com/c/rwjhkqP6/43-e05us-036-gia-%C4%91%C3%ACnh-ch%E1%BB%8Dn-g%E1%BB%A3i-%C3%BD-t%E1%BB%AB-ch%C6%B0%C6%A1ng-tr%C3%ACnh-4-tu%E1%BA%A7n-f02a
- US-044: https://trello.com/c/Yu8mhNlV/44-e05us-044-gia-%C4%91%C3%ACnh-xem-ti%E1%BA%BFn-%C4%91%E1%BB%99-v%C3%A0-h%C6%B0%E1%BB%9Bng-d%E1%BA%ABn-s%E1%BB%95-gi%E1%BA%A5y-f02b

Tài liệu cũ có thể nói F02 “chưa wiring”, dùng nhánh `feat/*`, adapter 69/81 methods hoặc yêu cầu xác nhận ghép đôi. Đọc supersede notes và code mới; không áp dụng máy móc lịch sử.

### 6.2. Call paths phải truy vết thật

1. `zalo-mini-app/src/app/router.js` → `src/pages/companion/index.js` → adapter Mini App → shared endpoints/API client → F02 backend → database/provider.
2. `packages/family_bridge_shared/src/adapter/**` và session/client contracts; `packages/family_bridge_mobile/f02_program/**` chỉ là một consumer/module, không thay thế việc kiểm trang chính thức.
3. `packages/family_bridge_features/f02_program/`: models, migrations, auth, API/urls, registry, `services/program.py`, `wiring.py`, `apps.py`, tests, seed command.
4. `backend/config/settings.py`, `backend/config/urls.py`, feature registry: chứng minh app production dùng đúng provider/session/URLs, không chỉ test doubles.
5. B16 `admin_core` ContentItem/lifecycle; F09 catalog/invites/wiring; F01 Connection/session; F16 ClassAccount/admin provisioning; F15 revoke/unlink liên quan.
6. `docs/features/f02/**`, `docs/handover/f02-four-week-program/**`, `scripts/f02_e2e_flow.mjs`, CI workflows và các test độc lập đã có.

Phải xuất bảng “trang → adapter method → HTTP → service → dữ liệu/quyền”. Nếu màn nhìn đúng nhưng không có call path thật, ghi FAIL/GAP.

## 7. API tham chiếu — đối chiếu với head mới trước gọi

Prefix API: `/api/v1`. Các đường dưới được đọc từ source F02 tại baseline; không tự thêm slash/field theo phỏng đoán. Contract cuối cùng phải được kiểm với source và HTTP thật của bản đang QA.

| HTTP | Đường | Ý nghĩa |
| --- | --- | --- |
| POST | `/auth/class-session` | Đăng nhập mã HS/PH + password, nhận phiên ứng dụng |
| GET | `/connections` | Đọc kết nối active/đối tượng đúng theo contract |
| GET | `/program/catalog` | Nguồn chương trình đã publish |
| POST | `/program/enroll` | `{program_key, program_revision}`; tự nguyện, pin revision |
| GET | `/program/my` | Enrollment của người đang đăng nhập |
| POST | `/program/opt-out` | `{program_key}`; nghỉ chương trình |
| GET | `/program/weeks/{program_key}` | Cả bốn tuần ở revision đang pin, tiến độ của mình |
| POST | `/program/progress` | `{program_key, week_no, activity_key, status}`; done/skipped/reset |
| POST | `/program/agreement/accept` | Acceptance template cá nhân cũ; KHÔNG đủ chứng minh thỏa ước hai phía |
| GET | `/program/agreement?program_key=...` | Overview template/bản hiệu lực/đề xuất của đúng cặp |
| POST | `/program/agreement/propose` | `{program_key}`; tạo đề xuất |
| POST | `/program/agreement/{agreement_id}/confirm` | Chính người hiện tại xác nhận |
| POST | `/program/agreement/{agreement_id}/withdraw` | Rút đề xuất theo quyền/trạng thái |
| GET | `/activities/catalog` | Nội dung hoạt động F09 published và revision thật |
| GET/POST | `/activities/invites` | Đọc/tạo lời mời, field theo contract F09 |
| POST | `/activities/invites/{invite_id}/respond` | Người nhận accept/decline theo contract |

Không nhầm `joint_activity_keys` của JSON nội dung B16 với payload `/program/weeks`: tại baseline HTTP weeks trả `activities:[{activity_key,status}]`. Tiêu đề/thời lượng/revision F09 phải đến từ catalog thật, không tạo fixture sai shape để che lỗi consumer.

Token ứng dụng chỉ dùng header theo cơ chế hiện hành; không bỏ vào URL, screenshot, báo cáo/log hoặc bundle. Luồng auth app không dùng cùng ý nghĩa với Zalo SDK token.

## 8. Chuẩn bị môi trường kiểm thử tách biệt

1. Chọn exact SHA bàn giao. Ghi repo, nhánh, working SHA, main SHA, dirty diff và thời điểm.
2. Xem process/cổng đang dùng. Cổng 3002/8002 có thể đang chạy snapshot cũ của Huy, không tự kill hoặc ghi đè DB.
3. Nếu cần, dùng frontend `127.0.0.1:3003`, backend `127.0.0.1:8003` hoặc cổng trống khác. Cấu hình API base + CORS chính xác. Không coi cổng ví dụ là server đang sống.
4. Cài dependency theo lockfile và phiên bản CI/package engines hiện hành. Không upgrade để “sửa nhanh”; không thêm framework React/zmp-ui vào frontend mới.
5. Dùng DB local/test riêng, fixture giả rõ ràng. Không trỏ MYSQL_* production/TiDB thật, không dùng 100 tài khoản thật để thử xóa/unlink/sửa hàng loạt.
6. Tạo ít nhất hai cặp độc lập A=HS_A/PH_A, B=HS_B/PH_B; thêm tài khoản không kết nối và backup supporter C khi kiểm quyền. Tạo bằng luồng/service admin cấp cặp hiện hành, đúng capability/scope, không viết tắt active bằng SQL để né code cần kiểm.
7. Kiểm trạng thái ngay sau admin cấp: canonical Connection active, invite có thể NULL, source/provenance đúng, không có consent/grant giả và không cần end-user proposal confirm.
8. Đăng nhập qua endpoint thật, mỗi người một phiên/browser context riêng. Đừng cùng localStorage/session toàn cục rồi gọi đó là hai người độc lập.
9. Nội dung test gồm draft/valid published/malformed/retired, program rev1/rev2, activity có revision >1 và fixture nhiều hơn catalog window. Chỉ publish synthetic trong DB riêng để kiểm lifecycle; việc này không phải thầy phê duyệt nội dung sử dụng thật.
10. Phải có một lượt chạy backend bằng `backend/config/settings.py` và registries startup thật, không monkeypatch provider/session resolver. Harness vẫn cần nhưng không đủ.

**Lưu ý runner có sẵn:** đọc script trước chạy. `f02_e2e_flow.mjs` ở remote baseline cũ cố định backend8002 và yêu cầu xác nhận proposal hai bước; không được dùng kết quả đó để chứng minh luồng admin mới. Script sửa ở worktree Codex chưa được xác minh. Nếu viết runner mới, bắt buộc chặn mọi base URL ngoài loopback khi có mutation, kiểm fixture marker/DB riêng và dừng khi sai môi trường; output không chứa token/password.

Không tự chạy script tạo fixture vào một DB đã có dữ liệu. Ưu tiên checkout/DB mới, không có `.env` production. Nếu thiếu MySQL, tiếp tục QA local hữu ích và đánh dấu phần MySQL NOT_RUN; không đổi cấu hình triển khai sang SQLite.

## 9. Quy trình QA, theo thứ tự ưu tiên

1. Hiểu nghiệp vụ bằng bản diễn giải khoảng 300–500 từ: ai làm gì, dữ liệu riêng là gì, đâu là active connection, đâu là acceptance/invite/agreement, revision/generation ảnh hưởng thế nào. Gắn với đường code thật.
2. Audit diff và kiểm runtime wiring; tìm mismatch giữa contract/tài liệu/test doubles/consumer.
3. Smoke local thật: login → consent dịch vụ theo người dùng → home → companion → catalog/enroll → mở tuần4 → tiến độ reload → hai phía mời/thỏa ước.
4. Kiểm các ca sai quyền, sai revision, generation mới, phiên hết hạn và lỗi mạng trước khi làm polish giao diện.
5. Reproduce các lỗi cũ và hai nghi vấn mới ở mục 11; test đúng raw payload thật.
6. Bổ sung regression có ý nghĩa cho lỗi thực sự; nếu sửa, fail trước/pass sau. Không đổi expectation để hợp thức hóa hành vi sai.
7. Chạy suite/build/boundary/docs đúng phạm vi; kiểm consumer web khi shared API bị ảnh hưởng nhưng không sửa giao diện web của người khác.
8. Mở URL local đã tự xác minh, để Huy test theo checklist ngắn; lưu report/handover. Nếu thiếu môi trường, hoàn thành phần làm được và mô tả đúng chỗ dừng.

## 10. Ma trận kiểm thử bắt buộc theo đầu ra

Mỗi case phải có `ID`, precondition, actor, steps, expected, actual, status, bằng chứng và exact SHA. Không ghi PASS bằng cách đọc source đơn thuần cho case runtime.

### A — Luồng hiện hành và nội dung

| ID | Thao tác / điều kiện | Tiêu chí đạt |
| --- | --- | --- |
| A01 | Admin cấp cặp giả; HS và PH đăng nhập | Đã active, đúng counterpart; không bị ép /proposal xác nhận; không có consent/grant riêng tư sinh hộ. |
| A02 | Đi từ home vào chương trình | Đúng trang Mini App chính thức, API thật, không fixture/mock ngầm. |
| A03 | DB chỉ có draft hoặc chưa có chương trình | Empty state đúng nguyên nhân, không “Sắp có” để che UI chưa nối; không tự publish, không bịa chương trình. |
| A04 | Publish chương trình hợp lệ trong DB test | Catalog/weeks hiển thị đúng version đã publish; draft/retired/malformed không lọt. |
| A05 | Xem bốn chủ đề đã nêu | Đủ 1–4, nội dung/cách làm đúng source; không hardcode nội dung cũ thay response. |
| A06 | HS rồi PH mở hướng dẫn | Đúng hướng dẫn theo vai trò server; không đổi quyền chỉ bằng sửa client. |
| A07 | Chưa làm tuần1, mở tuần4 và tuần3 | Đọc được, không khóa tuần/gate theo tiến độ/lịch. |
| A08 | Người không có cặp mở chương trình | Phần cá nhân không bị khóa chỉ vì chưa kết nối; phần cần cặp giải thích rõ điều kiện. |
| A09 | Chọn không tham gia | Dùng được chức năng cơ bản; không tự enrollment; không ép khảo sát. |

### B — Enrollment, tiến độ và dữ liệu riêng

| ID | Thao tác / điều kiện | Tiêu chí đạt |
| --- | --- | --- |
| B01 | Bấm tham gia rồi reload/đăng nhập lại | Server lưu đúng enrollment/revision, UI khôi phục đúng. |
| B02 | Chọn done → skipped → reset | Đúng API, reload đúng trạng thái contract; reset không giữ trạng thái cũ ngầm. |
| B03 | HS done, PH skipped cùng hoạt động | Hai trạng thái độc lập; không tick hộ, không family progress giả. |
| B04 | Gửi participant_id/user_id của người khác hoặc sửa body | Không sửa/đọc hộ; field ngoài contract bị xử lý đúng; danh tính lấy từ phiên. |
| B05 | Activity/tuần không thuộc bản đang pin | Server từ chối, không tạo progress mồ côi hoặc lách sang chương trình khác. |
| B06 | Nội dung rev2 publish sau khi đang theo rev1 | Không silent migrate; mở/reload vẫn rev1; chuyển version chỉ khi người dùng chọn rõ. |
| B07 | Chuyển revision có activity_key trùng | Progress rev1 không bị kế thừa sai sang rev2; bản cũ được quản lý theo contract. |
| B08 | Tạo >20 release để bản pin rơi ngoài catalog | Exact lookup bản pin vẫn hoạt động nếu bản đó còn published; không thành “chưa phát hành” vì LIMIT. |
| B09 | Opt-out rồi rejoin | Tự nguyện, không mất quyền dùng chức năng khác; giữ/khôi phục tiến độ đúng contract, chọn version rõ. |
| B10 | Hướng dẫn sổ giấy | Hiện được, không bắt upload/chụp sổ hoặc hoàn thành form để dùng app. |
| B11 | Suy ngẫm/nhật ký liên quan | Chỉ chủ sở hữu thấy mặc định; nếu chưa có đường dùng thật, ghi GAP + owner, không bịa đã hoàn thành. |

### C — Hoạt động chung qua F09

| ID | Thao tác / điều kiện | Tiêu chí đạt |
| --- | --- | --- |
| C01 | Dùng raw payload weeks thật `activities` | Hiện đúng hoạt động/CTA, không phụ thuộc field test tự bịa. |
| C02 | Activity catalog revision >1 | Invite dùng revision hiện hành đúng item; không hardcode1. |
| C03 | Hoạt động chưa publish/retired | Không mời được nội dung không hợp lệ; UI nói đúng lý do. |
| C04 | HS mời PH, PH mở app/context riêng | PH thấy đúng invite và đúng người; chưa đồng ý thì còn pending. |
| C05 | PH accept/decline; thử HS respond hộ | Chỉ người nhận được phản hồi; hai phía trạng thái nhất quán. |
| C06 | Người khác/cặp B truy cập invite cặp A | Không lộ nội dung/đối tượng; trả lỗi đúng contract. |
| C07 | Bấm mời nhiều lần/response chậm | Không nhân mutation do UI bấm lặp; idempotency/backend theo contract; không tự retry gửi. |
| C08 | Invite accepted | Không tự đánh dấu hai người hoàn thành, không gửi tâm sự/suy ngẫm kèm. |

### D — Thỏa ước gia đình tuần4

| ID | Thao tác / điều kiện | Tiêu chí đạt |
| --- | --- | --- |
| D01 | Admin pair active, inviteNULL | Tạo thỏa ước đúng cặp, không lỗi do assumptions về invite cũ. |
| D02 | Có primary và backup đồng thời | Thỏa ước đúng counterpart primary; backup không thay thế chỉ vì UUID/thứ tự lớn hơn. |
| D03 | Chỉ có backup, không primary | Không lặng lẽ coi backup là cặp gia đình chính. |
| D04 | Một người propose | Còn proposed, không giả timestamp xác nhận của một/hai người. |
| D05 | Chỉ một người confirm, bấm lặp | Chưa confirmed hai phía; một actor không thể ký hai lần cho cả cặp. |
| D06 | Hai người tự confirm cùng revision | Chỉ lúc này confirmed; dữ liệu timestamp/actor phản ánh thật; thứ tự HS/PH không quyết định quyền. |
| D07 | Khác program/agreement revision | Không xác nhận nhầm bản; yêu cầu đồng bộ/đề xuất đúng và thông báo rõ. |
| D08 | Confirmed rev1 → propose rev2 | Rev1 vẫn hiệu lực trong lúc rev2 pending; proposal mới không tự vô hiệu bản đã xác nhận. |
| D09 | Rút pending rev2 | Chỉ đúng người/đúng trạng thái được rút theo contract; rev1 hiệu lực giữ nguyên. |
| D10 | Hai bên confirm rev2 | Chuyển hiệu lực/supersede đúng; không còn hai bản hiệu lực mâu thuẫn. |
| D11 | Cặp B đoán agreement_id của cặp A | Không đọc, confirm, withdraw hộ; không lộ dữ liệu riêng qua lỗi. |
| D12 | Unlink rồi reconnect generation mới | Không tái dùng chữ ký/thỏa ước của generation cũ; thao tác dùng dữ liệu cũ bị chặn. |
| D13 | Race confirm/withdraw/unlink/revision | Chuyển trạng thái atomic, không lỗi500/ghi sai; phân biệt kết quả SQLite và kiểm khóa MySQL thật. |

### E — Phiên, lỗi và trải nghiệm thực

| ID | Thao tác / điều kiện | Tiêu chí đạt |
| --- | --- | --- |
| E01 | Không token/expired token | API chặn; frontend về login/expired đúng, không thành empty catalog hoặc tự demo. |
| E02 | programMy OK, weeks/agreement hoặc request song song trả401 | Không nuốt 401 thành null/trang trống; không còn quyền hiển thị dữ liệu cũ. |
| E03 | Logout/đổi actor khi GET cũ đang treo | Phản hồi muộn không render dữ liệu/điều hướng sai phiên mới. |
| E04 | Logout/đổi actor khi mutation cũ đang treo | Không cập nhật UI mới từ response cũ; không để người mới thấy trạng thái riêng người cũ. |
| E05 | Offline/timeout/invalidJSON/404/409/503 | Lỗi trung thực, trạng thái không fake success; retry do người dùng chủ động, không tự gửi lại mutation. |
| E06 | Chỉ một phần catalog/invite lỗi | Không che lỗi như “không có nội dung” khi chưa xác minh; phần dùng được vẫn rõ, có đường khôi phục. |
| E07 | Trợ giúp trong mọi trạng thái F02 | Không bị opt-out, pause, consent nghiên cứu hoặc tiến độ chương trình chặn. |
| E08 | Browserlocal không có `?demo=1` | Có network/API thật và dữ liệu server; demo được tách và dán nhãn, không làm bằng chứng nghiệm thu. |
| E09 | Rộng360/390/768/1366/1440 | Đọc và bấm được, không tràn ngang/che CTA; keyboard/focus/dialog hoạt động. Localbrowser chưa chứng minh SDK/deviceZalo. |
| E10 | Web regression sau thay shared/backend | Web vẫn build/test, auth/API compatibility giữ; không copy MiniApp UI vào web hay ngược lại. |

Ưu tiên quyền riêng tư/sai cặp/sai phiên/sai phiên bản/giả xác nhận là blocker. Thiếu MySQL/Zalo device là khoảng trống bằng chứng cần ghi rõ, không tùy tiện đổi thành PASS hay bỏ toàn bộ công việc local.

## 11. Các lỗi cũ và nghi vấn phải kiểm độc lập

### R1–R4 từng phát hiện và sửa ở remote `689531e`

- R1: UI đọc `joint_activity_keys` trong HTTP weeks trong khi response thật là `activities`; fixture cũ che lỗi. Kèm hardcode F09 revision1.
- R2: tạo pending thỏa ước mới làm mất/supersede bản confirmed đang hiệu lực trước khi đủ hai chữ ký.
- R3: enrollment pin cũ không mở được vì version bị đẩy khỏi bounded catalog.
- R4: mutation lỗi bị nuốt, bấm lặp, và response cũ cập nhật phiên người khác.

Không chỉ đọc test đã viết để gật đầu. Chạy với raw HTTP shape/revision>1/actor riêng/pending vs effective thật.

### Hai lỗi mới Codex đã tái hiện trên baseline tích hợp local

1. Chọn backup thay primary do query active không filter relationship_kind và order UUID. Test có primary UUID nhỏ, backup UUID lớn cho kết quả sai trước sửa. Kiểm A/B hai chiều và backup-only.
2. `Promise.all` GET con `.catch(()=>null)` nuốt401 khi tải weeks/agreement. Kiểm một request401 và các request khác200, với adapter thực sự thay đổi/clear session như runtime; kiểm stale success lẫn stale failure.

Các điểm khác chỉ là câu hỏi audit, KHÔNG phải bug đã xác minh: transaction thỏa ước khi unlink đồng thời; revision agreement khi content đổi; điều kiện withdraw sau connection thay đổi; trạng thái partial-fetch. Hãy tái hiện và đọc contract trước kết luận, tránh báo cáo khẳng định quá bằng chứng.

## 12. Suite và lệnh tham khảo

Đọc CI và scripts tại head mới để lấy lệnh chính xác. Không chạy đúng một test module rồi khẳng định toàn app. Ghi exit code và log từng lệnh. Trên PowerShell dùng env syntax PowerShell, đừng copy Bash nguyên xi.

Backend harness dùng đủ integration feature labels (F02 wiring tiêu thụ F01/F09/B16/F16):

```bash
cd tests/feature-lab
export DJANGO_SETTINGS_MODULE=harness.settings
export DJANGO_ENV=test
export FB_FEATURES=f01_identity,f15_privacy,f05_inbox,f03_cards,f04_ai,f06_drafts,f07_mood,f08_journal,f10_signal,f11_supporters,f13_help,f12_appointments,f09_activities,f02_program,f14_surveys,admin_core,f16_classroom
python manage.py test family_bridge_features.f02_program family_bridge_features.f09_activities family_bridge_features.f16_classroom.tests.test_admin_provision -v 1
```

Nếu label/path thay đổi, tìm path thật và ghi lý do thay. Harness dùng user app/test resolver riêng, không dùng kết quả để chứng minh production auth/wiring.

Từ repo root, các lệnh client/kiểm biên giới tham khảo:

```bash
node --test packages/family_bridge_shared/tests/*.test.mjs
node --test packages/family_bridge_mobile/f02_program/tests/*.test.mjs
node scripts/check_import_boundaries.mjs
python scripts/check_agent_docs.py
```

Trong `zalo-mini-app/`: `npm ci`, `npm test`, `npm run build` theo lockfile. Build có verify manifest/assets; đọc output thực, không chỉ thấy Vite compile.

Trong `web/`: chạy tests/build phù hợp package scripts khi thay shared/backend hoặc sync main ảnh hưởng consumer; giữ nguyên web source.

Kiểm migration với database test đúng backend thật: `check`, `makemigrations --check --dry-run`, migration trên DB disposable từ schema baseline đến schema mới; không bỏ lỗi bằng `|| true`. Nếu CI helper có chỗ nuốt exit code, đọc log và chạy check trực tiếp.

Chạy integration/E2E riêng qua server HTTP thật và startup registries thật; xác thực hai actor bằng login API. Không patch provider/session resolver trong lượt này. Cố định nguồn nội dung synthetic, lưu bản dữ liệu đã redact để kiểm contract.

MySQL8/TiDB: chỉ trên DB test đã xác nhận tách biệt, kiểm migration/unique/transaction/races/JSON/UUID/query behavior. Nếu không có môi trường, báo NOT_RUN và bước tiếp theo cụ thể. Không chạy load/scan/xóa vào production.

## 13. Bằng chứng và cách kết luận

Mỗi kết luận phải liên kết với nguồn:

- Code review: path + line + SHA, trigger và hậu quả.
- Unit/integration: lệnh, exit code, số pass/fail/skip, phiên bản runtime, DB, log.
- API: method/path, actor giả, payload/redactedresponse, status, state trước/sau. Không token/password.
- UI: route thật, viewport, hành động, ảnh/screencast đã redact, network chứng minh server cùng SHA.
- MySQL/device: chỉ ghi PASS khi đã chạy trên môi trường đó.

Trạng thái từng case chỉ chọn: **PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE (có lý do)**. Tách lỗi sản phẩm, thiếu content được phê duyệt, thiếu hạ tầng test, và việc thuộc owner khác.

Phân mức: P0/P1 dữ liệu sai/quyền sai/cặp sai/không hoàn tất coreflow; P2 trải nghiệm/khôi phục/thiếu nhánh nghiệp vụ; P3 polish. Không thổi severity cho lỗi văn bản nhỏ, không hạ severity lỗi riêng tư vì chỉ dùng thử lớp học.

Kết luận cần có hai trục:

1. **Kỹ thuật trên local:** coreflow/API/UI trên SHA nào đạt, còn blockers nào.
2. **Sẵn sàng cho người dùng thật:** content đã phê duyệt/published chưa, migration/deployment có đúng head chưa, MySQL và Zalo device đã kiểm chưa.

Không dùng một chữ “Done” để gộp hai trục. Empty state đúng khi chưa publish có thể PASS cho case A03, nhưng chưa đủ nói Huy đã trải nghiệm đầy đủ giáo trình.

## 14. Giao Huy URL và checklist ngắn để tự test

Khi server local đã chạy và bạn đã tự mở thành công, đưa các link hoàn chỉnh theo cổng THỰC TẾ. Ví dụ chỉ khi bạn thật sự dùng3003:

- `http://127.0.0.1:3003/#/login`
- `http://127.0.0.1:3003/#/consent` (nếu chưa có service consent; không đổi hộ consent nghiên cứu)
- `http://127.0.0.1:3003/#/companion` — trang F02 chính
- `http://127.0.0.1:3003/#/help` — kiểm trợ giúp không bị chương trình chặn

`#/role-select`, `#/proposal` không phải đường bắt buộc để xác nhận lại admin-assigned relationship. Nếu router tự đưa qua đó sai luồng, ghi lỗi và đối chiếu trạng thái tài khoản thực trước kết luận.

Không đưa link sai dạng `https://miniapp.zaloplatforms.comhttp://127...`. Không thêm `?demo=1` vào link nghiệm thu thật. “Local web” ở đây là cách mở frontend Mini App bằng trình duyệt để thử HTTP/UI; không được trình bày như đã nâng cấp frontend `web/` hay đã test Zalo thật.

Checklist gửi Huy tối đa khoảng8 dòng, dạng **trang → làm gì → thế nào là đạt**, ví dụ:

| Trang | Việc làm | Pass khi |
| --- | --- | --- |
| Login → Companion | Đăng nhập HS giả, mở chương trình | Đúng tài khoản/cặp; đọc được nội dung đã publish. |
| Companion | Mở tuần4 trước tuần1 | Không khóa, không “Sắp có” với nội dung đã phát hành. |
| Companion | Tham gia, done/skipped/reset, reload | Server giữ đúng tiến độ riêng. |
| Companion, PH ở context khác | PH đánh dấu trạng thái khác HS | Không ghi đè/lộ tiến độ người kia. |
| Companion | Mời hoạt động, người nhận accept | Chờ đúng người nhận, trạng thái cập nhật thật. |
| Companion tuần4 | Đề xuất, chỉ1 người xác nhận, rồi người thứ2 | Chỉ đủ2 người cùngversion mới confirmed. |
| Companion | Nghỉ chương trình | Không chặn tính năng khác, có thể quay lại. |
| Help | Mở từ trạng thái đang nghỉ/chưa tham gia | Trợ giúp vẫn truy cập được. |

Cung cấp mã tài khoản fixture và cách nhận mật khẩu giả qua file local/biến môi trường riêng; đừng dùng mật khẩu thật trong repo public. Phải nói rõ tài khoản này chỉ ở DB local, không phải100tài khoản Render.

## 15. Artifact bắt buộc và bàn giao khi hết lưu lượng

Chọn thư mục local riêng, ví dụ `qa-artifacts/f02/<timestamp>/`; kiểm ignore trước lưu log/screenshot. Tài liệu sạch có thể ở `docs/handover/f02-qa/` trên nhánh được phép; không commit dữ liệu nhạy cảm vào public repo.

Tối thiểu phải có:

1. `00-START-HERE.md`: bản đang QA, cách chạy, link local, trạng thái chung, đọc tài liệu nào tiếp.
2. `01-CONTEXT-AND-SOURCE.md`: repo/refs/fullSHAs, owner đang làm, trạng thái dirty, source config/database, mapcallpaths và quyết định auth/adminpair hiện hành.
3. `02-TEST-MATRIX.md` hoặc `.csv`: toàn bộ ID trên với actual/status/evidence; không bỏcase FAIL/NOT_RUN khỏi tổng.
4. `03-FINDINGS.md`: lỗi đã tái hiện, severity, bước lặp lại, expected/actual, path/line, fix/owner/test; các nghi vấn chưa xác minh tách riêng.
5. `04-RUN-RESULTS.md`: lệnh có thể chạy lại, môi trường, exit codes/counts/loglinks; phân harness/productionwiring/SQLite/MySQL/browser/Zalo.
6. `05-HUY-MANUAL-TEST.md`: link thật và checklist ngắn tại mục14.
7. `06-RESUME-HANDOVER.md`: file bàn giao sống cho Codex tiếp tục, cập nhật sau mỗi mốc lớn và TRƯỚC khi gần hết lưu lượng.
8. `evidence/`: log/screenshots/redactedresponses; dữ liệu fixture không có thông tin cá nhân thật.

Nội dung tối thiểu của `06-RESUME-HANDOVER.md`:

```markdown
# F02 — tiếp tục từ đây
- Mốc giờ UTC+7:
- Repo / nhánh bàn giao / exact HEAD / main SHA:
- Worktree path và dirty files (file nào của ai):
- Agent triển khai còn làm hay đã bàn giao; điều phối đã thống nhất:
- Đã kiểm gì: ID → PASS/FAIL + bằng chứng:
- Lỗi tái hiện còn mở, ưu tiên cao nhất:
- Đã sửa gì: commit/patch path, test fail-trước/pass-sau:
- Phần CHƯA RUN hoặc đang chạy: command + session/process ID + cách đọc output:
- Server: frontend URL/PID/cwd/SHA, backend URL/PID/cwd/SHA:
- DB test: engine/path/schema, fixture marker, cách tạo lại không phá dữ liệu:
- Tham số env cần thiết (tên, cách cấp; không giá trị secret thật):
- Công việc 1–3 bước tiếp theo, tiêu chí xong mỗi bước:
- Owner/blocker cần phối hợp, phần tuyệt đối không đụng:
- Trạng thái remote push/PR/deploy: nêu rõ cái nào CHƯA làm:
```

Nếu môi trường cloud sẽ mất khi hết quota, chuẩn bị runner/fixture sạch và hướng dẫn tái tạo, không chỉ đưa URL tạm. Gói báo cáo/patch sạch để Huy tải được nếu công cụ cho phép. Không hứa tự làm tiếp sau khi phiên bị dừng.

## 16. Điều kiện dừng và lời nhắn cuối cho Huy

Không dừng sau bước đọc repo/viết test plan. Phải thực thi phần có thể làm được. Không kéo dài vì polish khi đã có lỗi blocker rõ mà chưa báo. Cập nhật ngắn khi có phát hiện hoặc thay đổi kết luận.

Hoàn tất một lượt QA khi đã có:

- Baseline mới nhất được xác định và kết quả gắn exactSHA/artifact.
- Coreflow thực tế HS/PH trên frontend MiniApp +backend thật được chạy, hoặc blocker tái hiện rõ ngăn bước nào.
- Ma trận ghi đủ PASS/FAIL/BLOCKED/NOT_RUN, quyền và trạng thái cạnh tranh đã được xem xét.
- Lỗi có regression/fix theo đúng owner hoặc báo cáo/patch đủ rõ để agent triển khai sửa.
- URL local đã xác minh cùng checklist để Huy thử và handover để Codex tiếp tục.

Tin nhắn cuối cho Huy ngắn gọn:

1. “F02 hiện đạt/chưa đạt những đầu ra nào” — không chỉ số test.
2. Link mở thử và3–8 thao tác chính.
3. Lỗi còn mở/giới hạn môi trường, ai cần làm gì.
4. Link báo cáo và `06-RESUME-HANDOVER.md`.
5. Xác nhận không merge main, không deploy production; trạng thái push thật nếu có.

**Bắt đầu ngay bằng việc xác định bản bàn giao mới nhất, đọc quy tắc/source liên quan, rồi chạy smoke qua giao diện và API thật. Ưu tiên chứng minh người dùng nhận được đúng đầu ra F02, không ưu tiên làm đẹp báo cáo.**
