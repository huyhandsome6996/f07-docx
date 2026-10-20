# F15 Quyền riêng tư thu hồi và yêu cầu xóa dữ liệu

**US:** US-012, US-017, US-023. **PR:** https://github.com/huyhandsome6996/family-bridge/pull/33

## Đầu vào và đầu ra

Đầu vào: phiên F01/F16 hợp lệ, dữ liệu/grants thuộc actor, đối tượng/recipient/revision được chọn, ý định unlink/withdraw/xóa và policy/capability người xử lý phù hợp.

Đầu ra: người dùng biết chính xác đang chia sẻ gì với ai; thu hồi từng mục; hủy kết nối; rút từng purpose consent; gửi yêu cầu xóa có biên nhận/trạng thái tiến trình trung thực. **Gửi yêu cầu không phải đã xóa hoàn tất**, không hứa purge mọi backup/provider khi chưa có kiểm chứng/policy.

## UI cần đạt trên cả hai client

`#/privacy` là điểm vào nhất quán từ profile/settings. Có overview chia sẻ/consent/Connection; liệt kê từng item thuộc actor và trạng thái approved/stale/revoked; xác nhận thu hồi/hủy kết nối; lựa chọn category trước yêu cầu xóa, biên nhận, xem trạng thái/cancel khi được phép. Nhánh F15 có `/privacy-items` cho thao tác item; giữ route hoặc điều hướng tương đương rõ ràng, không để chỉ Mini có còn website chỉ shell cũ.

Màn người dùng không hiển thị admin verification/process như nút tự nhận đã xác minh. Người xử lý có capability đúng scope/TTL mới dùng nghiệp vụ. Thiếu cơ chế/policy phải hiển thị pending/failed-needs-action trung thực, không điền pass mặc định.

## Bối cảnh tích hợp rủi ro cao

F15 head aeae321 đang xa main (63 commit main ngoài nhánh ở snapshot này); báo cáo review-ready cũ không phải nghiệm thu với HS/PH/admin-pairs/shared API mới. Không checkout theirs toàn bộ session/router/profile để lấy feature, vì sẽ làm mất các thay đổi mới hơn.

Đọc `docs/features/f15/api.md`, `report.md`, `pilot-2026-10-14.md`, `two-account-script.md`, services wiring/adapters/ports/deletion/consent/verification và restore tests tại snapshot F15. Đọc song song main hiện hành F16/session/core wiring/F10–F13 và nhánh F07/F04 consumers.

## Bất biến không được mất khi resolve

- Session HS/PH dùng UUID nội bộ; logout/expiry/disabled user và service withdrawal có hiệu lực đúng luồng. Không rơi về import resolver F01 sai hoặc chỉ hỗ trợ token Zalo cũ.
- Mutation revoke/unlink và ledger cùng transaction; owner, item-type, recipient, approved revision và connection ID/generation đúng. Lặp idempotent; không hồi sinh grant cũ.
- Withdraw theo purpose: AI không tắt service tùy tiện, research không khóa app, service vẫn không khóa help. F01/F14 state không mâu thuẫn; không timestamp/UUID resurrect accepted consent cũ.
- Deletion: scope/categories và cutoff được chốt, retry không nới phạm vi hoặc xóa mục tạo sau cutoff; phase/checkpoint chịu crash; missing hook là failed-needs-action, không báo completed.
- Restore: replay latest revoke/deletion ledger trước serve, thiếu provider/hook/cutoff malformed phải fail-closed; watermark/sequence bounded; replay không tự thêm event hay tái kích hoạt account/share.
- Handler phải pass authorizer thật, không bool client hoặc is_staff; note/journal/AI không là dữ liệu admin mặc định.

## Công việc cần hoàn thiện

1. Ghép sessions.py với main mới, bảo toàn F16 class-session và current F01 behavior. Test login HS/PH/revoke/logout với tất cả bốn feature.
2. Ghép F07 mood service với bản 3fe66cd; thống nhất hook/provider registration và startup order. Đừng có hai đường revoke khác nhau hoặc adapters đọc khác grants.
3. Nối hook AI F04 và progress F02 nếu domain/policy hỗ trợ. Không coi hook chưa có là đã xóa; nếu chưa được chốt retention phải ghi rõ external/policy gate và không bật destructive processing giả.
4. Website phải có đầy đủ thao tác tương đương Mini App (không chỉ overview), same API và response state. Không import UI mini vào web; shared page-core chỉ dùng nếu headless thật.
5. Update hợp đồng/negative/race/restore tests theo cùng source tích hợp; xử lý stale 409, cursor và limits. Query/payload bounded, không full-history scan trên mỗi revoke/list.

## Gate riêng F15

Merge code: session/grant/ledger/deletion/restore tests trên backend thật và MySQL cho transition/concurrency có tác động; UI hai client rõ request-vs-completed và guard. Release xử lý dữ liệu thật: policy retention, authority, operator, backup restore, provider deletion và bằng chứng postcondition cần được chốt. Không tự giải quyết phần OPEN bằng số ngày tùy ý hoặc account deletion flag.
