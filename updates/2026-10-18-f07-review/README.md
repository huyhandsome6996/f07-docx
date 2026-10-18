# F07 — kết quả kiểm tra độc lập sau coding agent

Ngày: 18/10/2026. Nhánh: `tinh-nang/f07-tam-trang-va-chia-se-us015-us026`.

**Chưa đạt nghiệm thu toàn bộ. Có 6 finding còn mở, trong đó R01 và R02 ảnh hưởng riêng tư.** Không merge/deploy dựa trên bảng PASS trong bàn giao cũ.

- Commit đã kiểm: `bb75b2cee314bd5dfea3fff7928664dc68d3e2dd`.
- Main khi kiểm: `571abcb7916954964d82e0aa27e7661e7d7efd83`.
- PR được đối chiếu bằng Git remote ref: [#42](https://github.com/huyhandsome6996/family-bridge/pull/42). Không suy luận trạng thái Draft/approval từ ref này.
- Không sửa tracked source của ứng dụng trong phiên kiểm tra. Các finding cần coding agent sửa trên nhánh F07; đợt này cập nhật kho tài liệu và bộ tái hiện.

## Đọc theo thứ tự

1. [FINDINGS.md](FINDINGS.md): 6 lỗi/thiếu sót, bằng chứng và tiêu chí sửa.
2. [TEST-RESULTS.md](TEST-RESULTS.md): kết quả mới, lệnh và giới hạn môi trường.
3. [ACCEPTANCE.md](ACCEPTANCE.md): đối chiếu lại 25 tiêu chí F07.
4. [repro/README.md](repro/README.md): chạy bộ tái hiện trước/sau sửa.
5. [PROMPT-NEXT-AGENT.md](PROMPT-NEXT-AGENT.md): prompt đầy đủ để copy.

## Thành phần

- `evidence/`: log kiểm thử mới và screenshot dữ liệu synthetic. `browser/` chứa ảnh viewport 320/390/430 và phóng chữ CSS 200%.
- `repro/`: kiểm tra bổ sung dùng Django test database và browser local. Các test đỏ là phát hiện cần sửa, không phải test được đánh dấu expected-failure để làm xanh báo cáo.
- `branch-snapshot/`: đúng 46 tệp tracked thay đổi từ main đến commit F07, gồm handover của coding agent và ảnh của họ. Đây là tham chiếu từng phần, không phải checkout để chạy hoặc chép đè.
- `BRANCH-FILES.json`: SHA-256 từng tệp trong snapshot nhánh.
- `PROVENANCE.json`: refs, phạm vi, runtime và Docker image digest.

Tài liệu trong `branch-snapshot/docs/handover/f07-mood-sharing/` được giữ nguyên để đối chiếu tuyên bố cũ. Kết quả mới ở thư mục này thay thế các tuyên bố PASS rộng hơn đối với cùng commit. ZIP 00 và các gói 01–09 vẫn là bàn giao lịch sử; không bị viết lại.

## Cách lấy từ ZIP

Từ gốc repo `f07-docx`, chạy:

```bash
python3 tools/bundles.py verify
python3 tools/bundles.py extract 10 --dest /tmp/f07-review-reading
```

Sau đó đọc `updates/2026-10-18-f07-review/README.md` trong thư mục đích. Đọc gói 10 trước khi dùng nhiệm vụ lịch sử trong gói 01. Việc đọc chỉ dẫn bên trong ZIP không tự cấp quyền merge, deploy hoặc thay đổi dữ liệu thật.
