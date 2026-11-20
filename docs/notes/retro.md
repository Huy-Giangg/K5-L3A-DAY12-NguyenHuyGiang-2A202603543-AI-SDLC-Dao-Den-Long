# Đánh giá & Retro (Retrospective)

## Đánh giá Phase 1 (PRD-0)

### 1. Những gì đạt được
- **Đạt chuẩn Test Contract v1.0:**
  - Có file `game.contract.json` đầy đủ các tham số tuning.
  - Tham số dòng lệnh headless nhận đúng các cờ `--seed`, `--night 1`, `--ticks`, `--out`, `--scenario`, `--inputs`, `--snapshot-every`.
  - Tính tất định (Determinism): Chạy 2 lần cùng seed và input cho kết quả JSONL khớp 100%.
  - Mã thoát: Thoát mã 0 khi hoàn thành, thoát mã 2 khi file input/scenario sai format.
  - Đạt 15/15 test cases tự động (`pytest`).
- **Chất lượng sản phẩm trực quan:**
  - Trò chơi 3D mượt mà trên trình duyệt, không yêu cầu cài đặt driver đồ họa phức tạp trên hệ điều hành.
  - Bầu không khí đêm huyền ảo, đèn lồng phát sáng vàng cam ấm, sương mù và bóng mực tím đen đúng yêu cầu nghệ thuật trong PRD-0.
  - HUD trực quan đầy đủ: thời gian đếm ngược, máu/lửa, đom đóm mang theo, số đèn đã thắp, điểm số.

### 2. Các điểm cần lưu ý & Cải tiến cho Phase 2
- Ở Phase 2 (Ticket-02), các yêu cầu mới có thể bổ sung thêm chủng loại bóng mực hoặc cơ chế mới. Kiến trúc của `SimulationEngine` đã sẵn sàng mở rộng các list entity mà không phá vỡ logic cũ.
- File `AGENTS.md` hoạt động hiệu quả giúp agent luôn tuân thủ nguyên tắc chạy headless và kiểm thử trước khi nộp.
