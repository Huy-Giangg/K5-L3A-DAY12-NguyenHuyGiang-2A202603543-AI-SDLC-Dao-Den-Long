# Nhật Ký Thay Đổi (CHANGELOG)

Tất cả các thay đổi quan trọng và các thay đổi phá vỡ tương thích (Breaking Changes) qua từng phase được ghi lại tại đây.

---

## [Phase 3] - TICKET-03: Đèn Cạn Dầu (2026-11-20)

### ⚠ Thay Đổi Phá Vỡ Tương Thích (Breaking Changes)
1. **Bãi bỏ luật thắng sớm `all_lit`:**
   - Trước đây: Game kết thúc và chiến thắng ngay khi tất cả đèn lồng được thắp sáng.
   - Hiện tại: Thắp đủ toàn bộ đèn không kết thúc màn chơi. Người chơi phải duy trì bảo vệ đèn đến hết giờ (Bình minh).
   - Sự kiện `game_over` khi thắng đổi trường `reason` từ `"all_lit"` thành `"dawn_survived"`. `"all_lit"` không còn được sử dụng.
2. **Đèn lồng hao hụt dầu và có thể tắt:**
   - Trước đây: Đèn đã sáng thì sáng vĩnh viễn và không nhận thêm đom đóm.
   - Hiện tại: Đèn sáng có chỉ số `fuel` (tối đa 100), tự hao $1.0$/s. Khi `fuel <= 0`, đèn tắt hoàn toàn (`lit = False`, `fuel = 0`, `deposited = 0`), phát sự kiện `lantern_out`.
3. **Chi phí thắp lại được giảm:**
   - Đèn đã từng sáng (`ever_lit = True`) chỉ cần 5 đom đóm (`relight_cost = 5`) thay vì 10 đom đóm như lần đầu.
4. **Bóng Mực có trạng thái mới `drain`:**
   - Khi đèn có `fuel < 30`, đèn mất vùng an toàn. Bóng Mực ở trạng thái `wander` sẽ tiếp cận và chuyển sang `drain`, hút $5$ fuel/s liên tục.
5. **Thay đổi toàn bộ công thức tính điểm:**
   - Nạp đom đóm (thắp mới, thắp lại hoặc châm dầu): `+5` điểm/con.
   - Thắp lần đầu: `+100` điểm; Thắp lại: `+40` điểm.
   - Choáng Bóng Mực đang drain: `+15` điểm; Choáng bình thường: `+5` điểm.
   - Thắng bình minh: `+50 + floor(fuel)` mỗi đèn sáng + `50` mỗi Ngọn Lửa. Bỏ thưởng thời gian còn lại.
6. **Thời lượng các đêm rút ngắn:**
   - Đêm 1: 240s (trước là 300s); Đêm 2: 270s (trước là 330s); Đêm 3: 300s (trước là 360s).
7. **Nâng cấp Test Contract lên v1.2:**
   - Thêm các khóa tuning: `fuel_max`, `fuel_decay_per_s`, `fuel_per_mote`, `relight_cost`, `win_ratio`, `drain_per_s`, `low_fuel_threshold`, `capacity_max`.
   - Snapshot cập nhật: mỗi đèn thêm `fuel`, `ever_lit`, `relit_count`; player thêm `capacity`.
   - Sự kiện mới: `refuel`, `lantern_out`, `fuel_drain`, `lantern_lit {relight: bool}`.

---

## [Phase 2] - TICKET-02: Ba Hòn Đảo (2026-11-20)
- Nâng cấp Contract lên v1.1.
- Mở rộng 3 Đêm: Đêm 1 (Đảo Bến), Đêm 2 (Đảo Cau nối cầu tre), Đêm 3 (Đảo Chuông 3 tầng).
- Thêm kỹ năng Lướt (Dash), Nhảy (Jump), Bục Nhảy (Jump Pad), Gió Lạc (Drifter), Bùa Gió (Charm), Gió mạnh (Night 3), Rơi vực ($Y < -10$), Tạm dừng (Pause).

---

## [Phase 1] - PRD-0: Đảo Đèn Lồng (2026-11-20)
- Thiết lập Test Contract v1.0, chạy headless 60 tick/s độc lập.
- Gameplay cốt lõi Đêm 1: gom đom đóm, thắp 5 đèn, Bóng Mực truy đuổi, Tỏa Sáng.
