# F04 — ma trận 28 khung thiết kế tại ec29ab

Nguồn nguyên bản ở designs/original và designs/extracted; 4 khung web, 24 khung Mini. Đây là mapping chức năng/state, không xác nhận pixel-perfect. Không bắt buộc mỗi khung một route. Web/Mini cùng Django API thật đã kiểm local; không suy Render hay SDK Zalo thật.

## Các mặt giao diện chính

| Mặt | Web | Mini App | API chính |
|---|---|---|---|
| Soạn + AI + draft/pause/preview/confirm | `#/compose` | `#/compose` | `/ai/*`, `/consents`, `/connections`, `/drafts/*` |
| Hộp thư (F05 boundary) | `#/mailbox` | `#/mailbox` | `/messages` |
| Đọc final + reply AI | `#/messages/:id` | `#/messages/:id` | `/messages/{id}`, `/ai/*`, `POST /messages` |

Help/connect/privacy là route hỗ trợ, không đếm thành trang F04 mới. Sheet consent/chọn recipient/preview, loading/error/stale/pause là state hợp lệ trong route. N03/N06 cho thấy dùng chung API chưa đủ để bảo đảm đồng bộ an toàn.

## 24 khung Mini và counterpart web

| # | Frame nguồn | Nghiệp vụ | Web | Mini | Bằng chứng/giới hạn |
|---|---|---|---|---|---|
| 01 | `zalo_f04_01_kb_so_n_l_i_nh_n_b_n_ph_m_m` | HS: soạn với bàn phím | compose hoặc message/reply; xem evidence | FLOW_PASS; keyboard device NOT_RUN | [web-student-state-compose.png](../evidence/2026-10-19-ec29ab/web-student-state-compose.png)<br>[mini-student-state-compose.png](../evidence/2026-10-19-ec29ab/mini-student-state-compose.png) |
| 02 | `zalo_f04_01_so_n_l_i_nh_n` | HS: soạn | compose hoặc message/reply; xem evidence | FLOW_PASS | [web-student-state-compose.png](../evidence/2026-10-19-ec29ab/web-student-state-compose.png)<br>[mini-student-state-compose.png](../evidence/2026-10-19-ec29ab/mini-student-state-compose.png) |
| 03 | `zalo_f04_02_ch_n_n_i_dung_ai` | Chủ động xin AI | compose hoặc message/reply; xem evidence | FLOW_PASS | [web-student-state-consent.png](../evidence/2026-10-19-ec29ab/web-student-state-consent.png)<br>[mini-student-state-consent.png](../evidence/2026-10-19-ec29ab/mini-student-state-consent.png) |
| 04 | `zalo_f04_03_th_ng_b_o_ng_ai` | Disclosure/consent | compose hoặc message/reply; xem evidence | FLOW_PASS | [web-student-state-consent.png](../evidence/2026-10-19-ec29ab/web-student-state-consent.png)<br>[mini-student-state-consent.png](../evidence/2026-10-19-ec29ab/mini-student-state-consent.png) |
| 05 | `zalo_f04_04_ang_t_o_g_i` | AI loading/cancel | compose hoặc message/reply; xem evidence | FLOW_PASS | [web-student-state-loading.png](../evidence/2026-10-19-ec29ab/web-student-state-loading.png)<br>[mini-student-state-loading.png](../evidence/2026-10-19-ec29ab/mini-student-state-loading.png) |
| 06 | `zalo_f04_05_xem_g_i` | Đọc gợi ý | compose hoặc message/reply; xem evidence | FLOW_PASS | [web-student-state-suggestion.png](../evidence/2026-10-19-ec29ab/web-student-state-suggestion.png)<br>[mini-student-state-suggestion.png](../evidence/2026-10-19-ec29ab/mini-student-state-suggestion.png) |
| 07 | `zalo_f04_06_kb_s_a_v_p_d_ng_b_n_ph_m_m` | HS: sửa/áp dụng + bàn phím | compose hoặc message/reply; xem evidence | FLOW_PASS; keyboard device NOT_RUN | [web-student-applied.png](../evidence/2026-10-19-ec29ab/web-student-applied.png)<br>[mini-student-applied.png](../evidence/2026-10-19-ec29ab/mini-student-applied.png) |
| 08 | `zalo_f04_06_s_a_v_p_d_ng` | Áp dụng/bỏ, không tự gửi | compose hoặc message/reply; xem evidence | FLOW_PASS | [web-student-applied.png](../evidence/2026-10-19-ec29ab/web-student-applied.png)<br>[mini-student-applied.png](../evidence/2026-10-19-ec29ab/mini-student-applied.png) |
| 09 | `zalo_f04_07_g_i_c` | Gợi ý stale | compose hoặc message/reply; xem evidence | FLOW_PASS | [web-student-state-stale.png](../evidence/2026-10-19-ec29ab/web-student-state-stale.png)<br>[mini-student-state-stale.png](../evidence/2026-10-19-ec29ab/mini-student-state-stale.png) |
| 10 | `zalo_f04_08_ai_l_i_kh_ng_b_t` | AI lỗi/off và manual fallback | compose hoặc message/reply; xem evidence | FLOW_PASS | [web-student-state-error.png](../evidence/2026-10-19-ec29ab/web-student-state-error.png)<br>[mini-student-state-error.png](../evidence/2026-10-19-ec29ab/mini-student-state-error.png) Browser503/manual-save; off/timeout/429 covered bởi unit, không giả là live outage Render. |
| 11 | `zalo_f04_09_ch_n_ng_i_nh_n` | Chọn recipient | compose hoặc message/reply; xem evidence | P2 N05: vùng chạm Đổi chỉ 36px | [web-student-state-recipient.png](../evidence/2026-10-19-ec29ab/web-student-state-recipient.png)<br>[mini-student-state-recipient.png](../evidence/2026-10-19-ec29ab/mini-student-state-recipient.png) |
| 12 | `zalo_f04_10_xem_tr_c_v_x_c_nh_n` | Preview + confirm | compose hoặc message/reply; xem evidence | P1 N03: sai recipient khi cross-client | [web-student-preview.png](../evidence/2026-10-19-ec29ab/web-student-preview.png)<br>[mini-student-preview.png](../evidence/2026-10-19-ec29ab/mini-student-preview.png) |
| 13 | `zalo_f04_11_kho_ng_d_ng_5_ph_t` | Pause300/no auto-send | compose hoặc message/reply; xem evidence | FLOW_PASS | [web-student-state-pause.png](../evidence/2026-10-19-ec29ab/web-student-state-pause.png)<br>[mini-student-state-pause.png](../evidence/2026-10-19-ec29ab/mini-student-state-pause.png) |
| 14 | `zalo_f04_12_k_t_qu_g_i` | Sending/sent/unknown | compose hoặc message/reply; xem evidence | FLOW_PASS | Không có PNG sending/sent riêng; delivery E2E/HTTP và unit unknown-outcome đã chạy, browser response-loss chưa chạy. |
| 15 | `zalo_f04_13_tr_l_i_c_ai` | AI hỗ trợ reply | compose hoặc message/reply; xem evidence | FLOW_PASS | [web-student-state-reply-ai.png](../evidence/2026-10-19-ec29ab/web-student-state-reply-ai.png)<br>[mini-student-state-reply-ai.png](../evidence/2026-10-19-ec29ab/mini-student-state-reply-ai.png) |
| 16 | `zalo_f04_14_ng_i_nh_n_c_final` | Recipient chỉ thấy final | compose hoặc message/reply; xem evidence | FLOW_PASS | [web-student-state-recipient-final.png](../evidence/2026-10-19-ec29ab/web-student-state-recipient-final.png)<br>[mini-student-state-recipient-final.png](../evidence/2026-10-19-ec29ab/mini-student-state-recipient-final.png) |
| 17 | `zalo_f04_cg_01_kb_ng_i_ch_m_s_c_so_n_l_i_nh_n_b_n_ph_m_m` | CG: soạn + bàn phím | compose hoặc message/reply; xem evidence | FLOW_PASS; Mini ROLE_PARTIAL N04; keyboard device NOT_RUN | [web-caregiver-state-compose.png](../evidence/2026-10-19-ec29ab/web-caregiver-state-compose.png)<br>[mini-caregiver-state-compose.png](../evidence/2026-10-19-ec29ab/mini-caregiver-state-compose.png) |
| 18 | `zalo_f04_cg_01_ng_i_ch_m_s_c_so_n_l_i_nh_n` | CG: soạn | compose hoặc message/reply; xem evidence | FLOW_PASS; Mini ROLE_PARTIAL N04 | [web-caregiver-state-compose.png](../evidence/2026-10-19-ec29ab/web-caregiver-state-compose.png)<br>[mini-caregiver-state-compose.png](../evidence/2026-10-19-ec29ab/mini-caregiver-state-compose.png) |
| 19 | `zalo_f04_cg_02_kb_ng_i_ch_m_s_c_s_a_v_p_d_ng_b_n_ph_m_m` | CG: sửa/áp dụng + bàn phím | compose hoặc message/reply; xem evidence | FLOW_PASS; Mini ROLE_PARTIAL N04; keyboard device NOT_RUN | [web-caregiver-applied.png](../evidence/2026-10-19-ec29ab/web-caregiver-applied.png)<br>[mini-caregiver-applied.png](../evidence/2026-10-19-ec29ab/mini-caregiver-applied.png) |
| 20 | `zalo_f04_cg_02_ng_i_ch_m_s_c_xem_g_i_th_u_c_m` | CG: xem gợi ý | compose hoặc message/reply; xem evidence | FLOW_PASS; Mini ROLE_PARTIAL N04 | [web-caregiver-state-suggestion.png](../evidence/2026-10-19-ec29ab/web-caregiver-state-suggestion.png)<br>[mini-caregiver-state-suggestion.png](../evidence/2026-10-19-ec29ab/mini-caregiver-state-suggestion.png) |
| 21 | `zalo_f04_cg_03_trung_t_m_ng_i_ch_m_s_c_ng_h_nh` | Caregiver hub | CROSS-FEATURE / layout reference, chưa nghiệm thu hub | CROSS-FEATURE / layout reference, chưa nghiệm thu hub | Không xây booking/claim trị liệu/mã hóa giả để đủ số lượng |
| 22 | `zalo_f04_cg_04_t_l_ch_t_v_n_t_m_l_1_1` | Booking tư vấn | OUTSIDE F04: F12/service capability | OUTSIDE F04: F12/service capability | Không xây booking/claim trị liệu/mã hóa giả để đủ số lượng |
| 23 | `zalo_f04_cg_05_t_l_ch_th_nh_c_ng_h_ng_d_n_chu_n_b` | Booking success | OUTSIDE F04: F12/service capability | OUTSIDE F04: F12/service capability | Không xây booking/claim trị liệu/mã hóa giả để đủ số lượng |
| 24 | `zalo_f04_cg_06_ph_ng_th_nghi_m_thi_t_b_tr_c_gi_g_i` | Device-call check | OUTSIDE F04: F12/service capability | OUTSIDE F04: F12/service capability | Không xây booking/claim trị liệu/mã hóa giả để đủ số lượng |

