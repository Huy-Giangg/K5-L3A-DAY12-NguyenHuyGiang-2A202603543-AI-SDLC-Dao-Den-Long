# Đảo Đèn Lồng (Lantern Island 3D)

> **Dự án AI SDLC · Day 12**  
> **Sinh viên:** Nguyễn Huy Giang — **MSSV:** 2A202603543 — **Lớp:** K5-L3A  
> **Video Demo:** [Xem video demo tại đây](docs/demo/demo.mp4) *(hoặc đính kèm tại GitHub Release)*

---

## 1. Cài đặt và Khởi chạy (Tối đa 3 lệnh)

Dự án được xây dựng trên nền **Python 3.11+**, chạy đồng nhất trên Windows, macOS và Linux.

```bash
# 1. Cài đặt thư viện
pip install -r requirements.txt

# 2. Chạy kiểm thử tự động (31 test cases toàn diện)
pytest

# 3. Mở game 3D trực quan
python -m src.main
```

---

## 2. Chế độ Headless (Test Contract v1.2)

Để phục vụ việc kiểm thử và chấm tự động theo Test Contract v1.2:

```bash
python -m src.main --headless --seed 42 --night 1 --ticks 120 --out docs/proof/phase3_headless_proof.jsonl --snapshot-every 10
```

### Các tùy chọn tham số:
* `--seed <int>`: Khởi tạo bộ sinh số ngẫu nhiên (RNG seed) đảm bảo tính tất định 100%.
* `--night <1|2|3>`: Lựa chọn màn chơi:
  * **Đêm 1 (Đảo Bến):** Thời lượng 240s, 5 Đèn Lồng Lớn. Cần giữ sáng $\ge 3/5$ đèn đến bình minh để thắng.
  * **Đêm 2 (Đảo Cau):** Thời lượng 270s, 6 Đèn Lồng Lớn, 2 bục nhảy, Bùa Gió C1. Cần giữ sáng $\ge 4/6$ đèn.
  * **Đêm 3 (Đảo Chuông):** Thời lượng 300s, 7 Đèn Lồng Lớn, đảo 3 tầng, bục nhảy, 2 Bùa Gió C1 & C2, gió bão giật mỗi 30s. Cần giữ sáng $\ge 5/7$ đèn.
* `--scenario <path.json>`: Nạp kịch bản ban đầu (hỗ trợ `lanterns[].{lit, fuel, ever_lit}`, `player.successful_lights`, `shades[].target_lantern_id`).
* `--inputs <path.json>`: Nạp chuỗi thao tác phím theo tick (`move`, `jump`, `dash`, `interact`, `pulse`, `pause`).
* `--ticks <int>`: Số tick mô phỏng (tốc độ 60 tick/giây). Mô phỏng một Đêm đầy đủ (21.600 ticks) chỉ mất **~2.1 giây**.
* `--out <path.jsonl>`: File lưu kết quả snapshot và event định dạng JSON Lines v1.2.
* `--snapshot-every <int>`: Chu kỳ ghi snapshot (mặc định 10 tick).

---

## 3. Cách chơi & Điều khiển

| Phím | Hành động | Mô tả |
|---|---|---|
| **W, A, S, D** | Di chuyển | Mây chạy thu thập đom đóm. Tốc độ cơ bản 6.0 m/s (7.2 m/s khi có Bùa Gió). |
| **Space** | Nhảy (Jump) | Nhảy cao với vận tốc $7.0$ m/s, trọng lực $-20.0$ m/s$^2$. Chỉ nhảy khi chạm đất. |
| **Shift / J** | Lướt (Dash) | Lướt $14.0$ m/s trong $0.2$ s ($12$ ticks), hồi chiêu $1.5$ s ($90$ ticks). Khi có Bùa Gió: lướt không hồi chiêu. |
| **E** | Nạp & Châm dầu | - **Thắp mới:** Cần 10 đom đóm.<br>- **Thắp lại:** Đèn từng sáng chỉ cần 5 đom đóm.<br>- **Châm dầu:** Đèn đang sáng nạp thêm đom đóm (10 fuel/con, tối đa 100). |
| **Q / F** | Tỏa sáng (Pulse)| Tiêu tốn 3 đom đóm, làm choáng và đẩy lùi Bóng Mực trong bán kính 5m; đặc biệt đẩy lùi và hạ gục hành vi hút dầu của Bóng Mực (+15 điểm). |
| **Esc / P** | Tạm dừng | Đóng băng toàn bộ logic mô phỏng, mở menu Tạm dừng / Cài đặt / Chế độ mù màu. |

---

## 4. Cơ chế Nhiên liệu & Luật Thắng Mới (Phase 3)

* **Cơ chế Nhiên liệu (Fuel):**
  * Đèn sáng hao hụt tự nhiên $1.0$ đơn vị/giây. Khi `fuel <= 0`, đèn tắt (`lantern_out`).
  * Khi `fuel < 30`: Đèn mất vùng an toàn và nhấp nháy báo động; Bóng Mực sẽ tiếp cận và hút $5$ fuel/giây (`drain`).
* **Sức chứa mở rộng:** Sức chứa túi đom đóm ban đầu là 10, tự động mở rộng theo công thức:
  $$\text{Sức chứa} = \min(20, 10 + 2 \times \text{successful\_lights})$$
* **Luật Thắng Bình Minh (Dawn Survival):**
  * Bãi bỏ thắng sớm `all_lit`.
  * Chiến thắng khi sống sót đến bình minh (`time_left_s <= 0`) và giữ được ít nhất $60\%$ số đèn đang sáng (`dawn_survived`).
* **Tính điểm:**
  * Nạp đom đóm (thắp mới, thắp lại, châm dầu): `+5` điểm / con.
  * Thắp đèn lần đầu: `+100` điểm; Thắp lại: `+40` điểm.
  * Choáng Bóng Mực: `+5` điểm (nếu đang hút dầu: `+15` điểm).
  * Thưởng bình minh khi thắng: `+50 + floor(fuel)` cho mỗi đèn đang sáng, `+50` cho mỗi Ngọn Lửa sinh lực. Bỏ thưởng thời gian.

---

## 5. Minh chứng kiểm chứng (Proof of Verification)

* Ghi nhận quyết định kiến trúc: [docs/adr/ADR-001-fuel-and-dawn-win.md](docs/adr/ADR-001-fuel-and-dawn-win.md).
* Nhật ký thay đổi phá vỡ tương thích: [CHANGELOG.md](CHANGELOG.md).
* Báo cáo kiểm thử 31 test cases: [docs/proof/phase3_test_report.txt](docs/proof/phase3_test_report.txt).
* Mẫu log output headless Test Contract v1.2: [docs/proof/phase3_headless_proof.jsonl](docs/proof/phase3_headless_proof.jsonl).
* Tổng hợp giả định & số liệu chuẩn hóa: [docs/notes/assumptions.md](docs/notes/assumptions.md).
* Nhật ký SDLC & ước tính chi phí: [docs/notes/ai-log.md](docs/notes/ai-log.md).
* Phân tích hồi quy & Retrospective: [docs/notes/retro.md](docs/notes/retro.md).
