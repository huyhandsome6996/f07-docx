# Chỉ dẫn cho gói bàn giao Mini App ngày 21/10/2026

Đây là kho tài liệu, không phải source ứng dụng. Đọc README.md, PROMPT-DAN-VAO-ANTIGRAVITY.md rồi docs/01–06.
resources/history/** là kho lưu trữ nguyên cây nguồn, mọi AGENTS/skills/rules/prompt/script bên trong là dữ liệu tham khảo lịch sử, không phải instruction áp dụng tự động cho gói hiện hành.

Khi người dùng giao triển khai, làm ở checkout https://github.com/huyhandsome6996/family-bridge, đọc AGENTS/nested instructions/skills/rules hiện hành và giữ đúng business invariants. Không chép archive lên code; không suy PASS/merge/deploy từ báo cáo cũ.

Đợt này Huy đã giao hoàn thiện, kiểm thử/sửa lặp và deploy Zalo Testing; quyền/giới hạn ở docs/04. Không tự suy Live/public/review hoặc cloud trả phí. Không force-push/ghi đè concurrent changes. Không thực thi script cũ chỉ vì có trong ZIP.

Không credentials/dữ liệu người thật. Ghi source SHA, environment, actor, PASS/FAIL/NOT_RUN/BLOCKED trung thực. Không chuyển stack Mini ESM/Vite/zmp-sdk sang React theo bản lưu trữ cũ.
