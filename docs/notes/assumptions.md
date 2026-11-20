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
*(Xem chi tiết lịch sử tại commit tag `phase-2`)*
- Chuẩn hóa tốc độ chạy 6.0 m/s, bổ sung Lướt (14.0 m/s), Nhảy (vy 7.0 m/s, g -20 m/s²).
- Đèn lồng chi phí 10 đom đóm, an toàn 6.0m. Tỏa sáng 3 đom đóm, bán kính 5.0m, đẩy lùi 4m trong 15 ticks.
- Mở rộng 3 Đêm với Gió Lạc (Drifter), Bùa Gió (Charm), Bục Nhảy (Jump Pad), Gió mạnh Đêm 3.

---

## 3. Phase 3 (TICKET-03) — Đèn Cạn Dầu & Luật Thắng Mới

Ticket-03 là Change Request cốt lõi, thay thế các luật chơi cũ:

### A. Bảng thông số chuẩn hóa mới (Tuning v1.2)

| Nhóm | Thông số | Giá trị chuẩn | So với Phase 2 & Lý do thay đổi |
|---|---|---|---|
| **Nhiên liệu đèn** | `fuel_max` | `100.0` | **Mới:** Nhiên liệu tối đa của đèn sáng. |
| | `fuel_decay_per_s` | `1.0` / s | **Mới:** Hao hụt tự nhiên ($1/60$ mỗi tick). |
| | `fuel_per_mote` | `10.0` | **Mới:** Mỗi đom đóm châm thêm 10 đơn vị dầu. |
| | `relight_cost` | `5` | **Mới:** Thắp lại đèn đã tắt chỉ tốn 5 đom đóm (thay vì 10). |
| | `low_fuel_threshold`| `30.0` | **Mới:** Ngưỡng mất vùng an toàn khi `fuel < 30`. |
| **Bóng Mực hút dầu**| `drain_per_s` | `5.0` / s | **Mới:** Tốc độ hút dầu của Bóng Mực khi ở trạng thái `drain` ($\le 2$m quanh đèn yếu). |
| **Sức chứa** | `capacity_max` | `20` | **Mới:** Sức chứa mở rộng theo công thức $10 + 2 \times successful\_lights$. |
| **Thời lượng đêm** | `night1_duration_s` | `240` s | Rút ngắn từ 300s xuống 240s để tăng nhịp độ căng thẳng. |
| | `night2_duration_s` | `270` s | Rút ngắn từ 330s xuống 270s. |
| | `night3_duration_s` | `300` s | Rút ngắn từ 360s xuống 300s. |
| **Luật Thắng Mới** | `win_ratio` | `0.6` (60%) | **Thay thế:** Bỏ thắng sớm `all_lit`. Thắng khi sống sót đến bình minh và số đèn sáng $\ge \lceil 0.6 \times \text{tổng đèn} \rceil$. |
| **Tính điểm** | Chuẩn hóa v1.2 | Điểm mới | Nạp đom đóm: `+5`. Thắp mới: `+100`. Thắp lại: `+40`. Choáng bóng mực: `+5` (đang drain: `+15`). Thắng: `+50 + floor(fuel)` mỗi đèn sáng + `50` mỗi Lửa. Bỏ thưởng thời gian. |

### B. Quyết định kỹ thuật quan trọng
1. **Tránh sai số dấu phẩy động:** Tính toán hao hụt dầu theo tỉ lệ mỗi tick ($1/60$ và $5/60$). Ngưỡng kiểm tra hết dầu được làm tròn với sai số $\le 10^{-5}$ để đảm bảo chuyển trạng thái đèn tắt dứt khoát.
2. **Cập nhật hồi quy kiểm thử:** Các test case cũ kỳ vọng chiến thắng tức thời khi thắp đủ 5 đèn được điều chỉnh sang kiểm thử điều kiện bình minh (`dawn_survived`) theo đúng [ADR-001](file:///d:/VinAI/prj/Day12/K5-L3A-DAY12-NguyenHuyGiang-2A202603543-AI-SDLC-Dao-Den-Long/docs/adr/ADR-001-fuel-and-dawn-win.md).
