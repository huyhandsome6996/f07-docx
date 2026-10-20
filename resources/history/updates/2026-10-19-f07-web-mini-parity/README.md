# F07 — nghiệm thu web và Mini App, 19/10/2026

**Chưa đủ tiêu chuẩn để Huy nghiệm thu như người dùng bình thường. Có 7 finding còn mở: R01–R06 trước đây và R07 thiếu luồng F07 đầy đủ trên web.**

Đã kiểm đầu nhánh F07 và PR #42: `bb75b2cee314bd5dfea3fff7928664dc68d3e2dd`. Main quan sát được là `ee1346a32bb5adaee7fdb7e842fceb7b9b8c32d0`. Mốc UTC ở [PROVENANCE.json](PROVENANCE.json); ngày bàn giao dùng UTC+7. Không sửa tracked source ứng dụng trong lượt này.

## Đọc trước khi coding

1. [Quyết định mới của Huy](USER-DECISION-WEB-PARITY.md): F07 phải có UI/API thật trên cả web và Mini App. Phần cấm sửa web của bàn giao cũ được thay thế trong phạm vi F07.
2. [R07 và bằng chứng](FINDINGS-R07.md); R01–R06 chi tiết vẫn ở [review trước](../2026-10-18-f07-review/FINDINGS.md).
3. [Yêu cầu, ma trận hai client và nghiệm thu chéo](REQUIREMENTS-AND-ACCEPTANCE.md).
4. [Kết quả kiểm thử mới](TEST-RESULTS.md).
5. [Prompt đầy đủ](PROMPT-NEXT-AGENT.md) và [cách chạy repro](repro/README.md).

## Kết luận chính

- R01/R02 còn ảnh hưởng riêng tư; MySQL vẫn tái hiện unapproved content ở cùng revision sau concurrent edit.
- Web đăng nhập và adapter gọi API thật được. Web có quick mood card trên trang chủ, nhưng thiếu `/mood`, `/mood-shared` và navigation F07. Đây là thiếu UI chức năng, không phải thiếu toàn bộ API/adapter web.
- Browser: hai route web đều hiện trang không tìm thấy; Mini App có các route tương ứng.
- Mini App 307 tests PASS, web 227 tests PASS và hai build PASS trong lượt này; các kết quả đó không bao phủ parity F07 và không phủ định regression mới.
- MySQL regression 3/3 FAIL, create-race assertion FAIL, Mini lifecycle/text scaling 5/9 FAIL, parity smoke 3/12 FAIL.

## Đóng gói

Gói 11 bổ sung tài liệu yêu cầu mới, test/ảnh/log và source-reference có chọn lọc. Gói 10 vẫn giữ review/recheck cũ; 00–09 giữ bản gốc.

```bash
python3 tools/bundles.py verify
python3 tools/bundles.py extract 11 --dest /tmp/f07-current-reading
python3 tools/bundles.py extract 10 --dest /tmp/f07-current-reading
```

Đọc `updates/2026-10-19-f07-web-mini-parity/README.md` trước. Snapshot là tham chiếu từng phần tại SHA đã kiểm, không phải checkout để chạy/chép đè. Scripts trong ZIP không được tự thực thi bởi công cụ giải nén.
