# F07 Tâm trạng lịch sử và chia sẻ từng mục

**US:** US-015, US-026. **PR:** https://github.com/huyhandsome6996/family-bridge/pull/42

## Đầu vào và đầu ra

Đầu vào: phiên HS/PH, mã cảm xúc allowlist, ghi chú có giới hạn, ngày do server theo chính sách VN, revision của mục và người nhận primary ACTIVE nếu chia sẻ.

Đầu ra: ghi nhận/sửa tâm trạng riêng tư, đọc lịch sử, chọn một mục và một người để preview/chia sẻ, xem/thu hồi grant; người nhận chỉ đọc revision được chia sẻ còn hiệu lực. Không tự share sau lưu hoặc sửa, không mở lịch sử riêng vì đã ghép cặp.

## Các màn phải có trên cả website và Mini App

- `#/mood`: editor tạo/sửa, emotion và note, lịch sử có cursor, trạng thái đang sửa đúng mục, share preview và quản lý grant.
- `#/mood-shared`: danh sách mục mình được chia sẻ, chi tiết authorized; trạng thái khi stale/revoked/unlinked.
- Đường vào từ home/profile. Chưa có Connection vẫn ghi riêng tư được; kết nối chỉ là điều kiện của sharing.
- Sheet lỗi nằm trong sheet đang thao tác; keyboard/focus, 320/390/430px, text scaling và desktop không tràn/cắt nhãn.

## Thứ tự đọc evidence và tránh sửa theo finding đã lỗi thời

Root `updates/2026-10-19-f07-final-audit/` audit **2ffd674** và nêu R08–R10 còn mở tại mốc đó. Head nhánh hiện tại **3fe66cd** có bản sửa và regression cho ba finding này, mô tả tại `source-reference/f07/docs/handover/f07-mood-sharing/verification-report.md`. Vì thế trạng thái hiện hành là **FIX_REPORTED_NEEDS_INTEGRATED_RETEST**, không tự ghi vẫn lỗi hoặc đã nghiệm thu cuối.

Giữ đầy đủ R01–R10/X01–X10: edit-race revision không mất update, schema field rõ, cursor/page-size đúng, note không lộ sau revoke/reconnect, lexical date validation toàn chuỗi, cleanup private DOM/sheet khi actor đổi, parity web/Mini, editor giữ entry_id sau save, nút Tải thêm thật sự hidden và có guard khi hết cursor, lỗi 409 hiển thị trong sheet có đường xem lại bản mới.

## Công việc cần kiểm sau ghép F15/main

1. F07/F15 dùng cùng nguồn grants, provider và connection-generation; không để last-registration-wins làm mất cutoff/revocation ledger của F15 hoặc guard revision của F07.
2. Tạo entry rồi lưu tiếp ba lần không remount: POST một lần rồi PATCH cùng ID; sửa ngày cũ không âm thầm tạo mục hôm nay. Lỗi giữ nháp; backend vẫn một mục/ngày.
3. History và shared-list: nhiều trang, trang cuối, retry/double-click, dedup IDs, không request first page lặp khi cursor null, nút không focus/click được khi hidden.
4. Mở share preview trên web, sửa note/revision trên Mini rồi xác nhận web: 409 đúng, không grant bản mới; lỗi nằm TRONG dialog; xem lại mới là GET, không auto-share. Chạy chiều ngược lại.
5. Share → PH đọc từ cả hai client → revoke qua F15 → cả list/detail/DOM cũ bị chặn/gỡ. Unlink/reconnect generation mới không mở grant cũ. Provider thiếu phải fail-closed.
6. Logout/late response khi PH đang xem chi tiết, sau đó login actor khác: kiểm cả note VÀ revision không lộ. Dùng fixture riêng cho unlink/reconnect; không dùng pair đã revoke cho case kế tiếp.
7. X07/X10 và các NOT_RUN không được cộng PASS. Bằng chứng MySQL cũ trong nhánh ghi rõ phiên bản/chạy ở đâu, không thay test tích hợp sau merge.

## Gate riêng F07

Qua backend thật với F01/F15, MySQL race cho create/share/edit, browser thật hai client cho R08–R10 và hai chiều sharing, routing/build/keyboard/cleanup. Device Zalo là gate phát hành Mini App riêng, browser mô phỏng không thay device thật. Không chỉ dùng source CSS pin/happy-dom để kết luận reflow/focus đạt.
