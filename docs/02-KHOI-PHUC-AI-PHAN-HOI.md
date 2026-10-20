# Khôi phục AI hỗ trợ phản hồi — Family Bridge

Trích nguyên phần bổ sung AI từ báo cáo commit eaeb733a531f705954c1e3a51120531f97147d3e tại f07-docx. Đọc cùng 01-SUA-LUONG-PHAN-HOI-HS-PH.md; giữ đúng giới hạn bằng chứng.

## 9. Bổ sung yêu cầu Huy — Khôi phục AI hỗ trợ viết phản hồi êm ái hơn

Bổ sung 21/10/2026, sau khi Huy phản ánh không dùng được nút AI. Main kiểm tra lại vẫn là `7ace3dab80c2473095cdef51c0cd3b35805b4143`.

### 9.1. Yêu cầu sản phẩm

AI phải tiếp tục phục vụ người ĐANG VIẾT một phản hồi hợp lệ. Sửa R01 không được làm mất AI của người nhận:
- HS gửi M cho PH: HS không tự phản hồi M; PH mở M và được nhờ AI sửa lời PH đang soạn.
- PH gửi N cho HS: HS là người nhận, được nhờ AI sửa lời HS đang soạn.
- Người dùng viết ý ban đầu → chủ động yêu cầu AI → xem gợi ý → Dùng gợi ý hoặc Bỏ → có thể sửa tiếp → xem trước/xác nhận gửi theo contract.
- AI không tự nhập vai cha trả lời con, không tự gửi, không tự đọc thư/nguyên sổ/nhật ký để lấy ngữ cảnh.
- Không coi đường viết tay dự phòng là đã hoàn thành yêu cầu AI. Phải tìm và sửa nguyên nhân dịch vụ thật không hoạt động.

Ví dụ dữ liệu synthetic: người cha viết “Bố bực vì con về muộn.”, AI có thể gợi ý “Bố lo khi con về muộn. Lần sau con báo bố nhé.” Đây chỉ là ví dụ giao tiếp, không phải kết quả Gemini thật của reviewer.

### 9.2. Bằng chứng đọc code và probe bổ sung

Đã đọc:
- `web/src/components/ai-assist.js`.
- `zalo-mini-app/src/pages/message/index.js` (AI inline).
- `packages/family_bridge_shared/src/adapter/http-endpoints.js`.
- `packages/family_bridge_features/f04_ai/api.py`.
- `packages/family_bridge_features/f04_ai/apps.py`.
- `packages/family_bridge_features/f04_ai/services/wiring.py`.
- `packages/family_bridge_features/f04_ai/services/express.py`.
- `packages/family_bridge_features/f04_ai/services/gemini.py`.
- `backend/config/settings.py`.

Code đã có:
- Authenticated `GET /api/v1/ai/status` trả `{ai_enabled: boolean}`.
- `POST /api/v1/ai/refine`, `POST /api/v1/ai/suggestions/{id}/accept` và discard.
- Cổng consent `ai_processing`.
- Gợi ý `suggested_text` và input revision.
- UI “Dùng gợi ý” chỉ điền textarea, không gọi F05 send.

Reviewer chạy trực tiếp component web thật trong V8, thay DOM/helpers/adapter bằng doubles tối thiểu:
1. aiStatus trả false → CTA disabled, thông báo AI chưa bật.
2. aiStatus ném lỗi mạng giả lập → CTA disabled, thông báo chưa kiểm tra được trạng thái.
3. aiStatus true + consent hợp lệ + refine/accept giả lập → tạo được thẻ gợi ý, bấm “Dùng gợi ý” điền textarea và hiện ghi chú “chưa gửi”. Quan sát 1 refine call, 1 accept call.
Đây là probe logic component **web**, không phải phép thử Gemini/Render thật, cũng không chứng minh Mini AI đã chạy end-to-end.

### 9.3. Chưa xác định nguyên nhân live — phải chẩn đoán theo request thật

Không đọc được ba ảnh mới trong môi trường review; không khẳng định ảnh hiển thị lỗi nào. Không có phiên HS/PH để đọc API AI authenticated trên Render.

Antigravity dùng một tài khoản thử đã được phép và Network/log đã khử secrets, ghi route/client/deployed SHA, HTTP status + mã lỗi an toàn theo từng bước:

| Điểm kiểm tra | Nếu quan sát được | Việc cần làm |
| --- | --- | --- |
| ai/status | 401 | Sửa phiên/Authorization/expiry; không gọi đây là lỗi Gemini |
| ai/status | 403 hoặc lỗi quyền/consent theo code | Đối chiếu error code và lớp xử lý; không bỏ cổng đồng ý |
| ai/status | 200, ai_enabled=false | Kiểm startup provider wiring, flag/config, F04 registration; không ép client bật nút |
| ai/status | Timeout/network/CORS | Kiểm API base URL, backend availability và allowlist origin của từng client |
| ai/status | 200, ai_enabled=true | Chỉ chứng minh provider được wire + kill switch chưa chặn; chưa chứng minh key/model/quota thực dùng được |
| ai/refine | 403 consent_required | Đọc/ghi consent hiện hành đúng phiên bản; không đồng ý hộ |
| ai/refine | 400/409 | Kiểm DTO, revision, idempotency và conflict detail |
| ai/refine | 429 hoặc 503 | Xem mã lỗi an toàn: local limit, provider quota, auth, unavailable, timeout hoặc output invalid; không gộp thành “AI tắt” |
| ai/refine | 201 có suggested_text | Kiểm render gợi ý, revision guard và lời phản hồi đúng actor |
| accept | Lỗi/không điền textarea | Kiểm suggestion ownership, status, current input revision và callback stale |
| Sau apply | Nội dung có nhưng không gửi | Kiểm F05 preview/send riêng; AI accept không phải thao tác gửi |

