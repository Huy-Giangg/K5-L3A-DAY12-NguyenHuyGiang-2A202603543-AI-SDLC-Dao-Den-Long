# Đặc Tả Kỹ Thuật Phase 2 (TICKET-02: Ba Hòn Đảo)

Tài liệu này xác định chi tiết tiêu chí nghiệm thu (Acceptance Criteria - AC) cho các tính năng mới trong Phần 3 của Ticket-02 theo đúng Định nghĩa hoàn thành (DoD).

---

## 1. Gió Lạc (Drifters) - Đêm 2 & 3
### Tiêu chí nghiệm thu (AC):
- **AC 1.1 (Hình thái & Vận tốc):** Dải lụa xám xanh (`#8FA3B8`), bay lượn trên không trung. Vận tốc tuần tra `idle` $2.0$ m/s, vận tốc truy đuổi `chase` và tháo chạy `flee` là $7.0$ m/s.
- **AC 1.2 (Lịch sinh & Số lượng):** Tối đa 2 con đồng thời. Sinh tại tick $1200, 2400, \dots$ trên điểm sương. Định danh `D1, D2, ...`
- **AC 1.3 (Chuyển trạng thái):** 
  - `idle` $\to$ `chase`: khi Mây mang $\ge 5$ đom đóm và khoảng cách $d \le 15$ m.
  - `chase` $\to$ `idle`: khi Mây mang $< 5$ đom đóm hoặc khoảng cách $d > 15$ m.
- **AC 1.4 (Cướp đom đóm):** Khi chạm Mây ($XZ \le 1.2$ m): cướp $\min(3, \text{đang mang})$ đom đóm. Chuyển sang `flee` bay ra xa Mây trong 240 ticks rồi biến mất cùng số đã cướp. Mỗi con chỉ cướp 1 lần. Phát sự kiện `drifter_steal`.
- **AC 1.5 (Tương tác Tỏa Sáng):**
  - Tỏa Sáng trúng khi đang `chase`: Chuyển `flee` ngay lập tức mà không cướp đồ.
  - Tỏa Sáng trúng khi đang `flee` có mang đồ: Rơi toàn bộ số đom đóm đã cướp tại chỗ (thành đom đóm rơi `dropped` với TTL 480 ticks), phát sự kiện `drifter_drop`, biến mất sau 120 ticks.
- **AC 1.6 (Quy tắc an toàn):** Không làm mất Ngọn Lửa của Mây; vùng an toàn của đèn và trạng thái bất tử của Mây không ngăn cản Gió Lạc cướp đom đóm.

---

## 2. Bùa Gió (Charms)
### Tiêu chí nghiệm thu (AC):
- **AC 2.1 (Vị trí & Định danh):** Lá bùa đỏ viền vàng (`#C8102E` viền `#F2C14E`), định danh `C1, C2`. Vị trí: Đêm 2 tại $(35, 0, 0)$; Đêm 3 tại $(30, 0, 25)$ và $(-30, 0, 25)$.
- **AC 2.2 (Nhặt bùa):** Tương tác nhặt khi $XZ \le 1.0$ m và chênh cao $|Y_{player} - Y_{charm}| \le 1.5$ m. Phát sự kiện `charm_picked {"charm_id": cid, "charm_ticks": 600}`.
- **AC 2.3 (Hiệu lực 600 ticks):**
  - Tốc độ chạy của Mây tăng từ $6.0$ m/s lên $7.2$ m/s.
  - Lướt (Dash) không có thời gian hồi chiêu (vẫn cần bấm lại phím; bấm khi đang lướt bị bỏ qua; lướt vẫn $14.0$ m/s trong 12 ticks).
  - Nhặt lại bùa làm mới thời gian hiệu lực 600 ticks.
- **AC 2.4 (Hồi phục):** Bùa xuất hiện lại sau 2700 ticks ($45$ giây).

---

## 3. Chuỗi 3 Đêm & Vòng lặp trò chơi
### Tiêu chí nghiệm thu (AC):
- **AC 3.1 (Luồng chơi):** Menu chính $\to$ Giới thiệu Đêm (tên đảo, lời dẫn Ông Đăng) $\to$ Chơi màn $\to$ Màn hình kết quả $\to$ Chuyển tiếp Đêm kế tiếp.
- **AC 3.2 (Màn hình Bình Minh):** Hoàn thành chiến thắng Đêm 3 kích hoạt màn hình Bình Minh hiển thị tổng điểm tích lũy của cả 3 Đêm.
- **AC 3.3 (Thử lại):** Nếu thua ở bất kỳ Đêm nào, người chơi được chọn chơi lại ngay Đêm đó.

