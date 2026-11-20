# Giả định & Thiết kế (Assumptions & Design Choices)

Tài liệu này ghi lại toàn bộ các giả định hợp lý cho các điểm PRD để ngỏ và các thông số cân bằng (`tuning`).

---

## 1. Phase 1 (PRD-0) — Các thông số ban đầu
*(Xem chi tiết lịch sử tại commit tag `phase-1`)*
- `player_speed`: 5.0 m/s
- `lantern_cost`: 5 đom đóm
- `pulse_cost`: 1 đom đóm, `pulse_radius`: 6.0 m
- `fall_enabled`: false

---

## 2. Phase 2 (TICKET-02) — Chuẩn hóa số liệu & Mở rộng 3 Đêm

Ticket-02 đồng bộ các số liệu chuẩn bắt buộc, thay thế toàn bộ giá trị tự chọn ở Phase 1:

### A. Bảng thông số chuẩn hóa (Tuning v1.1)

| Nhóm | Thông số | Giá trị chuẩn | So với Phase 1 & Lý do thay đổi |
|---|---|---|---|
| **Di chuyển** | `player_speed` | `6.0` m/s | Tăng từ 5.0 lên 6.0 m/s để di chuyển linh hoạt qua các đảo rộng. |
| | `dash_speed` | `14.0` m/s | **Mới:** Tốc độ lướt tức thời. |
| | `dash_duration_s`| `0.2` s (12 ticks)| **Mới:** Thời gian lướt. |
| | `dash_cooldown_s`| `1.5` s (90 ticks)| **Mới:** Thời gian hồi chiêu lướt. |
| **Nhảy & Rơi** | Nhảy | $v_y = 7.0$ m/s | Trọng lực $-20.0$ m/s$^2$. Chỉ nhảy khi chạm đất (`grounded`). |
| | `fall_enabled` | `true` | Bật cơ chế rơi khỏi đảo khi $Y < -10$. Mất 1 Lửa, mất sạch đom đóm, chờ 60 tick hồi sinh tại (0,0,0) với 90 tick bất tử. |
| **Đom đóm** | `carry_capacity` | `10` | Giữ nguyên 10 con tối đa. |
| | `pickup_radius` | `1.0` m | Giảm từ 1.5m xuống 1.0m (kèm điều kiện chênh cao $\le 1.5$m). |
| | Số lượng sinh | 20 con ban đầu | Trần 30 con; sinh thêm 1 con mỗi 240 ticks nếu còn điểm trống. |
| | Đom đóm rơi | TTL 480 ticks | Rơi khi bị Bóng Mực đánh hoặc Gió Lạc bị Pulse làm rơi; nhặt lại được từ tick sau. |
| **Đèn lồng** | `lantern_cost` | `10` | Tăng từ 5 lên 10 đom đóm. Nạp nhiều lần được. |
| | `interact_radius`| `2.0` m | Chuẩn hóa 2.0m quanh đèn chưa thắp sáng. |
| | `safe_radius` | `6.0` m | Tăng từ 5.0m lên 6.0m. Bóng mực ở ngoài bị cản ở 6m; bóng ở trong bị đẩy ra mép trong 30 ticks. |
| **Tỏa Sáng** | `pulse_cost` | `3` đom đóm | Tăng từ 1 lên 3 đom đóm. |
| | `pulse_radius` | `5.0` m | Chuẩn hóa 5.0m tính từ tâm (chân Mây + 0.8m). |
| | `pulse_cooldown_s`| `3.0` s | Tăng từ 1.0s lên 3.0s. |
| | `pulse_stun_s` | `2.0` s (120 ticks)| Thời gian làm choáng Bóng Mực. |
| | `pulse_push_m` | `4.0` m | Đẩy lùi chia đều trong 15 ticks đầu thay vì tức thời. |
| **Bóng Mực** | `shade_speed` | `4.0` m/s | Đêm 1 và 2 là 4.0 m/s; Đêm 3 tăng lên 4.5 m/s. |
| | Trạng thái chuẩn | 5 trạng thái | `spawning`, `wander`, `chase`, `recoil`, `stunned`. |
| **Thời lượng** | `night1_duration_s`| `300` s | Đêm 1: 5 phút. |
| | `night2_duration_s`| `330` s | Đêm 2: 5 phút 30 giây. |
| | `night3_duration_s`| `360` s | Đêm 3: 6 phút. |
| **Tính điểm** | Chuẩn hóa | Điểm mới | Nạp đom đóm: `+10/con`; Thắp đèn: `+100/đèn`; Choáng bóng: `+5/lần`. Thắng: `+ floor(thời gian) * 2 + 50 * Ngọn Lửa`. |

### B. Giả định thiết kế cho các thực thể mới
1. **Gió Lạc (Drifter):** 
   - Bay ở độ cao $Y \approx 2.0$m. Cướp $\min(3, \text{đang mang})$ khi $XZ \le 1.2$m.
   - Khi Tỏa Sáng trúng lúc đang `flee` có mang đồ: thả rơi đom đóm tại tọa độ hiện tại của Gió Lạc và đom đóm này có TTL 480 ticks.
2. **Bùa Gió (Charm):**
   - Hồi sinh sau 2700 ticks kể từ khi bị người chơi nhặt.
   - Khi nhặt bùa trong lúc còn bùa cũ: làm mới lại đủ 600 ticks.
3. **Bục nhảy (Jump Pad):**
   - Vận tốc giữ nguyên quỹ đạo parabol đến khi chạm sàn đích (phím di chuyển không ghi đè vận tốc phóng, nhưng vẫn cho phép lướt).