Không xuất key/token, prompt/body người thật hoặc chi tiết lỗi provider có thể chứa dữ liệu riêng vào console/tài liệu. Không dùng `GET health` thay cho phép thử AI authenticated.

### 9.4. Cấu hình đúng service BACKEND trên Render

Theo code hiện hành, đây là các tên biến cần đối chiếu. Giá trị key phải được cung cấp qua secrets hiện có, không gửi vào báo cáo:

```dotenv
FB_AI_ENABLED=true
GEMINI_API_KEY=<secret-cua-moi-truong-backend>
GEMINI_MODEL=<model-da-xac-minh-con-kha-dung-va-trong-allowlist-code>
GEMINI_TIMEOUT_SECONDS=15
GEMINI_MAX_OUTPUT_TOKENS=1024
```

- Settings mặc định FB_AI_ENABLED=false khi không có biến/giá trị không đúng.
- Startup chỉ wire provider khi flag bật, key không rỗng và cấu hình hợp lệ.
- Model phải hợp lệ theo code allowlist VÀ tài khoản/provider thực tế. Không suy từ model name có trong code rằng hiện tại provider còn phục vụ model đó; kiểm nguồn Gemini chính thức trước khi thay model/allowlist.
- Nếu không có nhu cầu override model, đối chiếu default đang pin trong code với trạng thái provider hiện hành, không đoán model mới.
- Không đặt Gemini key vào biến VITE_*, web frontend hoặc Mini App.
- Thay environment trên Render cần restart/redeploy backend để Django nạp lại settings và startup wiring. Không tự mở/tạo dịch vụ mới.
- Chỉ thực hiện thay cấu hình/deploy trong quyền phiên Huy đã cấp; chưa có credential thì hoàn thành code/tests rồi báo đúng cấu hình còn thiếu, không bảo “đã bật AI”.
- Sau restart, status=true vẫn chưa đủ: chạy refine thật với nội dung synthetic được phép, kiểm suggested_text rồi accept/apply. Ghi rõ provider call có thể phát sinh chi phí theo tài khoản; không chạy hàng loạt.

### 9.5. Các điểm UI phải sửa hoặc kiểm tra thêm

Web hiện chỉ hỏi aiStatus lúc component mount. Khi request lỗi/off, nút bị khóa; chưa thấy nút chủ động “Kiểm tra lại AI” ngay trong component. Mini message hiện còn ẩn toàn bộ nút AI khi status false hoặc fetch thất bại.

Bổ sung trải nghiệm:
- Phân biệt “AI chưa được bật”, “Không kiểm tra được kết nối” và “Tạo gợi ý thất bại”.
- Khi lỗi tải trạng thái, có nút thử lại trạng thái AI; debounce/busy guard, không tạo polling vô hạn và không tự refine.
- Mini không biến mất im lặng: đưa lý do và hành động phù hợp; bố cục riêng cho điện thoại.
- Không khóa gửi bằng tay/làm mất bản soạn vì AI lỗi.
- Giữ consent thực, author-only, input revision và stale checks trước/sau accept.
- Không ghi đè phần người dùng vừa sửa trong lúc chờ.
- Không giả lời gợi ý dựng sẵn thành kết quả Gemini thật.

### 9.6. Nghiệm thu AI bắt buộc, bổ sung cho T18

| ID | Ca | Kỳ vọng |
| --- | --- | --- |
| AI01 | PH mở thư HS gửi, nhập phản hồi và tạo gợi ý | Provider thật trả suggested_text hợp lệ; giữ nguyên ý, xưng hô phù hợp |
| AI02 | HS mở thư PH gửi và dùng AI | Được hỗ trợ bình thường vì HS là người nhận |
| AI03 | Tác giả mở thư mình đã gửi | Không có composer tự phản hồi; không dùng AI ở composer không hợp lệ |
| AI04 | Chưa đồng ý AI | Disclosure/đồng ý thực trước refine; từ chối vẫn viết/gửi tay được |
| AI05 | Dùng gợi ý | Ghi nhận accept và điền ô soạn; chưa tạo Message hoặc gửi |
| AI06 | Sửa lời khi refine/accept đang chờ | Bản mới không bị đè; stale cần tạo lại |
| AI07 | Flag off, key/config thiếu, status lỗi, provider timeout/quota | Trạng thái trung thực, không mất lời; retry hợp lý |
| AI08 | Double-click, đóng màn/đăng xuất/đổi actor | Không refine/accept trùng hoặc áp gợi ý actor cũ |
| AI09 | Cả web và Mini | Cùng backend/contract, UI đúng riêng từng client |
| AI10 | PH dùng AI rồi gửi, HS đăng nhập phiên riêng | HS nhận đúng lời PH đã duyệt; không nhận original/prompt/suggestion riêng |

Báo cáo tách biệt: component doubles / backend mock-provider tests / Gemini thật / Render deployed flow / Zalo device. Không đóng yêu cầu Huy bằng cách xóa nút AI, ép ai_enabled=true ở client hoặc chỉ nói “có thể viết tay”.
