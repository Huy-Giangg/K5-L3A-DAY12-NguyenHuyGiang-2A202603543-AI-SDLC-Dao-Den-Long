# Đánh giá & Retro (Retrospective)

---

## Đánh giá Phase 1 (PRD-0) & Phase 2 (TICKET-02)
*(Xem chi tiết tại các tag `phase-1` và `phase-2`)*
- Hoàn thành đầy đủ lõi engine, giao diện 3D và Test Contract v1.0, v1.1.
- Xây dựng 24 unit & scenario tests ban đầu.

---

## Đánh giá Phase 3 (TICKET-03: Đèn Cạn Dầu)

### 1. Những gì đạt được
- **Chuyển đổi thành công kiến trúc mô phỏng theo Change Request:**
  - Triển khai mô hình nhiên liệu đèn lồng hoàn chỉnh: đèn sáng tự tiêu hao $1.0$/s, có thể được châm dầu, tắt đèn khi hết dầu, và nhớ trạng thái để thắp lại với chi phí giảm còn 5 đom đóm.
  - Hành vi Bóng Mực hút dầu (`drain`) hoạt động mượt mà: nhận diện đèn yếu (`fuel < 30`) mất vùng an toàn, tiếp cận $\le 2$m và hút $5$ fuel/s, phát sự kiện `fuel_drain` mỗi 60 ticks.
  - Luật thắng mới được kích hoạt chuẩn xác tại thời điểm bình minh: kiểm tra tỉ lệ đèn sáng $\ge 60\%$, phát sự kiện `game_over {"reason": "dawn_survived"}`.
  - Sức chứa túi đom đóm mở rộng động theo số lần thắp đèn thành công ($10 + 2 \times successful\_lights$, trần 20).
- **Tuân thủ quy trình SDLC khi có Breaking Changes:**
  - Có tài liệu kiến trúc [ADR-001](file:///d:/VinAI/prj/Day12/K5-L3A-DAY12-NguyenHuyGiang-2A202603543-AI-SDLC-Dao-Den-Long/docs/adr/ADR-001-fuel-and-dawn-win.md) giải trình chi tiết lý do và giải pháp.
  - Có file [CHANGELOG.md](file:///d:/VinAI/prj/Day12/K5-L3A-DAY12-NguyenHuyGiang-2A202603543-AI-SDLC-Dao-Den-Long/CHANGELOG.md) liệt kê rõ ràng các điểm phá vỡ tương thích.
  - Không có bất kỳ test nào bị skip âm thầm. Test cũ `test_game_over_win` được cập nhật kèm ghi chú giải thích luật thắng mới.
- **Kiểm thử tự động đạt 31/31 passed 100% trong ~1.9 giây.**

### 2. Phân tích lỗi & Cách phát hiện
- **Lỗi sai số dấu phẩy động (Floating point precision):** Khi trừ dầu mỗi tick ($1/60$), giá trị nhiên liệu bị dư lại $6.9 \times 10^{-18} > 0$ khiến đèn không chuyển sang tắt đúng lúc.
  * **Giải pháp:** Sử dụng ngưỡng sai số epsilon $10^{-5}$ (`if L.fuel <= 1e-5:`) khi kiểm tra hết dầu, đảm bảo tính tất định và chuyển trạng thái dứt khoát.
