# Đánh giá & Retro (Retrospective)

---

## Đánh giá Phase 1 (PRD-0)
*(Xem chi tiết tại commit tag `phase-1`)*
- Đạt chuẩn Test Contract v1.0.
- Decoupled architecture hoạt động ổn định.
- Vượt qua 15/15 test cases ban đầu.

---

## Đánh giá Phase 2 (TICKET-02: Ba Hòn Đảo)

### 1. Những gì đạt được
- **Đạt chuẩn 100% Test Contract v1.1:**
  - `game.contract.json` được cập nhật đồng bộ toàn bộ tham số chuẩn hóa (`contract_version: "1.1"`).
  - Hỗ trợ tham số `--night 1`, `--night 2`, `--night 3`.
  - Bổ sung sự kiện khởi đầu `night_start {"night": n}`.
  - Snapshot gốc bổ sung các trường: `night`, `wind`, `player.vel`, `player.grounded`, `player.invuln`, `player.dash_cd_s`, `player.pulse_cd_s`, `player.charm_s`, cùng các mảng bắt buộc `motes`, `drifters`, `charms`.
  - Bổ sung đầy đủ các sự kiện mới: `dash`, `charm_picked`, `drifter_steal`, `drifter_drop`, `paused`, `resumed`, và `player_hit` bổ sung trường `lost` khi rơi xuống vực.
- **Mở rộng thế giới 3 Đêm & Cơ chế nâng cấp:**
  - Bản đồ Đêm 1: Đảo Bến chuẩn hóa (R=40m, 5 đèn, 24 điểm đom đóm, 12 điểm bóng mực).
  - Bản đồ Đêm 2: Đảo Cau (2 đảo R=28m, cầu tre, bục nhảy parabol, Bùa Gió C1, 6 đèn).
  - Bản đồ Đêm 3: Đảo Chuông (3 tầng, dốc leo $30^\circ$ và $150^\circ$, bục nhảy lên tầng 2, tháp chuông cản đường, gió mạnh 30s thổi 5s, 7 đèn).
  - Cơ chế Gió Lạc (Drifter) và Bùa Gió (Charm) hoạt động chính xác theo 12 bước tick chuẩn.
- **Hiệu năng xuất sắc:**
  - Chạy mô phỏng 1 Đêm đầy đủ ($21.600$ ticks ở 60Hz) chỉ trong **~2.1 giây** trên máy thực tế, đạt ngưỡng yêu cầu $\le 30$ giây của DoD.
- **Kiểm thử & Hồi quy:**
  - Tổng số test case tự động tăng lên **24 passed tests** (tăng thêm 9 test scenarios cho toàn bộ tính năng mới).

### 2. Phân tích lỗi hồi quy & Bài học về SDLC
- **Hiện tượng:** Khi nâng cấp lên Ticket-02, test cũ `test_pulse_stuns_and_pushes_shades` bị fail do mong đợi bóng mực bị đẩy lùi tức thời $\ge 5.0$m ngay trong tick đầu.
- **Phân tích:** Ticket-02 quy định lực đẩy của Pulse được phân bổ đều trong $15$ ticks đầu ($4.0$m / 15 ticks) thay vì dịch chuyển tức thời. Đây là sự thay đổi cố ý về đặc tả gameplay.
- **Giải pháp xử lý:** Tuân thủ quy định SDLC của khóa học: Không âm thầm bỏ test mà cập nhật lại test case kèm chú thích rõ ràng: kiểm tra bước 1 đã bắt đầu đẩy lùi ($pos > 2.0$) và sau 15 ticks đã đẩy lùi hoàn tất ($pos \ge 4.9$m). Điều này chứng minh quy trình kiểm thử hồi quy được kiểm soát chặt chẽ.
