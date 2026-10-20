# F02 — tiếp tục từ đây

## Trạng thái cuối lượt QA 19/10

- App source exactSHA c29469b3d57f2c2cc53fe686fe7ec8f917f2dec6; nhánh F02 hiệncó.
- Không sửa/commit/push codeapp. WorkingtreeQA detached sạch, ngoài DB/build/dependencies ignored.
- Không đụng worktree dirty `work/f02-completion-20261018` từ phiên trước. Agent đã push fixes tươngứng tốt hơn; khôngcherry-pick patch cũ mù.
- Tài liệu/ảnh/prompt mới nằm ở **f07-docx/F02-docx** theo chỉ thịHuy; mainF07 được giữ nguyên.
- Đọc FINDINGS:7mục,4lỗiruntime +2gapMiniApp +1gapweb; R02 vàR03 ưu tiêncao. Backend/clientssuites đều xanh nhưng assertions mới fail.

## Runtime local đã chạy

- Appcheckout: `C:/Users/PC/Documents/Codex/2026-10-14/https-github-com-huyhandsome6996-family-bridge/work/qa-f02-c29469b-20261019`.
- Backend8004: config.settings, SQLite riêng backend/db.sqlite3, sessionexec89604.
- MiniApp3004: sessionexec27401, VITE_API_BASE_URL=http://127.0.0.1:8004, labelF02QAc29469b.
- Một serverweb test3104 được mở để chuẩn bị, session69946; không gọi đây là F02web đãtestUI. Không CORS3104 trongbackend vàkhôngcần chạmserverHuy đangdùng.
- BrowserMiniApp đã giữ làm deliverable, accountHS903 active; localonly.
- Server/sessionID có thể khôngcòn sống khi chatkhác đọc. Verifyhealth/cwd/SHA trước dùng; khôngkill cổng củaagentkhác.

## Dữ liệu fixture cuối lượt

- CặpHS901/PH901 đã test coreHTTP rồi unlink; còn invite test được accepted sai saurevoke (R03).
- CặpHS903/PH903 active; HS903 enrollrev1/doneweek1/pendinginvite/đềxuấtagreement; PH903 chưaenroll.
- CặpHS905/PH905 active; cảhai enrollprogramrev2, pendingagreement vẫn pinrev1 gâyR02.
- Programrev1/2, agreementtemplaterev1; week1activitypublishedrev1/2. Tấtcảsynthetic.
- Passwordthử doenvF02_QA_PASSWORD của các runner; checklist cógiátrịfake riêng local. Không gửi/render realcredentials.

## Bước tiếp theo cho chat coding

1. Fetchapp/docs đúngnhánh, kiểm source/owner mới nhất; đọcPROMPT-COPY-F02 +FINDINGS/evidence.
2. Tái hiệnR02/R03/R01, viếtregressions thật trướcfix; đồngbộF09owner/sharedcontracts; giữ cácfixcũR1–R4/BUG01/02.
3. Hoànthiệnread-before-enroll/activitydetail và xácđịnhwebgate; khônglấyMiniAppbrowserpreview làmweb.
4. Chạy suite/realHTTP/UI lại trênSHAcuối, update docs ở thưmục mới dướiF02-docx, đưaHuyURLthật+checklistngắn.

Không tự merge main, deploy, publish nội dungthật hoặcapplymigrationproduction. Nếu gần hếtlưu lượng, ghi exactSHA/log/state/dở ởhandover trướcngừng.