---

## 4. Tạm dừng (Pause / Resume)
### Tiêu chí nghiệm thu (AC):
- **AC 4.1 (Kích hoạt):** Phím `Esc` hoặc `P` (trong input: `pause: true`).
- **AC 4.2 (Đóng băng logic):** Khi tạm dừng, toàn bộ logic mô phỏng đóng băng: thời gian, hồi chiêu, trạng thái bóng mực, gió lạc, spawn, TTL đom đóm đều giữ nguyên.
- **AC 4.3 (Dữ liệu Contract):** Tick vẫn tăng, `sim_tick` đứng yên, snapshot ghi `state: "paused"`. Phát sự kiện `paused` khi dừng và `resumed` khi tiếp tục.
- **AC 4.4 (Giao diện):** Menu tạm dừng có các tùy chọn: Tiếp tục, Chơi lại Đêm, Cài đặt, Về menu chính.

---

## 5. Cài đặt (Settings)
### Tiêu chí nghiệm thu (AC):
- **AC 5.1 (Tham số):** Cung cấp thanh trượt điều chỉnh Âm lượng (Master Volume) và Độ nhạy chuột (Mouse Sensitivity).
- **AC 5.2 (Lưu trữ bền vững):** Các giá trị cấu hình được tự động lưu vào `localStorage` của trình duyệt và giữ nguyên giữa các phiên chơi.

---

## 6. Âm thanh (Audio System)
### Tiêu chí nghiệm thu (AC):
- **AC 6.1 (Nhạc nền):** Giai điệu đêm ấm áp, cổ tích bằng Web Audio API tổng hợp âm.
- **AC 6.2 (Hiệu ứng âm thanh đầy đủ):** Tạo âm thanh sống động cho các sự kiện: nhặt đom đóm, thắp đèn, tỏa sáng, bị đánh, nhảy, lướt, chiến thắng, thất bại, Bóng Mực xuất hiện, nhịp tim đếm ngược 10 giây cuối.

---

## 7. Giao diện HUD
### Tiêu chí nghiệm thu (AC):
- **AC 7.1 (Bố cục thông tin):**
  - Góc trên trái: 3 Ngọn Lửa sinh lực.
  - Góc trên giữa: Đồng hồ thời gian `mm:ss` (đổi màu đỏ `#FF5A5F` và nhấp nháy khi thời gian $\le 30$ s).
  - Góc trên phải: Tiến độ đèn $k/n$ và Điểm số.
  - Góc dưới giữa: Thanh chứa đom đóm 10 ô trực quan.
  - Góc dưới phải: Biểu tượng hồi chiêu Lướt và Tỏa Sáng.
- **AC 7.2 (Gợi ý tương tác):** Hiển thị nhắc nhở `E — Nạp ánh sáng (x/10)` khi đứng trong bán kính $2.0$ m quanh Đèn Lồng Lớn chưa sáng.
- **AC 7.3 (Mũi tên chỉ hướng):** Mũi tên định hướng trên màn hình chỉ về Đèn Lồng chưa sáng gần nhất khi đèn nằm ngoài tầm nhìn camera.

---

## 8. Bảng màu chuẩn (Palette Compliance)
### Tiêu chí nghiệm thu (AC):
- **AC 8.1 (Màu đối tượng):**
  - Trời đêm / sương: `#0E1430` / `#1B2350`
  - Cỏ / cát / gỗ / biển mây: `#2F5D50` / `#C9B48A` / `#6B4A2F` / `#12384A`
  - Đèn sáng / lõi / đèn tắt: `#FFB347` / `#FFE9B0` / `#5B5F6E`
  - Đom đóm lõi / quầng: `#FFF6C2` / `#FFE58A`
  - Bóng Mực thân / viền / bị choáng: `#120A1A` / `#7A3CFF` / `#3A3450`
  - Áo Mây / khăn Mây và Bùa Gió: `#E8E2D0` / `#C8102E`
  - Viền vàng, điểm số / Gió Lạc: `#F2C14E` / `#8FA3B8`
  - UI nguy hiểm / chữ UI: `#FF5A5F` / `#F5F1E6`
- **AC 8.2 (Cường độ ánh sáng động):**
  - Cường độ ánh sáng môi trường tính theo công thức:
    $$I = 0.15 + 0.55 \times \left(\frac{\text{đèn sáng}}{\text{tổng đèn}}\right)$$
