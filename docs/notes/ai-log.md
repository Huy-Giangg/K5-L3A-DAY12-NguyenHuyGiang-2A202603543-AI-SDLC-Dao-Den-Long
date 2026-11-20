# Nhật ký sử dụng AI (AI Usage Log)

Theo dõi việc sử dụng công cụ AI, quản lý ngữ cảnh, ước tính token và chi phí qua từng phase.

---

## CP0: Khởi tạo và thiết lập dự án
- **Model:** Gemini 3.8 Flash
- **Hoạt động:**
  - Khởi tạo repo, cấu trúc thư mục chuẩn theo `SUBMISSION.md`.
  - Khai báo file quy chuẩn `AGENTS.md`, `CREDITS.md`, `LICENSE`, `requirements.txt`.
- **Ước tính token:** ~8.000 tokens.
- **Ước tính chi phí:** ~$0.003 USD.

---

## CP1: Phase 1 (PRD-0)
- **Model:** Gemini 3.8 Flash
- **Hoạt động:**
  - Phân tích tài liệu PDF 6 trang `Dao_Den_Long_Phase1_PRD0.pdf`.
  - Thiết kế kiến trúc Decoupled: `src/core/` (Simulation engine 60Hz) và `src/web/` (Giao diện 3D WebGL Three.js).
  - Khai báo cấu hình bắt buộc `game.contract.json` theo Test Contract v1.0.
  - Xây dựng 15 test cases tự động (`pytest`) và chế độ headless CLI.
- **Ước tính token:** ~35.000 tokens.
- **Ước tính chi phí:** ~$0.015 USD.

---

## CP2: Phase 2 (TICKET-02: Ba Hòn Đảo)
- **Model:** Gemini 3.8 Flash
- **Hoạt động:**
  - Đọc và phân tích toàn diện tài liệu PDF 6 trang `Dao_Den_Long_Phase2_TICKET02.pdf`.
  - Nâng cấp `game.contract.json` lên Test Contract v1.1 với toàn bộ số liệu chuẩn hóa (`dash_speed`, `dash_duration_s`, `dash_cooldown_s`, `night2_duration_s`, `night3_duration_s`, `fall_enabled: true`).
  - Thiết kế và triển khai mở rộng 3 Đêm: Đêm 1 (Đảo Bến), Đêm 2 (Đảo Cau 2 đảo nối cầu tre + 2 bục nhảy + Bùa Gió C1), Đêm 3 (Đảo Chuông 3 tầng + bục nhảy + dốc + 2 Bùa Gió C1, C2 + gió mạnh).
  - Bổ sung các cơ chế mới: Lướt (Dash), Nhảy (Jump), Gió Lạc (Drifter cướp đom đóm / Pulse rơi đồ), Bùa Gió (tăng tốc độ, bỏ hồi chiêu lướt), Rơi khỏi đảo ($Y < -10$), Tạm dừng (Pause / Resume).
  - Tối ưu hiệu năng headless: Chạy 21.600 ticks chỉ mất 2.1 giây (vượt xa yêu cầu $\le 30$ giây của DoD).
  - Viết tài liệu đặc tả kỹ thuật nghiệm thu `docs/spec_phase2.md`.
  - Mở rộng bộ test lên 24 test cases, đạt 100% pass.
- **Chiến lược tiết kiệm token:**
  - Lập trình tích hợp song song các file module models, engine, runner.
  - Phân tích chính xác nguyên nhân lỗi hồi quy test cũ (đẩy lùi chia 15 ticks) và xử lý ngay tại turn đầu mà không tốn các vòng lặp thử sai.
- **Ước tính token:** ~45.000 tokens.
- **Ước tính chi phí:** ~$0.020 USD.
- **Tổng chi phí ước tính đến hết Phase 2:** ~$0.038 USD.
