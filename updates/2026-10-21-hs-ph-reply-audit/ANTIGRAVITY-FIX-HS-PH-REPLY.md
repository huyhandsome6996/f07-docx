# Family Bridge — Kiểm tra luồng HS/PH và prompt sửa cho Antigravity

Ngày lập: 21/10/2026 (UTC+7).  
Repo ứng dụng: https://github.com/huyhandsome6996/family-bridge  
Nhánh kiểm tra: main.  
Commit kiểm tra: `7ace3dab80c2473095cdef51c0cd3b35805b4143`.  
Phạm vi: F05 chi tiết thư/phản hồi; đối chiếu F10, shared adapter và quyền backend. Không phải nghiệm thu toàn bộ 15 tính năng.

## 1. Kết luận cần đọc trước

Phản ánh của Huy có cơ sở từ code: **cả web và Zalo Mini App đều dựng khung “Phản hồi thư này” ngay cả khi người đang mở chính là người gửi thư**.

Tuy nhiên, không được kết luận backend đã cho học sinh tự phản hồi thành công:
- F05 backend đã kiểm tra người phản hồi phải là recipient của thư gốc.
- Với A gửi B, A gửi tiếp có reply_to trỏ về thư A→B sẽ bị nhánh kiểm tra hiện hành từ chối.
- Lỗi nhìn thấy là giao diện mời người gửi thực hiện hành động không hợp lệ; khi API từ chối, UI lại có thể làm người dùng hiểu nhầm rằng thư có thể đã gửi.
- Lượt review này không gọi API ghi dữ liệu trên Render, không có tài khoản HS/PH thật để chạy end-to-end.

**Đích sửa:** đúng người, đúng chiều, đúng nội dung được trả lời; sửa đồng bộ hai client độc lập và giữ backend kiểm quyền.

Không sửa thành “chỉ cha mẹ được phản hồi mọi thư”. Với thư cha gửi con, con là người nhận và phải được phản hồi hợp lệ.

## 2. Bối cảnh và bất biến

Huy phản ánh tài khoản học sinh gửi nội dung cho cha rồi vẫn thấy chức năng tự phản hồi. Hai ảnh đã được nhắc trong cuộc trao đổi nhưng không đọc được trong môi trường review này; chưa xác định được chính xác route trên ảnh. Finding ở đây dựa trên mã nguồn và thăm dò hàm render, không dựa vào suy đoán nội dung ảnh.

Sản phẩm hiện tại có:
- Web độc lập trong `web/`.
- Zalo Mini App trong `zalo-mini-app/`.
- Shared headless contracts/adapter/session trong `packages/family_bridge_shared/`.
- Backend F05 trong `packages/family_bridge_features/f05_inbox/`.
- Hai client gọi cùng backend; sửa web không tự sửa giao diện Mini App.
- Stack hiện hành: HTML/CSS/JavaScript ES Modules + Vite; Mini dùng zmp-sdk. Không chuyển framework theo tài liệu React cũ.
- HS/PH được quản trị cấp tài khoản và liên kết sẵn theo quyết định hiện hành. Không bắt làm lại mã mời.

| Bước | Tài khoản HS | Tài khoản PH |
| --- | --- | --- |
| HS gửi thư M cho PH | Xem bản mình đã gửi; không có composer phản hồi vào M | Thấy thư nhận M |
| PH mở M | Không có hành động thay PH | Có composer phản hồi, gợi ý và AI nếu đủ điều kiện |
| PH gửi thư R trả lời M | Nhận thư R; mở/xem hoặc phản hồi R hợp lệ | Xem bản R mình gửi; không tự phản hồi R |
| PH chủ động gửi một thư mới | HS là người nhận và được phản hồi | PH là người gửi, không tự phản hồi thư đó |

“Đã gửi”, “đã đọc/đã nhận tín hiệu” và “đã có phản hồi” là ba trạng thái khác nhau. Không lấy mark_read hoặc F10 ack làm bằng chứng cha đã trả lời bằng lời. Không hiển thị “chờ phản hồi” vĩnh viễn nếu dữ liệu thực cho thấy đã có hồi âm; cũng không bịa trạng thái khi API chưa cung cấp.

## 3. Đã đọc và đã kiểm tra những gì

