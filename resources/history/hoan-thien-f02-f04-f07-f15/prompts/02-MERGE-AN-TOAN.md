# PROMPT GIAI ĐOẠN MERGE AN TOÀN SAU HOÀN THIỆN

Bạn là lead/release reviewer của Family Bridge. Huy muốn đưa phần hoàn thiện F02/F04/F07/F15 vào main của https://github.com/huyhandsome6996/family-bridge sau kiểm chứng. Đây không phải lệnh merge mù bốn tip hiện có. Không làm mất phần F10–F13/admin/HS-PH đã vào main hoặc công việc người khác.

## 1. Xác nhận nguồn và phạm vi

Đọc bộ tổng hợp tại repo f07-docx, nhánh `tai_lieu_hoan_thien_F02_F04_F07_F15_docx`, tài liệu 00–09 và prompt hoàn thiện. Fetch main/bốn feature/integration, đọc AGENTS hiện hành, status/worktree/PR/CI/review. Ghi full SHA main, F02 #39, F04 #40, F07 #42, F15 #33 và integration đã review. PR có thể đã đổi/đóng; kiểm branch/head mới, không tạo PR trùng hoặc đóng PR không liên quan.

Các mốc a64f653/e38688c/d33b250/3fe66cd/aeae321 trong bộ này là source snapshot, không phải SHA bắt buộc dùng nếu repo tiến. Không reset hoặc force về chúng.

## 2. Kiểm gate trước hành động

Chỉ chuyển MERGE_READY khi đồng thời:

- Cây thực sự ghép đủ bốn feature, UI web/Mini không placeholder ở phần đã giao; HS/PH prelinked, private data và consent giữ đúng.
- Conflict resolved từng hunk và semantic review vùng shared/session/provider/wiring/router/CSS/migrations đã ghi rõ. Không còn unresolved merge marker hoặc P1/P2 chưa xử lý.
- Tests/cross-client/browser/negative/race/migrations trên chính SHA tích hợp đạt, MySQL bằng chứng phù hợp thay đổi. F10–F13/main canary không regression. Required CI/branch protection checks green trên đúng head.
- Review độc lập có kết quả dựa trên diff/test thật. Không coi PR title/body cũ hoặc green check của commit khác là approval.
- Final diff không unrelated code, secret, .env/DB, re-enable SDK login, auto-consent, auto-share, quyền admin rộng hơn.
- Có release plan vì main có thể auto-deploy web. Backend/schema/client tương thích, flags chưa sẵn mặc định an toàn, rollback giữ dữ liệu và revoke/deletion ledger.
- Scope/quyền merge của phiên hiện hành áp dụng cho đúng bốn feature. Huy đã giao hoàn thiện rồi merge khi đạt gate; không hỏi lại cho bước đã được ủy quyền, nhưng không bypass bảo vệ hoặc thao tác ngoài scope.

Nếu còn điều kiện chưa đạt: KHÔNG MERGE. Ghi FAIL/BLOCKED chính xác, fix phần thuộc scope, rerun checks bị ảnh hưởng; không đổi gate/test để xanh. Không giả tạo key, nội dung published, consent hoặc nhân sự để đóng blocker release.

## 3. Chọn đường merge có truy vết

Ưu tiên PR tích hợp từ nhánh đã ghép và kiểm đầy đủ, vì bốn nhánh có nhiều file shared và bản F15 xa main. PR description nêu bốn source heads, resolution commits, tổng diff, tests môi trường, migration/release plan. Không nhấn Merge từng PR gốc theo thứ tự tùy tiện rồi coi bằng chứng tích hợp trước đó còn hiệu lực.

Nếu quy trình nhóm chọn merge từng PR gốc: dựng và kiểm chuỗi trạng thái main tương ứng, cập nhật base và reconcile các patch đã có để tránh duplicate; review lại mỗi head sau resolve, chạy canary sau từng merge và full suite cuối. Không merge trung gian biết chắc làm hỏng auth/privacy/wiring.

Không bật auto-merge khi branch còn người đang push hoặc bỏ qua expected head. Không rebase/force các nhánh public của contributor để dễ merge. Không merge W036/consent/CI ngoài scope hoặc xóa nhánh/đóng PR khác nếu chưa được giao.

## 4. Thực thi cuối có chống race

1. Ngay trước merge, fetch và đọc main/head/CI mới. Nếu approved head hoặc base đã đổi, xem diff mới, tái tích hợp và chạy lại checks cần thiết; không sử dụng kết quả cũ.
2. Dùng GitHub merge action với expected approved head SHA nếu connector hỗ trợ; giữ required review/checks/protection, không admin bypass. Đối với cập nhật ref, chỉ fast-forward có expected old SHA; không force push main.
3. Sau merge, lấy main SHA từ GitHub và Git remote để xác nhận kết quả. Xác minh cây final chứa đủ source intentions, routes/shared methods không thiếu, migrations graph đúng và CI sau merge đạt.
4. Không báo “đã merge” chỉ vì API request được nhận hoặc PR có merge_commit_sha dự kiến. Phải thấy trạng thái merged/main thực tế và SHA tương ứng.
5. Nếu kiểm sau merge phát hiện regression: thông báo, khoanh vùng và revert/restore artifact có kiểm soát theo runbook; không reset lịch sử main, drop DB hoặc bỏ revoke/deletion records.

## 5. Deploy và trạng thái bàn giao

Merge code không tự là release ready. Ghi riêng Render auto-deploy thực tế có chạy không, SHA artifact/backend và flags; deploy thủ công/Zalo release chỉ khi được giao quyền cho đúng kênh. Không dùng localhost container làm URL Huy truy cập. Nội dung F02 published, Gemini live/retention, operator deletion và Zalo device có thể là gate release riêng; liệt kê status đúng thay vì báo mọi feature hoàn tất.

Bàn giao tối thiểu: PR/commit URLs, main before/after, source head map, conflict decision log, tests/env/PASS/FAIL/SKIP/NOT_RUN, UI routes hai client, blockers code/release, rollback/data-safety, hướng dẫn Huy thử. Lưu báo cáo tại nhánh docs tổng hợp, không đưa dữ liệu người thật hoặc credentials vào repo công khai.
