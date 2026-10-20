# Quy trình tích hợp và xử lý xung đột

## Bằng chứng mới tại main a64f653

Đã chạy `git merge-tree --write-tree --name-only` cho main với từng head và sáu cặp feature; không checkout/commit/merge ứng dụng. Cả mười phép đều có textual conflict (exit 1). `evidence/branch-and-conflicts.json` là bản máy đọc đủ SHA/file; chưa chạy thử runtime trên một cây hợp nhất và chưa giải bất kỳ conflict nào. Git merge sạch cũng không bảo đảm đúng nghiệp vụ.

| Nhánh vào main | File conflict thực tế ở snapshot |
| --- | --- |
| F02 | shared `contract.js`, `http-endpoints.js`, `mock-adapter.js`; shared tests `http-endpoints.test.mjs`, `purity.test.mjs` |
| F04 | `web/src/styles/components.css` |
| F07 | hai shared tests trên; `web/tests/router.test.mjs` |
| F15 | `.gitignore`; F15 `services/sessions.py`; Mini App `privacy/index.js`, `profile/index.js`, `tests/pages.test.mjs` |

F07 ↔ F15 còn conflict trực tiếp tại `f07_mood/services/mood.py`. F02 ↔ F07 trùng adapter contract/endpoints/mock và tests; F04 ↔ F07 trùng endpoints và CSS. Danh sách file giao nhau KHÁC danh sách Git conflict: file auto-merge vẫn cần semantic review.

## Một lead chịu trách nhiệm vùng dùng chung

| Vùng | Ý định cần giữ và phép kiểm |
| --- | --- |
| Shared adapter/contract/mock | Hợp tất cả method F02/F04/F07/F15 VÀ F10–F13 main; không trùng tên hay shape; kiểm request thật, không chỉ đổi số method expected |
| F01/F16/session | HS/PH login + stable UUID + revoked/disabled/TTL/generation; không import sai đường hoặc fallback bypass |
| F07/F15 provider/hook | Một nguồn grants/revoke ledger, current revision + connection generation; kiểm provider không bị ghi đè theo thứ tự startup |
| F04/F06 compose | expected_revision/recipient binding/preview snapshot/optional pause; gửi text qua F05 đúng transport |
| F02/F09 | primary pair, program revision pin, agreement 2 actor; provider content không bị core wiring thay thế |
| Router/nav/home/profile | Giữ mọi route cũ hợp lệ và routes mới; cả hai client đủ UI; preserve admin-provision và F10–F13 |
| CSS/components | Ghép theo scope, giữ hidden guards/a11y và stylesheet thứ tự hợp lý; không ghi đè toàn bộ CSS bằng ours/theirs |
| Migrations | Không sửa migration đã phát hành; kiểm graph/leaf mới, GeneratedField/W036 giao nhau, rollout/backfill thật |
| Tests/harness | Hợp test cases và contract semantics; không xóa assertions của contributor khác để xanh; count changes chỉ khi inventory đúng |

Không dùng `git checkout --ours .`, `--theirs .`, `git merge -X theirs`, chép snapshot cả thư mục, `--allow-unrelated-histories` hay force-push để dọn xung đột. Chỉ dùng resolution theo ý định từng hunk, giải thích trong log.

## Thứ tự tích hợp đề xuất cần xác minh lại

Đây là phương án kỹ thuật, chưa là bằng chứng đã chạy thành công: **F15 → F07 → F02 → F04** trên nhánh tích hợp tạm từ main mới nhất. Lý do: F15 đặt nền revoke/session/deletion; F07 kiểm consumer grants; F02/F09 thêm program; F04 thêm AI/F06 và hook AI. Có thể đổi thứ tự khi dependency/source mới cho thấy hợp lý hơn; phải ghi lý do và chạy lại ma trận.