Đã lấy cây file GitHub, AGENTS.md, scope, DSA/security/UI/workflow skills/rules và các tài liệu user flows, state machines, access matrix, acceptance, decision register có liên quan.

Đã đọc các điểm triển khai chính:
- [Web message](https://github.com/huyhandsome6996/family-bridge/blob/7ace3dab80c2473095cdef51c0cd3b35805b4143/web/src/pages/message/index.js).
- [Mini App message](https://github.com/huyhandsome6996/family-bridge/blob/7ace3dab80c2473095cdef51c0cd3b35805b4143/zalo-mini-app/src/pages/message/index.js).
- [Web mailbox](https://github.com/huyhandsome6996/family-bridge/blob/7ace3dab80c2473095cdef51c0cd3b35805b4143/web/src/pages/mailbox/index.js).
- [Web signal](https://github.com/huyhandsome6996/family-bridge/blob/7ace3dab80c2473095cdef51c0cd3b35805b4143/web/src/pages/signal/index.js).
- [F05 transport](https://github.com/huyhandsome6996/family-bridge/blob/7ace3dab80c2473095cdef51c0cd3b35805b4143/packages/family_bridge_features/f05_inbox/services/transport.py).
- [F05 API](https://github.com/huyhandsome6996/family-bridge/blob/7ace3dab80c2473095cdef51c0cd3b35805b4143/packages/family_bridge_features/f05_inbox/api.py).
- [F05 model/DTO](https://github.com/huyhandsome6996/family-bridge/blob/7ace3dab80c2473095cdef51c0cd3b35805b4143/packages/family_bridge_features/f05_inbox/models.py).
- [Shared HTTP adapter](https://github.com/huyhandsome6996/family-bridge/blob/7ace3dab80c2473095cdef51c0cd3b35805b4143/packages/family_bridge_shared/src/adapter/http-endpoints.js).
- [Backend API tests](https://github.com/huyhandsome6996/family-bridge/blob/7ace3dab80c2473095cdef51c0cd3b35805b4143/packages/family_bridge_features/f05_inbox/tests/test_api.py).
- [Backend transport tests](https://github.com/huyhandsome6996/family-bridge/blob/7ace3dab80c2473095cdef51c0cd3b35805b4143/packages/family_bridge_features/f05_inbox/tests/test_transport.py).
- [Web screen tests](https://github.com/huyhandsome6996/family-bridge/blob/7ace3dab80c2473095cdef51c0cd3b35805b4143/web/tests/web-screens.test.mjs).
- F10 service/API và package.json của hai client.

Đã kiểm tra lại đầu main trước khi kết thúc đọc code: vẫn là SHA trên.

### Phương pháp chạy được trong lượt này

Môi trường chạy shell/container dự án không khả dụng. Reviewer vẫn thực thi được JavaScript trong V8 của công cụ điều phối:
1. Lấy nguyên nội dung hai file message theo SHA cố định.
2. Bỏ static imports và đổi export declaration để nạp module vào một hàm thử.
3. Gọi trực tiếp hàm thật `renderThread`.
4. Thay h/clear/createButton, DOM và các dịch vụ UI phụ bằng double tối thiểu.
5. Web AI component được thay bằng stub; Mini aiStatus trả ai_enabled=false.
6. Chạy mỗi client với direction sent, received, null.
7. Ở ca sent: nhập nội dung synthetic, bấm handler gửi, adapter ném lỗi HTTP 404 giả lập, sau đó lookup trả đúng shape backend `{state:"sent",message_id:"response-id"}`.

Đây là **thăm dò logic render/handler với dependency doubles**, không phải chạy happy-dom, bộ test Node của repo, browser layout, Django/API thật hoặc thiết bị Zalo.

Kết quả quan sát thực:

```json
[
  {
    "client": "web",
    "direction": "sent",
    "replyComposerVisible": true,
    "sendButtonVisible": true,
    "sendCalls": 1,
    "error404PresentedAsUnknown": true,
    "lookupStateSentRecognized": false
  },
  {
    "client": "web",
    "direction": "received",
    "replyComposerVisible": true,
    "sendButtonVisible": true
  },
  {
    "client": "web",
    "direction": null,
    "replyComposerVisible": true,
    "sendButtonVisible": true
  },
  {
    "client": "zalo-mini-app",
    "direction": "sent",
    "replyComposerVisible": true,
    "sendButtonVisible": true,
    "sendCalls": 1,
    "error404PresentedAsUnknown": true,
    "lookupStateSentRecognized": false
  },
  {
    "client": "zalo-mini-app",
    "direction": "received",
    "replyComposerVisible": true,
    "sendButtonVisible": true
  },
  {
    "client": "zalo-mini-app",
    "direction": null,
    "replyComposerVisible": true,
    "sendButtonVisible": true
  }
]
```

Ca received có composer là đối chứng hợp lệ. Ca sent và null có composer là hành vi cần sửa. Không cộng các ca tái hiện lỗi thành “tính năng PASS”.

### Chưa chạy

| Kiểm tra | Trạng thái trong lượt review |
| --- | --- |
| Django tests / test_feature.sh | NOT_RUN — không có runtime dự án |
| Node test suite / Vite build nguyên dự án | NOT_RUN — không có runtime dự án |
| Gọi backend thật bằng cặp HS/PH synthetic | NOT_RUN |
| Render end-to-end / SHA thực đang phục vụ | NOT_VERIFIED |
| MySQL/TiDB | NOT_RUN |
| Zalo Android/iOS, safe area, bàn phím | NOT_RUN |
| Xem hai ảnh phản ánh | UNAVAILABLE |

Các con số PASS ghi trong báo cáo cũ của repo là lịch sử, không phải kết quả reviewer vừa chạy.

## 4. Finding và bằng chứng

### R01 — P1: Thư đã gửi vẫn có composer phản hồi

**Đã xác nhận bằng code và thăm dò hàm render, ở cả hai client.**

Vị trí tại SHA review:
- Web message: dòng 235–237 tính direction; từ 281–283 dựng composer vô điều kiện.
- Mini message: dòng 261–263 tính direction; từ 307–309 dựng composer vô điều kiện.
- Web onSend: 322–337; Mini onSend: 367–382. Không có guard direction trước khi gọi sendMessage.

```js
const direction = thread && thread.direction === "sent" ? "sent" : "received";
// ... render body ...
const composeCard = h("section", { class: "fb-scard fb-msg-compose" });
composeCard.appendChild(h("h2", { class: "fb-scard__title" }, "Phản hồi thư này"));
```

Khi mở thư sent và nhập nội dung, handler vẫn gọi:
```js
sendMessage({
  kind: "text",
  recipientId: counterpartyId,
  body: text,
  replyTo: messageId,
  key
});
```

**Cần sửa:**
- Chỉ render composer cho `direction === "received"` và DTO đủ dữ liệu hợp lệ.
- Thư sent vẫn xem được bản mình gửi, người nhận và thời điểm.
- Không dựng textarea, quick-reply chips, AI composer hoặc nút gửi cho thư sent.
- Không gọi quickReplies/AI phục vụ composer không tồn tại.
- Handler cũng guard lại, không chỉ ẩn CSS/nút.
- Giữ quyền phản hồi của HS khi HS thực sự là người nhận.

### R02 — P1: Lỗi từ chối xác định bị báo thành kết quả chưa xác định; dễ tạo lượt gửi mới

**Đã xác nhận bằng thăm dò với lỗi HTTP 404 giả lập ở cả hai client.**

- Web catch: dòng 342–360.
- Mini catch: dòng 387–405.
- Mọi lỗi đều bị biến thành “KẾT QUẢ CHƯA XÁC ĐỊNH: máy chủ có thể đã nhận thư”.
- catch đồng thời đặt busy=false và bật nút gửi lại.
- Mỗi onSend sinh key mới. Người dùng bấm lại sau tình huống không rõ kết quả có thể tạo operation mới trước khi đối soát.

Trong F05, lỗi `reply_target_not_found` là từ chối cụ thể của reply guard, không phải mất xác nhận sau commit.

**Cần sửa theo contract/error code, không phân loại máy móc mọi 4xx/5xx:**
- Auth hết hạn: xử lý phiên, không nói “có thể đã gửi”.
- Bị từ chối do quyền/reply target/validation/conflict xác định: nêu lý do phù hợp, giữ lời đang soạn khi còn quyền.
- Timeout/mất kết nối sau khi dispatch hoặc server failure không chứng minh chưa commit: vào unknown-outcome.
- Khi unknown-outcome, giữ key + snapshot payload của operation đang chờ, chặn việc bấm lại sinh key mới ngay.
- Lookup trước; chỉ mở đường gửi tiếp theo policy đã đối soát. Không tự retry/auto-send.
- Sửa nội dung phải là một ý định gửi mới có preview/xác nhận rõ; không âm thầm đổi payload của key cũ.

### R03 — P1: Lookup đọc status trong khi backend trả state

**Đã xác nhận từ code liên kết và probe hai client.**

- Backend `OperationStatusView.get`: trả `state: "sent"` hoặc `state: "not_found"`.
- Shared `lookupOperation` dòng 663–667: trả data nguyên trạng, không chuẩn hóa state→status.
- Web message dòng 368 và Mini message dòng 413: đọc `result.status`.
- Probe cấp `{state:"sent"}`: cả hai không hiển thị xác nhận gửi thành công.

```python
return Response({"idempotency_key": idempotency_key,
                 "state": "sent", "message_id": found.message_id,
                 "created_at": found.created_at.isoformat()})
```

```js
// Hiện tại ở UI:
const status = result && result.status;
```

**Cần sửa:**
- Chọn contract rõ, dùng shape hiện hành của backend hoặc normalization có chủ đích ở shared boundary.
- Không thêm fallback nhiều shape chỉ để che drift.
- Sửa comment `lookupOperation`, fixtures và contract tests tương ứng.
- Rà các consumer khác, đặc biệt F10 và các màn gửi có lookup; đây là shared DTO, không chỉ một trang.
- Fake API trong test phải trả `state`, không trả `status` sai backend.

### R04 — P2: Direction thiếu/sai bị mặc định thành received

**Đã xác nhận bằng probe direction=null.**

Hai file đều dùng:
```js
const direction = thread && thread.direction === "sent" ? "sent" : "received";
```

Mọi giá trị khác sent, kể cả null/thiếu/chuỗi không hợp lệ, đều được coi là thư nhận và dựng quyền thao tác.

**Cần sửa:** kiểm tra allowlist sent/received; DTO không hợp lệ không được suy thành quyền phản hồi. Hiện lỗi dữ liệu/phương án tải lại; không gọi send/read/AI. Backend vẫn là authority cuối, client không tự dựng role/actor.

### R05 — P1 cần tái hiện backend: Chưa ràng buộc người nhận phản hồi là tác giả thư gốc

**Xác nhận thiếu guard từ code; chưa chạy Django/API để xác nhận runtime.**

`transport.py` dòng 96–102 mới có:
```python
if reply_to:
    parent = Message.objects.filter(pk=reply_to).first()
    if parent is None or str(parent.recipient_id) != str(sender_id):
        raise NotFound({"reason": "reply_target_not_found"})
    reply_to_id = str(parent.pk)
```

Không thấy đối chiếu `recipient_id == parent.sender_id` trong phần còn lại của send.

Kịch bản phải kiểm thử:
1. A gửi M cho B.
2. B có một kết nối hợp lệ khác với C.
3. B POST phản hồi có `reply_to=M` nhưng `recipient_id=C`.
4. Guard hiện tại chỉ xác nhận M gửi cho B; connection guard tiếp theo kiểm B↔C.
5. Theo đường code đã đọc, không có guard chặn việc gắn phản hồi vào sai cuộc trao đổi.

Chưa tuyên bố nội dung M đã lộ cho C; chưa chứng minh payload đọc nào làm lộ body thư gốc. Vấn đề trực tiếp là integrity của reply target/recipient.

**Cần sửa:** tái hiện trong fixture ba actor, giữ hai điều kiện:
- Người phản hồi là recipient thư gốc.
- Người nhận phản hồi là sender thư gốc.
- Kiểm tra quyền/kết nối/generation hiện hành theo policy; không nới quyền để làm UI “hết lỗi”.
- Thư mới không reply_to vẫn là luồng thư mới, không vô tình chặn gửi hợp lệ.
- Không cần migration/bảng chat mới chỉ để thêm guard.

### Ghi chú F10 — rà thêm, không nhầm ack với phản hồi

Đã đọc:
- `web/src/pages/signal/index.js` nhánh caregiver dòng 120–127 chỉ lọc `kind === "listening_signal"`, chưa lọc direction received.
- UI danh sách caregiver dựng nút ack.
- F10 ack gọi `transport.mark_read`; F05 mark_read là recipient-only.
- F05 inbox trả cả thư gửi và nhận.

Antigravity phải đối chiếu Mini App hiện hành riêng, kiểm tra fixture có tín hiệu sent lẫn received để không đưa thư gửi vào “Tín hiệu đã nhận” hoặc dựng ack sai actor. Chưa chạy probe toàn màn F10 trong lượt này, không ghi là lỗi end-to-end đã tái hiện.

Ack chỉ xác nhận đã nhận/đọc tín hiệu; không được giả làm PH đã gửi câu phản hồi hoặc đã nhận lịch hẹn.

## 5. Vì sao test hiện có bỏ lọt

`web/tests/web-screens.test.mjs`:
- Case “thư gửi đi (sent + đã đọc)” dòng 1389–1399 chỉ kiểm bong bóng sent và không markRead.
- Không kiểm composer/nút/AI phải vắng mặt với sent.
- Fixture lookup dùng `{status:"sent"}` ở nhiều chỗ, trong khi API thật trả state.
- Happy path student reply hiện có là HS trả lời thư từ bố: hành vi đó hợp lệ, không được xóa chỉ vì người dùng đang phản ánh chiều ngược lại.
- Backend test reply target hiện kiểm người lạ và người nhận thật; phải bổ sung chính sender tự reply và trường hợp B đổi recipient sang C.

Không xóa/sửa assertion chỉ để suite xanh. Thêm test mô tả hành vi đúng rồi sửa code.

## 6. Prompt chính thức giao Antigravity

Bạn là Antigravity, chịu trách nhiệm sửa luồng phản hồi HS/PH của Family Bridge dựa trên báo cáo này.

### 6.1. Bắt đầu và scope

1. Fetch main mới nhất, đọc AGENTS.md/nested instructions, mandatory DSA/security/UI/workflow documents tại checkout ứng dụng.
2. Ghi baseline SHA/head/deployed SHA riêng. Báo cáo này kiểm `7ace3dab80c2473095cdef51c0cd3b35805b4143`; nếu main đã đổi, kiểm lại từng finding, không áp snapshot cũ chép đè.
3. Kiểm worktree đang làm; tái sử dụng nhánh sửa phù hợp nếu đã có. Nếu cần nhánh mới, tạo worktree riêng từ latest main, ví dụ `fix/hs-ph-reply-direction`. Không reset/clean worktree người khác.
4. Phạm vi sửa gồm R01–R05, tests bắt buộc và các shared consumers bị cùng drift R03. Kiểm tra ghi chú F10. Không redesign toàn sản phẩm hay triển khai lại F02/F04/F07/F15.
5. Hai UI tree độc lập: sửa đúng cả `web/` và `zalo-mini-app/`. Chia sẻ helper headless nhỏ khi thực sự giảm drift; không chuyển stack hay nhập nguyên UI desktop vào Mini.
6. Giữ F08 hiện hành: main review đã có diary đầy đủ. Không lấy ZIP cũ khôi phục placeholder “chưa mở”.
7. Giữ HS/PH liên kết sẵn; không thay consent, tự bật Zalo login, thêm admin bypass hay buộc mã mời.

### 6.2. Công việc bắt buộc

- Chặn render lẫn handler tự phản hồi thư sent; received được phản hồi ở cả HS và PH.
- Kiểm DTO direction/message ID/counterparty ID trước khi mở thao tác; unknown fail closed.
- Bảo toàn nội dung thư, recipient thật, preview và xác nhận chủ động theo WF-05.
- Với nội dung/recipient thay đổi sau preview, invalidate preview; không tự gửi từ AI/gợi ý/timer.
- Dùng đúng `kind: "text"` hoặc quick_reply hợp đồng hiện hành và `reply_to` đúng thư nhận; không tạo kind "reply" ngoài allowlist.
- Ràng buộc cặp actor reply ở backend, không chỉ hide button.
- Phân loại xác định bị từ chối và unknown-outcome; giữ operation key/payload khi chưa đối soát.
- Sửa lookup theo contract backend và đồng bộ adapter comments/mock fixtures/tests/consumers.
- Giữ cleanup/stale session safeguards: logout/đổi actor/unlink không để response cũ hoặc composer cũ phát sinh hành động dưới actor mới.
- Không dùng is_staff/superuser/client role để mở quyền đọc thư người khác.
- Không auto-reply, tự đóng vai PH, auto-ack thay người nhận, auto-forward hoặc tự tạo lịch hẹn.
- Câu chữ đúng sự thật: read không phải reply; không hứa trạng thái mà API chưa cung cấp.

### 6.3. Ma trận nghiệm thu tối thiểu

Chạy UI cho cả web và Mini, backend direct API cho phần ACL. Dùng dữ liệu synthetic cô lập.

| ID | Ca kiểm tra | Kỳ vọng |
| --- | --- | --- |
| T01 | HS gửi M cho PH, HS mở M | Thấy bản sent; không composer/AI reply/nút phản hồi; không gọi send |
| T02 | PH mở M | Received; có composer; read theo contract đúng recipient |
| T03 | PH trả lời M | Đúng một Message PH→HS, reply_to=M, body do PH duyệt |
| T04 | HS mở phản hồi PH | Đúng nội dung PH; HS được phản hồi thư nhận này nếu muốn |
| T05 | PH mở bản trả lời mình gửi | Không tự phản hồi bản sent |
| T06 | PH chủ động gửi thư N cho HS | HS phản hồi hợp lệ; không hardcode “HS không được phản hồi” |
| T07 | HS gọi POST tự reply M trực tiếp | Backend từ chối; DB không thêm Message; không unknown-outcome sai |
| T08 | A→B; B reply_to M nhưng recipient=C, B↔C active | Từ chối, không tạo Message sai cuộc trao đổi |
| T09 | Actor thứ ba/admin đoán M | Không đọc body, read/ack hoặc reply trái phép |
| T10 | Direction thiếu/sai, thiếu message/counterparty ID | Không composer và không mutation/read call suy từ mặc định |
| T11 | Server trả lỗi từ chối reply_target_not_found | Lỗi phù hợp; không báo “có thể đã gửi” |
| T12 | Mất response sau khi server đã commit | Giữ key/payload; lookup state=sent xác nhận; không tạo key mới/Message thứ hai |
| T13 | Lookup state=not_found hoặc còn không rõ | Phản ánh đúng mức chắc chắn; không auto-send; quyết định retry có policy |
| T14 | Double-click gửi và lookup; sửa nội dung giữa chừng | Có guard; không duplicate effect; snapshot/key nhất quán |
| T15 | Unlink/revoke/đổi actor khi đang tải, soạn hoặc gửi | ACL server/stale guards hoạt động; không render/gửi sai actor |
| T16 | F10 caregiver nhận list cả sent/received | Chỉ mục đúng chiều có ack; học sinh không ack thay PH |
| T17 | F10 ack, read một thư, PH gửi câu trả lời | Phân biệt ba hành động; không bịa “đã phản hồi” từ read |
| T18 | Gợi ý nhanh/AI | Chỉ cho composer hợp lệ; chỉ điền lời; không tự gửi |
| T19 | Nội dung HTML/script trong thư | Render text an toàn, không XSS |
| T20 | Thư sent có/không có hồi âm thật | Nhãn đúng dữ liệu, không gắn “chờ phản hồi” sai mãi |
| T21 | Mở Mini trên điện thoại nhỏ, bàn phím và back | Nội dung/nút không che khuất; không mang layout desktop vào |
| T22 | Cặp HS/PH đăng nhập hai phiên riêng, không dùng role preview giả | Đi hết vòng HS gửi → PH nhận/trả lời → HS nhận |

T01/T02/T06 phải là đối chứng hai chiều, không chỉ kiểm “ẩn mọi composer” rồi coi đã sửa.

### 6.4. Lệnh kiểm tra

Đây là lệnh cho Antigravity chạy, **reviewer chưa chạy trong lượt này**:

```bash
git diff --check
python scripts/check_agent_docs.py
bash tests/feature-lab/scripts/test_feature.sh f05_inbox
bash tests/feature-lab/scripts/test_feature.sh f10_signal
npm --prefix web test
npm --prefix web run build
npm --prefix zalo-mini-app test
npm --prefix zalo-mini-app run build
```

Đọc script harness/config hiện hành trước khi chạy; dùng đúng Python/dependency/feature registrations. Client yêu cầu Node >=22.12.0 theo package.json tại SHA review. Cài từ lockfile, không nâng dependency chỉ để vượt test.

Bổ sung test chạy với production wiring/FBSD session và hai tài khoản synthetic cô lập nếu harness module chỉ dùng connection doubles. Đọc backend README và test_classroom_integration hiện hành để chọn command/settings chính xác, không bịa lệnh đã PASS. Nếu không có MySQL/device thì ghi NOT_RUN, không thay bằng SQLite/browser rồi gọi là MySQL/Zalo PASS.

### 6.5. Git, triển khai và bàn giao

- Commit/push diff tập trung, PR theo workflow hiện hành; không force push, ghi đè concurrent changes hoặc tự merge ứng dụng khi chưa có quyền.
- Đợt giao việc này yêu cầu sửa và kiểm thử; không suy từ prompt deploy cũ để tự đổi cấu hình Render, chạy migration live, xét duyệt hoặc phát hành Zalo Live.
- Nếu phiên làm việc của Huy đã có quyền deploy Testing/Render còn áp dụng, thực hiện đúng phạm vi đó sau test, ghi deployed SHA và kiểm chứng bản đang phục vụ. Nếu chưa có quyền, hoàn thiện commit/PR/evidence và bàn giao bước deploy cụ thể, không chỉ nói “cần kiểm tra”.
- Không dùng secret từng lộ trong chat, không ghi credential hoặc dữ liệu thật vào báo cáo.
- Bàn giao tiếng Việt: baseline/head SHA, PR, changed files, nguyên nhân từng finding, before/after, command/environment/result, UI/API/MySQL/device tách biệt.
- R05 chỉ được đóng sau direct service/API test ba actor. R01 chỉ đóng khi cả hai client qua negative sent và positive received.
- Nếu đã deploy: cung cấp web routes thật, Mini Testing version/link/QR từ Zalo, cách test hai tài khoản và cách quay lại bản trước. Không đưa loopback làm URL cho Huy.
- Không nói “toàn bộ sản phẩm đã kiểm thử” từ một bộ test F05.

**Bắt đầu từ tái hiện rồi sửa; không chỉ trả lại kế hoạch.**

## 7. Tiêu chí reviewer chấp nhận và giới hạn

Có thể chấp nhận bản sửa code khi R01–R04 được regression tests kiểm chứng ở hai client, R05 có backend negative test, happy path hai chiều giữ nguyên, build/tests liên quan qua, diff không phá phần khác.

Nghiệm thu bản người dùng thật cần thêm bằng chứng hai tài khoản trên bản đã triển khai và Zalo thiết bị thật cho Mini. Hai gate riêng; CI xanh hoặc V8 probe không thay bằng chứng phát hành.

DSA cho thay đổi đề xuất:
- Direction guard/DTO checks O(1), bộ nhớ O(1), không cần query mới cho UI.
- Reply recipient binding tận dụng parent đã đọc, thường không cần tăng round trip.
- Lịch sử/phản hồi nếu cần bổ sung phải có quyền trước pagination và giới hạn; không tải toàn bộ hộp thư để suy trạng thái.
- Operation state giữ một lượt pending đang xét ở scope actor/session với bounds rõ; không persist private body/token ra storage công khai.
- Chưa đo query count/hiệu năng MySQL; không có benchmark trong lượt review.

## 8. Tình trạng cuối của đợt review này

- Đã đọc main hiện hành và đối chiếu code UI/shared/backend/tests.
- Đã chạy probe hàm render/handlers với dữ liệu synthetic và dependency doubles.
- Chưa thay đổi code ứng dụng, merge hoặc deploy.
- Chưa chạy Django, Node suite toàn repo, browser hay thiết bị Zalo.
- File này là báo cáo + prompt sửa, không phải xác nhận lỗi đã được sửa.


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
