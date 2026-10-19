# Synthetic probes — không chạy trên production

Đây là script audit ngoài source ứng dụng, không phải chức năng product. Provider trong browser E2E là `LOCAL_SYNTHETIC_PROVIDER`, các tài khoản chỉ là fixture. Không commit/copy `.synthetic-credentials.json`, DB hoặc file môi trường.

Tạo snapshot riêng từ SHA muốn kiểm tra, không dùng DB/checkout dev chứa dữ liệu của người dùng. Đặt `F04_AUDIT_DIR` tới thư mục thử và đặt snapshot code ở `$F04_AUDIT_DIR/source`. Venv ở `$F04_AUDIT_DIR/venv`. Cài dependencies theo lockfiles, migrate DB SQLite của snapshot, rồi chạy các script bằng venv đó.

```bash
export F04_AUDIT_DIR=/tmp/f04-audit
# source/ phải là bản chụp đã ghim SHA và dùng dữ liệu tổng hợp
python repro/independent_backend_probe.py
python repro/probe_claim_reuse.py
```

Hai probe Python dùng feature-lab và DB test tự tạo/hủy. Probe claim-reuse dự kiến FAIL ở e0ee388; nó dựng thứ tự giao nhau xác định qua service claim thật, không tuyên bố đã chứng minh row locking MySQL.

Browser scripts cần Chromium + Playwright. Đặt `F04_PLAYWRIGHT_MODULE` và `F04_CHROMIUM` theo máy nếu khác default. Chạy helper chuẩn bị fixture, backend audit và Vite ở cổng 8044/5144/3044 đúng như script; đọc script trước để biết state và điều kiện đầu vào. `browser_e2e.mjs` rồi `browser_layout_and_control.mjs` tạo các fixture được `preview_race.mjs` dùng tiếp. Không chạy cùng script nhiều lần trên DB đã đổi state mà bỏ qua phần chuẩn bị.

Scripts giữ output trong `$F04_AUDIT_DIR/evidence`. Các payload/ảnh chỉ chứa marker tổng hợp. Chỉ provider AI là fake; browser dùng HTTP adapter và Django/F05 thật. Không suy kết quả này thành Gemini live, deployment Render hoặc Zalo Android/iOS.
