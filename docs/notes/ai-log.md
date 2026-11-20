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
  - Soạn thảo Architectural Decision Record [ADR-001](file:///d:/VinAI/prj/Day12/K5-L3A-DAY12-NguyenHuyGiang-2A202603543-AI-SDLC-Dao-Den-Long/docs/adr/ADR-001-fuel-and-dawn-win.md) ghi nhận quyết định thay đổi mô hình trạng thái đèn và luật thắng.
  - Thiết lập [CHANGELOG.md](file:///d:/VinAI/prj/Day12/K5-L3A-DAY12-NguyenHuyGiang-2A202603543-AI-SDLC-Dao-Den-Long/CHANGELOG.md) liệt kê đầy đủ các thay đổi phá vỡ tương thích.
  - Nâng cấp Test Contract lên v1.2: cơ chế hao dầu ($1.0$/s), châm dầu (`refuel`), tắt đèn (`lantern_out`), thắp lại giá rẻ (`relight_cost: 5`), Bóng Mực hút dầu (`drain` / `fuel_drain`), sức chứa tăng dần ($10 + 2 \times successful\_lights$), luật thắng bình minh `dawn_survived` ($\ge 60\%$ đèn sáng).
  - Cập nhật test cũ bị ảnh hưởng có ghi chú lý do rõ ràng, bổ sung test scenarios mới nâng tổng số lên **31 test cases** (đạt 100% pass).
  - Cập nhật giao diện web trực quan: hiển thị thanh dầu, nhấp nháy đèn yếu, cài đặt chế độ mù màu.
- **Chiến lược tiết kiệm token:**
  - Áp dụng kỹ thuật phân tích sự khác biệt (diff analysis) giữa v1.1 và v1.2 trước khi code.
  - Gom các thay đổi liên quan đến model, engine, runner và tests vào các thao tác tập trung.
- **Ước tính token:** ~42.000 tokens.
- **Ước tính chi phí:** ~$0.018 USD.
- **Tổng chi phí ước tính đến hết Phase 3:** ~$0.056 USD.