Các nhánh riêng vẫn có thể sửa độc lập theo ownership. Đừng merge W036 (#34), consent (#41) hoặc thay đổi ngoài scope chỉ vì còn mở. Nếu DB constraint của phạm vi bắt buộc phụ thuộc W036, ghi dependency thật, review hướng giải riêng và xin quyết định cụ thể khi scope chưa được cấp; không âm thầm mang toàn bộ nhánh bảo trì vào. Không xóa nhánh feature hoặc PR gốc sau merge nếu Huy chưa giao.

## Các bước thực hiện

1. Fetch main và các head, ghi full SHA, dirty/worktree/PR/CI/review. Bảo toàn công việc đang chạy. Xác định ai đang sửa main/F10–F13 và khóa file shared theo người điều phối.
2. Tạo worktree tích hợp riêng, nhánh `tich-hop/f02-f04-f07-f15-an-toan` nếu tên chưa tồn tại; nếu tồn tại thì kiểm owner/state trước khi dùng. Không rebase/force nhánh cộng tác công khai.
3. Pin các head thực sự sẽ đưa vào. Trên nhánh tích hợp, merge lần lượt từng head bằng commit thông thường, giải quyết từng hunk. Có thể dùng `--no-commit --no-ff` để review trước commit; không để unresolved state rồi chạy tác vụ kế tiếp.
4. Sau mỗi phần chạy regression đúng phạm vi và canary F10–F13/F01/F16. Tạo commit resolution nhỏ rõ ý định; ghi source heads/affected invariants.
5. Khi đủ bốn phần, chạy toàn bộ gate trong `07-NGHIEM-THU-HAI-CLIENT.md` trên CHÍNH SHA tích hợp. Lấy ảnh UI/backend logs synthetic đúng SHA, loại secrets. Không dùng CI cũ của nhánh thay cho CI tích hợp.
6. Review diff tổng main…integration: không có unrelated code/deps/secret/data; migrations hợp lệ; mọi hành vi intended còn giữ. Dùng `git range-diff` khi có rebase/cherry-pick được phép để chỉ ra khác biệt, không coi patch equivalence là test.
7. Fetch lần cuối. Nếu main tiến, ghép main mới vào integration có kiểm soát và chạy lại checks bị ảnh hưởng; thay đổi session/shared/migrations thì full gate lại. Nếu feature head tiến, không tự tuyên bố bản tích hợp gồm head đó: hoặc pin bản đã kiểm và báo rõ, hoặc ghép head mới rồi kiểm lại.
8. Push integration và mở/cập nhật PR tích hợp có inventory bốn PR/head + conflict decisions. Ưu tiên một PR tích hợp được review trên cây kết hợp; nếu team chọn merge từng PR gốc, phải test chuỗi trạng thái main sau TỪNG bước, không lấy kết quả cuối che trạng thái trung gian hỏng.
9. Chỉ khi gate pass, review hoàn tất và quyền merge trong prompt hiện hành áp dụng mới merge đúng head theo `prompts/02-MERGE-AN-TOAN.md`. Expected head SHA và CI phải trùng; không bypass protections/auto-merge một đầu nhánh còn biến động.

## Gate merge và gate release khác nhau

**MERGE_READY:** cùng cây tích hợp đã test, không unresolved conflict/P1/P2 chưa xử lý, auth/privacy/races/migrations/production-wiring/UI/build/required CI đạt; default-off và lỗi honest cho các phụ thuộc bên ngoài chưa bật. Nếu thiếu MySQL để kiểm thay đổi constraint/race đang là rủi ro unresolved thì chưa merge-ready.

**RELEASE_READY:** ngoài MERGE_READY phải có nội dung published đã duyệt, key/provider/retention/operator hợp lệ, migration DB đích, deploy đúng SHA, smoke Render, testing/device Zalo và quyền phát hành kênh tương ứng. Không chờ dữ liệu vận hành bằng cách fabricate nó; không gọi merge code là hoàn tất pilot.
