# Kiểm thử lại đầu nhánh F07 — 18/10/2026

**Kết quả: chưa đạt để bàn giao nghiệm thu như người dùng bình thường. R01–R06 vẫn còn mở.**

Người dùng xác nhận lấy bản mới nhất đang có trên nhánh F07 làm chuẩn. GitHub branch và PR #42 đều được kiểm tra lại, cùng trỏ tới `bb75b2cee314bd5dfea3fff7928664dc68d3e2dd`. Đây là bản mới nhất quan sát được, không suy đoán coding agent có commit khác. Mốc kiểm refs và thời gian hoàn tất log ở [PROVENANCE.json](PROVENANCE.json).

Đã chạy lại đúng các kiểm tra cần để đối chiếu 6 finding, với source ứng dụng giữ nguyên:

| Kiểm tra mới | Kết quả | Bằng chứng |
| --- | --- | --- |
| Regression MySQL R02/R03/R05 | 3 tổng, 3 FAIL | [mysql-regressions.log](mysql-regressions.log) |
| MySQL create race R04 | 1 tổng, 1 FAIL | [mysql-create-race.log](mysql-create-race.log); lỗi assertion thứ tự, không phải duplicate row |
| Browser R01/R06 | 9 quan sát, 4 PASS + 5 FAIL | [browser-review.log](browser-review.log), [JSON](browser/browser-results.json) |

R02 vẫn quan sát `final_revision=2 unapproved_readable=True`; R03 vẫn chỉ liệt kê 1 trong 2 mục đọc được; R05 ngày có hậu tố sai vẫn trả HTTP 201. Browser vẫn giữ preview khi navigation/xóa phiên; CSS text scaling 200% vẫn làm content width thành 395px ở viewport 320/390.

Không chạy lặp full suite trên cùng SHA không đổi. Số 523/307/227 và các suite khác trong báo cáo trước là kết quả của lượt review trước, không gán thành kết quả mới của lượt này. Không kiểm production hoặc Zalo thiết bị thật.

## Hành động tiếp theo

Coding agent sửa ứng dụng trên nhánh F07 theo [prompt mới nhất](../PROMPT-NEXT-AGENT.md), dùng [FINDINGS.md](../FINDINGS.md) và tests tái hiện hiện có. Sau sửa cần commit/push SHA mới, chạy lại kiểm tra và hoàn tất [điều kiện bàn giao cho người dùng](../READY-FOR-USER-TEST.md).

Đây là xác nhận lại tình trạng hiện tại, không phải một bộ lỗi mới hay bằng chứng các bản sửa đã được thực hiện. Bằng chứng review lần đầu vẫn giữ ở `../evidence/`.
