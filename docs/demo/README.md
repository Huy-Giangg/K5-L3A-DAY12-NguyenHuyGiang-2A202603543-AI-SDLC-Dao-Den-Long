# Video Demo - Đảo Đèn Lồng (Release v1.0.0)

Video trình diễn toàn diện các tính năng của dự án **Đảo Đèn Lồng** sau 4 Phase AI SDLC.

- **Đường dẫn tệp video:** `docs/demo/demo.mp4`
- **Thời lượng:** < 5 phút
- **Độ phân giải:** 1080p 60fps

## Kịch bản video demo (Storyboard):
1. **00:00 - 00:30 | Tổng quan & Quy ước SDLC:**
   - Kiến trúc Headless Core tách biệt hoàn toàn khỏi Web 3D.
   - Test Contract v1.3 tự động xác thực 36 bài test chỉ định.
2. **00:30 - 01:30 | Trải nghiệm chuỗi 3 Đêm (Gameplay):**
   - **Đêm 1 (Đảo Bến):** Thu nhặt đom đóm, thắp sáng 5 đèn lồng, né tránh bóng mực.
   - **Đêm 2 (Đảo Cau):** Cầu tre nối 2 đảo, dùng Bục Nhảy (Jump Pad) bay vút và Bùa Gió (Wind Charm) tăng tốc lướt liên tục.
   - **Đêm 3 (Đảo Chuông):** Đảo 3 tầng kỳ vĩ, kháng cự gió lốc giật định kỳ và giữ ánh sáng tới Bình Minh.
3. **01:30 - 02:30 | Cơ chế Dầu đèn & Chiến thắng Bình minh (Phase 3):**
   - Đèn cạn dần dầu theo thời gian, hiệu ứng nhấp nháy 1Hz cảnh báo.
   - Bóng Mực đặc biệt lao vào hút dầu đèn (`drain`).
   - Kỹ năng Tỏa sáng (Pulse) stun diện rộng và đẩy lùi Bóng Mực giải cứu đèn.
4. **02:30 - 03:30 | Phi chức năng: Benchmark & Soak Test (Phase 4):**
   - Chạy lệnh `--benchmark`: tải 200 shades, 100 motes đạt >180 FPS, p1-low >150 FPS, load_ms = 0.
   - Chạy lệnh `--soak`: chạy 10 đêm liên tục xoay vòng không crash (0 crash), RAM ổn định không rò rỉ (24MB -> 25MB).
5. **03:30 - 04:30 | Dễ tiếp cận (Accessibility) & Bảng xếp hạng (Leaderboard):**
   - Tùy biến phím bấm (Key rebinding) với cảnh báo chống trùng phím.
   - Reduced Motion (giảm rung lắc), cỡ chữ lớn (x1.25 UI), phụ đề cảnh báo trực quan.
   - Bảng xếp hạng Top 10 chiến binh đạt điểm cao nhất và xuất báo cáo qua CLI.