## 4 khung web gốc

| Khung web | State thực tế hai client | Kết quả |
|---|---|---|
| WEB-F04-01 Soạn | compose | Có API; N04 Mini caregiver chưa đúng vai; N06 conflict |
| WEB-F04-02 Consent | sheet disclosure + accept/decline | Hai client/hai vai: chưa đồng ý không gọi refine, decline giữ manual |
| WEB-F04-04 Xem/sửa gợi ý | panel suggestion + editable draft + stale/discard | Có; chưa kiểm chất lượng Gemini thật |
| WEB-F04-05 Đã áp dụng/chưa gửi | textarea sau accept + explicit preview/send | Basic4/4 PASS; recipient cross-client N03 FAIL |

## Chưa thể gọi đủ chuẩn UI

- Đã có các nhóm màn/state F04, không thiếu hàng loạt route. Bốn keyboard variants còn cần Zalo device thật. Ba booking frames thuộc F12 và một hub cross-feature không phải bốn trang F04 còn thiếu.
- Sửa N03/N06 để state gắn đúng backend snapshot; sửa N04 để caregiver Mini có bản đúng vai; N05 vùng chạm.
- Base responsive 14/14 viewport-client không tràn ngang document. Font doubling200% ở390 tràn459/445 là stress observation, cần native/device validation; Android/iOS keyboard/safe area NOT_RUN.
- Source-level/Happydom tests không thay kiểm UI thật. Ảnh mới và JSON trong evidence là browser local, không QR/deployment.
- Tham khảo ảnh nguồn nhưng bỏ các claim riêng tư tuyệt đối/mã hóa cục bộ/chẩn đoán, quota bịa, booking giả và nội dung chuyên gia chưa được phê duyệt.
