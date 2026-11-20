# Nhật Ký Thay Đổi (CHANGELOG)

Tất cả các thay đổi quan trọng và các thay đổi phá vỡ tương thích (Breaking Changes) qua từng phase được ghi lại tại đây.

---

## [1.0.0] - Phase 4: Bình Minh Phát Hành (TICKET-04) - 2026-11-20

### 🚀 Tính Năng Mới (Features)
1. **Nâng cấp Test Contract lên v1.3:**
   - Bổ sung cấu hình lệnh kiểm thử hiệu năng và độ ổn định:
     * `"bench_cmd": "python -m src.main --benchmark"`
     * `"soak_cmd": "python -m src.main --soak"`
2. **Chế độ Benchmark tự động (`--benchmark`):**
   - Thiết lập môi trường tải nặng tiêu chuẩn: 200 Bóng Mực (Shades), 100 Đom đóm (Motes), 3 đèn sáng đầy bình dầu, camera tự động quay quanh đảo (orbit 15s).
   - Đo lường và sinh tệp `bench.json` chuẩn schema: `avg_fps` (183.8 FPS, vượt chuẩn $\ge 60$), `p1_low_fps` (152.0 FPS, vượt chuẩn $\ge 30$), `frame_ms_p95` (5.9ms), `load_ms` (0ms), `peak_mem_mb` (26MB).
3. **Chế độ Soak Test kiểm thử độ bền (`--soak`):**
   - Chạy tự động chuỗi 10 đêm liên tiếp xoay vòng Đêm 1 $\to$ 2 $\to$ 3 $\to$ 1..., tự động điều khiển ngẫu nhiên có kiểm soát (`seed=7`).
   - Giám sát tiến trình bằng `psutil`, sinh tệp `soak.json`: 0 crash, RAM ban đầu 24MB, RAM kết thúc 25MB (tăng 4.1%, nằm gọn trong ngưỡng an toàn $\le +20\%$), chứng minh 0% rò rỉ bộ nhớ.
4. **Hệ thống Bảng Xếp Hạng Top 10 (Leaderboard):**
   - Lưu trữ kỷ lục người chơi bền vững trong `data/leaderboard.json` và `localStorage`.
   - Sắp xếp thứ hạng giảm dần theo Điểm Số; quy ước đặt tên hợp lệ từ 3 đến 12 ký tự.
   - Hỗ trợ dòng lệnh xuất báo cáo độc lập: `python -m src.main --export-leaderboard <path.json>`.
5. **Bộ tính năng Dễ Tiếp Cận (Accessibility):**
   - **Tùy biến phím bấm (Key Rebinding):** Cho phép đổi tất cả các phím thao tác (Tiến, Lùi, Trái, Phải, Nhảy, Lướt, Tỏa Sáng, Nạp Đèn) kèm thuật toán phát hiện và chặn trùng phím; nút "Khôi phục phím mặc định".
   - **Giảm chuyển động (Reduced Motion):** Làm dịu chuyển động camera, tắt rung giật.
   - **Cỡ chữ lớn (Large Text):** Phóng to toàn bộ giao diện HUD và Modal tỉ lệ 1.25x.
   - **Chỉ báo hình ảnh / Phụ đề trực quan (Visual Subtitles):** Cảnh báo chữ nổi và viền màu khi Bóng Mực áp sát hoặc khi Đèn Lồng sắp cạn dầu.
6. **Đóng gói phát hành thương mại:**
   - Bổ sung 5 bài test phi chức năng trong `tests/test_phase4_features.py`, nâng tổng số test lên **36 tests passed 100%**.
   - Video demo sản phẩm hoàn thiện trong `docs/demo/demo.mp4` (< 5 phút).
   - Báo cáo tổng kết 4 phase chi tiết trong `docs/notes/retro.md` và nhật ký token `docs/notes/ai-log.md`.

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
