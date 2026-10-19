# F02 — Kiểm thử độc lập ngày 19/10/2026

**Kết luận: chưa đạt để chốt F02 hoàn chỉnh.** Luồng cơ bản chạy được, hai lỗi lần trước đã có regression pass; kiểm thử thêm phát hiện bốn lỗi runtime mới, hai khoảng trống Mini App và một khoảng trống web.

Nguồn ứng dụng: [family-bridge](https://github.com/huyhandsome6996/family-bridge), nhánh `tinh-nang/f02-dong-hanh-bon-tuan-us036-us044`, exact SHA **c29469b3d57f2c2cc53fe686fe7ec8f917f2dec6**. Main tại lần fetch: `ee1346a32bb5adaee7fdb7e842fceb7b9b8c32d0`. Working tree QA là detached checkout riêng, không sửa mã ứng dụng.

Kho lưu tài liệu: [f07-docx, nhánh F02-docx](https://github.com/huyhandsome6996/f07-docx/tree/F02-docx). Main của kho tài liệu dành cho F07 và được giữ nguyên.

## Đọc tiếp

- [Prompt copy cho chat coding](../../../PROMPT-COPY-F02.md).
- [Phát hiện và tiêu chí sửa](FINDINGS.md).
- [Kết quả tests, môi trường và giới hạn](TEST-RESULTS.md).
- [Đầu ra nghiệp vụ và checklist nghiệm thu](ACCEPTANCE.md).
- [Tiếp tục công việc](RESUME-HANDOVER.md).
- [Bằng chứng HTTP](evidence/http-results.json), [probe phiên bản](evidence/version-results.json).
- [Giao diện trước tham gia](evidence/01-before-enroll.jpg), [sau tham gia](evidence/02-enrolled.jpg), [tiến độ đã lưu](evidence/03-progress-saved.jpg), [390px](evidence/05-mobile-390.jpg).

## Đã chạy

| Nhóm | Kết quả trên đúng bản QA |
| --- | --- |
| Backend harness F02 + F09 + admin provisioning | 68/68 pass, SQLite |
| Mini App suite | 318/318 pass |
| Shared + F02 mobile | 38/38 pass |
| Web suite | 231/231 pass — không chứng minh trang F02 web hoàn chỉnh |
| Mini App build + verify assets/manifest | PASS |
| Web build / import boundaries | PASS / PASS |
| HTTP thật qua backend startup wiring | 44 pass, 2 fail trong46 assertion |
| Probe bổ sung sau thao tác UI | 3/3 assertion fail, tương ứng2 lỗi về phiên bản |
| Giao diện Mini App thật trong browser | Login HS903, service consent fixture, home, enroll, 4 tuần, mời, lưu tiến độ, đề xuất thỏa ước đã thao tác; có DOM/ảnh |
| Database check / migration diff | check sạch; No changes detected; 0001/0002 đã apply trên DB mới |
| MySQL/TiDB, Zalo Android/iOS thật | NOT_RUN |

Chỉ nội dung/tài khoản synthetic trong DB SQLite local được dùng. Chưa chứng minh nội dung đã được thầy duyệt/publish trên Render hoặc100 tài khoản thật đã active. Không merge main, không push ứng dụng, không deploy hay chạm DB production trong lượt này.

## Các ưu tiên

1. R01 sai revision hoạt động khi có nhiều bản published.
2. R02 thỏa ước bị kẹt sau đổi program revision mà agreement template giữ revision.
3. R03 lời mời F09 vẫn accept được sau unlink.
4. R04 thời gian confirmed_at lấy chữ ký đầu.
5. R05 chưa đọc được hướng dẫn trước enrollment; R06 thiếu nội dung chi tiết hoạt động.
6. R07 trang web F02 vẫn là placeholder, nếu nghiệm thu F02 trên web thì chưa đạt.

R01–R07 ở đây là mã phát hiện **F02 QA 19/10**, không phải R01–R07 của F07 hay R1–R4 của audit F02 cũ.

## Cập nhật 19/10/2026 — các phát hiện đã được xử lý

Bản sửa + kiểm lại theo FINDINGS của vòng này: [../2026-10-19-e113887/README.md](../2026-10-19-e113887/README.md) (nguồn ứng dụng head `e113887`, cha là đúng SHA `c29469b…` đã QA ở vòng này). Bằng chứng của vòng cũ giữ nguyên không đổi.
