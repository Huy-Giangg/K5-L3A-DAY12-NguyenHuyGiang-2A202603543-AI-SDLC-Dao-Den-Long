# Giả định & Thiết kế (Assumptions & Design Choices)

Tài liệu này ghi lại toàn bộ các giả định hợp lý cho các điểm PRD-0 để ngỏ và các thông số cân bằng (`tuning`).

## 1. Phase 1 (PRD-0)

### A. Các thông số cân bằng (Tuning Parameters)
Các thông số được cấu hình đồng bộ giữa logic simulation và file `game.contract.json`:

| Thông số | Giá trị | Ý nghĩa & Giải thích |
|---|---|---|
| `player_speed` | `5.0` (m/s) | Tốc độ di chuyển cơ bản của Mây. |
| `carry_capacity` | `10` | Sức chứa đom đóm tối đa Mây có thể mang cùng lúc. |
| `lantern_cost` | `5` | Số đom đóm cần nạp để thắp sáng hoàn toàn một Đèn Lồng Lớn. |
| `lantern_count_night1` | `5` | Số lượng Đèn Lồng Lớn trên Đảo Bến ở Đêm 1 (L1 đến L5). |
| `pickup_radius` | `1.5` (m) | Bán kính nhặt đom đóm tính từ chân Mây. |
| `interact_radius` | `2.5` (m) | Bán kính tương tác để nạp đom đóm vào Đèn Lồng Lớn. |
| `pulse_cost` | `1` | Số đom đóm tiêu tốn mỗi lần kích hoạt kỹ năng Tỏa sáng (Pulse). |
| `pulse_radius` | `6.0` (m) | Bán kính tác dụng của đợt sóng tỏa sáng. |
| `pulse_stun_s` | `3.0` (s) | Thời gian làm choáng Bóng Mực khi trúng sóng tỏa sáng. |
| `pulse_push_m` | `3.0` (m) | Khoảng cách đẩy lùi Bóng Mực ra xa người chơi. |
| `pulse_cooldown_s` | `1.0` (s) | Thời gian hồi chiêu giữa hai lần tỏa sáng. |
| `night1_duration_s` | `300.0` (s) | Thời lượng Đêm 1 (5 phút = 18.000 ticks ở 60Hz). |
| `flames` | `3` | Số ngọn lửa đại diện cho sinh lực (máu) của Mây. |
| `invuln_s` | `2.0` (s) | Thời gian miễn nhiễm sát thương sau khi bị Bóng Mực tấn công. |
| `hit_drop_ratio` | `0.5` | Tỉ lệ đom đóm bị đánh rơi khi Mây bị trúng đòn (`floor(carried * 0.5)`). |
| `safe_radius` | `5.0` (m) | Bán kính an toàn quanh đèn đã thắp sáng; Bóng Mực bị đẩy lùi ra ngoài. |
| `shade_speed` | `3.2` (m/s) | Tốc độ di chuyển truy đuổi Mây của Bóng Mực. |
| `shade_hit_radius` | `1.0` (m) | Khoảng cách va chạm gây sát thương giữa Bóng Mực và Mây. |
| `fall_enabled` | `false` | Đảo có ranh giới bán kính 35m; Mây không bị rơi khỏi đảo. |

### B. Công thức tính điểm (Score System)
- Nhặt mỗi đom đóm: `+10` điểm (`per_mote`).
- Thắp sáng mỗi Đèn Lồng Lớn: `+200` điểm (`per_lantern`).
- Làm choáng mỗi Bóng Mực bằng Pulse: `+25` điểm (`per_stun`).
- Thưởng khi chiến thắng (`all_lit`):
  - `+5` điểm cho mỗi giây còn lại (`per_second_left`).
  - `+100` điểm cho mỗi ngọn lửa còn lại (`per_flame_left`).

### C. Quy ước hình học và không gian
- Không gian 3 chiều: Trục $Y$ hướng lên, mặt đất ở $Y = 0$.
- Mây xuất phát tại gốc tọa độ $(0, 0, 0)$.
- 5 Đèn Lồng Lớn được bố trí đều theo đường tròn bán kính 25m quanh đảo tại các góc $0^\circ, 72^\circ, 144^\circ, 216^\circ, 288^\circ$.
- Mọi khoảng cách được tính theo khoảng cách Euclid trên mặt phẳng ngang $XZ$ ($Y$ chỉ dùng cho hiển thị).
