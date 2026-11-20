# Nhật ký sử dụng AI (AI Usage Log)

Theo dõi việc sử dụng công cụ AI, quản lý ngữ cảnh, ước tính token và chi phí qua từng phase.

---

## CP0: Khởi tạo và thiết lập dự án
- **Model:** Gemini 3.8 Flash
- **Hoạt động:** Khởi tạo cấu trúc dự án, harness ban đầu.
- **Ước tính token:** ~8.000 tokens. Chi phí: ~$0.003 USD.

---

## CP1: Phase 1 (PRD-0)
- **Model:** Gemini 3.8 Flash
- **Hoạt động:** Lõi mô phỏng headless 60Hz, Test Contract v1.0, 15 test cases, giao diện 3D WebGL Three.js.
- **Ước tính token:** ~35.000 tokens. Chi phí: ~$0.015 USD.

---

## CP2: Phase 2 (TICKET-02: Ba Hòn Đảo)
- **Model:** Gemini 3.8 Flash
- **Hoạt động:** Chuẩn hóa số liệu, mở rộng 3 Đêm, kỹ năng Lướt, Nhảy, Gió Lạc, Bùa Gió, Test Contract v1.1, nâng lên 24 test cases.
- **Ước tính token:** ~45.000 tokens. Chi phí: ~$0.020 USD.

---

## CP3: Phase 3 (TICKET-03: Đèn Cạn Dầu)
- **Model:** Gemini 3.8 Flash
- **Hoạt động:**
  - Tiếp nhận và phân tích Change Request cốt lõi Ticket-03 (Breaking Changes).
  - Soạn thảo Architectural Decision Record [ADR-001](../adr/ADR-001-fuel-and-dawn-win.md) ghi nhận quyết định thay đổi mô hình trạng thái đèn và luật thắng.
  - Thiết lập [CHANGELOG.md](../../CHANGELOG.md) liệt kê đầy đủ các thay đổi phá vỡ tương thích.
  - Nâng cấp Test Contract lên v1.2: cơ chế hao dầu ($1.0$/s), châm dầu (`refuel`), tắt đèn (`lantern_out`), thắp lại giá rẻ (`relight_cost: 5`), Bóng Mực hút dầu (`drain` / `fuel_drain`), sức chứa tăng dần ($10 + 2 \times successful\_lights$), luật thắng bình minh `dawn_survived` ($\ge 60\%$ đèn sáng).
  - Cập nhật test cũ bị ảnh hưởng có ghi chú lý do rõ ràng, bổ sung test scenarios mới nâng tổng số lên **31 test cases** (đạt 100% pass).
  - Cập nhật giao diện web trực quan: hiển thị thanh dầu, nhấp nháy đèn yếu, cài đặt chế độ mù màu.
- **Chiến lược tiết kiệm token:**
  - Áp dụng kỹ thuật phân tích sự khác biệt (diff analysis) giữa v1.1 và v1.2 trước khi code.
  - Gom các thay đổi liên quan đến model, engine, runner và tests vào các thao tác tập trung.
- **Ước tính token:** ~42.000 tokens. Chi phí: ~$0.018 USD.

---

## CP4: Phase 4 (TICKET-04: Bình Minh Phát Hành v1.0.0)
- **Model:** Gemini 3.8 Flash
- **Hoạt động:**
  - Nâng cấp Test Contract lên v1.3: bổ sung lệnh kiểm thử phi chức năng `bench_cmd` và `soak_cmd`.
  - Xây dựng mô đun Benchmark (`src/core/bench.py`): kiểm thử tải nặng (200 shades, 100 motes, camera orbit) tính toán tự động `avg_fps`, `p1_low_fps`, `frame_ms_p95`, `peak_mem_mb`, sinh tệp `bench.json` đạt 183.8 FPS.
  - Xây dựng mô đun Soak Test (`src/core/soak.py`): chạy 10 đêm liên tục xoay vòng 1->2->3, đo đạc bộ nhớ bằng `psutil`, sinh tệp `soak.json` đạt 0 crash và chênh lệch RAM chỉ 1MB (24MB -> 25MB, không rò rỉ).
  - Xây dựng hệ thống Bảng xếp hạng Top 10 (`src/core/leaderboard.py`): lưu trữ JSON, sắp xếp theo điểm số, hỗ trợ lệnh xuất CLI `--export-leaderboard <path>`.
  - Bổ sung trọn bộ tính năng Dễ tiếp cận (Accessibility): Key rebinding tùy biến phím có cơ chế phát hiện và ngăn trùng phím, nút khôi phục mặc định, chế độ giảm chuyển động (Reduced Motion), phông chữ lớn (Large Text UI scale 1.25x), chỉ báo hình ảnh / phụ đề trực quan (Visual Subtitles).
  - Bổ sung bộ kiểm thử `tests/test_phase4_features.py`, nâng tổng số test cases lên **36 tests passed 100%**.
  - Hoàn thiện tệp video demo `docs/demo/demo.mp4`, kịch bản `docs/demo/README.md`, báo cáo tổng kết 4 phase `docs/notes/retro.md`.
- **Ước tính token:** ~48.000 tokens. Chi phí: ~$0.021 USD.
- **TỔNG KẾT TOÀN DỰ ÁN (Phase 1 — Phase 4):**
  - **Tổng lượng token sử dụng:** ~178.000 tokens.
  - **Tổng chi phí API ước tính:** ~$0.077 USD (< $0.10 USD — siêu tối ưu và tiết kiệm).
