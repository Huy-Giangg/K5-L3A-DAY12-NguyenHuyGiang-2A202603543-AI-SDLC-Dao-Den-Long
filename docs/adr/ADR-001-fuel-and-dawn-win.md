# ADR-001: Chuyển Đổi Trạng Thái Nhiên Liệu Đèn & Cơ Chế Thắng Bình Minh

- **Trạng thái:** Được chấp thuận (Accepted)
- **Ngày:** 2026-11-20
- **Phạm vi:** Phase 3 (TICKET-03 Change Request)
- **Người thực hiện:** Nguyễn Huy Giang (2A202603543)

---

## 1. Bối cảnh & Vấn đề (Context & Problem Statement)

Trong Phase 1 và Phase 2, luật chơi quy định:
- Đèn Lồng Lớn sau khi nạp đủ đom đóm sẽ sáng vĩnh viễn và không nhận thêm đom đóm.
- Người chơi thắng ngay lập tức (`all_lit`) khi thắp sáng được toàn bộ đèn lồng trên đảo.

Kết quả playtest cho thấy: Người chơi thành thạo có thể thắp hết đèn chỉ trong 2 phút đầu, khiến giai đoạn cuối đêm bị mất đi tính thử thách và căng thẳng. Khách hàng yêu cầu chuyển đổi mục tiêu cốt lõi từ **"thắp hết đèn"** sang **"bảo vệ và duy trì ánh sáng của hòn đảo tới bình minh"**.

---

## 2. Các quyết định thiết kế (Decision)

### A. Mô hình Trạng thái Đèn Lồng (Lantern State Model with Fuel)
1. **Nhiên liệu (Fuel):**
   - Đèn sáng có chỉ số nhiên liệu `fuel` (tối đa 100).
   - Khi vừa thắp sáng hoặc thắp lại: `fuel = 100.0`.
   - Đèn tự hao hụt tự nhiên với tốc độ $1.0$ đơn vị/giây ($1/60$ đơn vị mỗi tick).
   - Bổ sung cơ chế **Châm dầu (Refuel):** Khi đèn đang sáng và chưa đầy dầu (`fuel < 100`), người chơi có thể tương tác để nạp thêm đom đóm (`used = min(carried, ceil((100 - fuel) / 10))`), mỗi đom đóm hồi 10 fuel.
   - Khi `fuel <= 0`: Đèn tắt hoàn toàn (`lit = False`, `fuel = 0`, `deposited = 0`), phát sự kiện `lantern_out`, ghi nhớ cờ `ever_lit = True`.
2. **Chi phí Thắp lại (Relight Discount):**
   - Đèn thắp lần đầu: chi phí 10 đom đóm.
   - Đèn từng sáng rồi bị tắt (`ever_lit = True`): chi phí giảm xuống còn 5 đom đóm (`relight_cost = 5`). Phát sự kiện `lantern_lit {relight: true}`.

### B. Hành vi Bóng Mực: Hút Dầu (Oil Drain Mechanism)
- Khi đèn có `fuel < 30`: mất vùng an toàn 6m.
- Bóng Mực ở trạng thái `wander` sẽ ưu tiên tìm đến đèn sáng yếu (`fuel < 30`) gần nhất.
- Khi tiếp cận trong bán kính $\le 2$m, Bóng Mực chuyển sang trạng thái mới `drain`, đứng yên hút $5.0$ fuel/giây liên tục (cộng dồn nếu có nhiều bóng cùng hút).
- Khi người chơi Tỏa Sáng trúng Bóng Mực đang `drain`, người chơi nhận được $+15$ điểm (thay vì $+5$ điểm thông thường).

### C. Luật Thắng Bình Minh (Dawn Survival Victory)
- **Bãi bỏ hoàn toàn luật thắng sớm `all_lit`:** Thắp đủ 100% đèn không kết thúc màn chơi.
- **Điều kiện Thắng:** Mây sống sót đến khi hết giờ ($time\_left\_s \le 0$) và số đèn đang sáng tại tick cuối $\ge \lceil 0.6 \times \text{tổng đèn} \rceil$:
  - Đêm 1: $\ge 3/5$ đèn.
  - Đêm 2: $\ge 4/6$ đèn.
  - Đêm 3: $\ge 5/7$ đèn.
  - Lý do kết thúc thắng: `dawn_survived`.
- **Điều kiện Thua:** Cạn Ngọn Lửa (`no_flames` - thua ngay lập tức) hoặc hết giờ mà số đèn sáng $< 60\%$ (`dawn`).

---

## 3. Hậu quả & Đánh giá (Consequences)

- **Ưu điểm:**
  - Nhịp độ gameplay ở cuối đêm căng thẳng, đòi hỏi người chơi liên tục tuần tra, châm dầu và bảo vệ các ngọn đèn yếu khỏi Bóng Mực.
  - Tạo chiều sâu chiến thuật giữa việc gom đom đóm để mở rộng sức chứa ($10 + 2 \times successful\_lights$) so với việc giữ dầu cho các ngọn đèn chủ chốt.
- **Các thay đổi phá vỡ tương thích (Breaking Changes):**
  - Schema Test Contract nâng cấp lên v1.2.
  - Kịch bản test cũ mong đợi `all_lit` thắng sớm phải được cập nhật lại theo điều kiện bình minh `dawn_survived`.

