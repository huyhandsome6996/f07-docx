# F07 — kiểm thử độc lập đầu nhánh mới 2ffd674 (19/10/2026)

**Kết luận: CHƯA ĐẠT gate bàn giao để Huy nghiệm thu như người dùng bình thường.** Web đã có F07 gọi cùng backend với Mini App; các regression R01–R07 được kiểm lại và không còn tái hiện trong phạm vi bên dưới. Ba lỗi UI mới R08–R10 còn mở trên CẢ HAI client, kèm khoảng trống bằng chứng nghiệm thu.

Mã kiểm tra: `2ffd674243c5063f95123010498bc9cc60cf441e`, nhánh `tinh-nang/f07-tam-trang-va-chia-se-us015-us026`, [PR #42](https://github.com/huyhandsome6996/family-bridge/pull/42). Đây là commit MỚI sau bb75b2c; không tiếp tục coi R01–R07 còn lỗi chỉ vì báo cáo trước.

Đọc theo thứ tự:

1. [Finding hiện hành và tiêu chí sửa](FINDINGS.md): R08 lưu liên tiếp sai POST/PATCH; R09 hết trang vẫn tải lại/nhân bản; R10 lỗi share nằm sau modal.
2. [Kết quả kiểm thử và giới hạn](TEST-RESULTS.md): phân biệt PASS/FAIL/SKIP/NOT_RUN, bằng chứng mới gắn đúng SHA.
3. [Gate và checklist Huy](READY-FOR-HUY.md).
4. [Quy tắc làm việc/báo cáo](REVIEW-RULES.md).
5. [Prompt đầy đủ](PROMPT-NEXT-AGENT.md), giống bản [ở gốc](../../PROMPT-COPY-F07.md).
6. [Chạy repro UI](repro/README.md), log/JSON/ảnh trong `evidence/`, nguồn tham chiếu trong `source-reference/`.

Gói ZIP **12** chứa toàn bộ cập nhật này. Đọc 12 trước; yêu cầu hai UI/API trong gói 11 vẫn áp dụng, gói 10 lưu regression R01–R06 cần giữ. Các gói cũ là lịch sử, không chép đè lên source ứng dụng.

Chỉ sửa/push repo tài liệu `f07-docx/main` trong đợt review này. Reviewer không sửa source ứng dụng, không merge/deploy, không tạo tài khoản thật. Dữ liệu chạy thử đều synthetic, local. MySQL thật không thay cho Zalo Android/iOS; loopback trong container không phải URL Huy truy cập được.
