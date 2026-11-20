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

# 2. Chạy kiểm thử tự động (24 test cases toàn diện)
pytest

# 3. Mở game 3D trực quan (Hỗ trợ chuỗi 3 Đêm)
python -m src.main
```

---

## 2. Chế độ Headless (Test Contract v1.1)

Để phục vụ việc kiểm thử và chấm tự động theo Test Contract v1.1:

```bash
python -m src.main --headless --seed 42 --night 1 --ticks 120 --out docs/proof/phase2_headless_proof.jsonl --snapshot-every 10
```

### Các tùy chọn tham số:
* `--seed <int>`: Khởi tạo bộ sinh số ngẫu nhiên (RNG seed) đảm bảo tính tất định 100%.
* `--night <1|2|3>`: Lựa chọn màn chơi:
  * **Đêm 1 (Đảo Bến):** Đảo tròn $R=40$m, 5 Đèn Lồng Lớn.
  * **Đêm 2 (Đảo Cau):** 2 đảo tròn $R=28$m nối cầu tre, 2 bục nhảy, Bùa Gió C1, 6 Đèn Lồng.
  * **Đêm 3 (Đảo Chuông):** Đảo 3 tầng (Y=0, Y=3, Y=6), 2 dốc leo, bục nhảy lên tầng 2, tháp chuông, 2 Bùa Gió C1, C2, gió mạnh mỗi 30s, 7 Đèn Lồng.
* `--scenario <path.json>`: Nạp kịch bản tình huống ban đầu (hỗ trợ `player.{invuln_ticks, dash_cd_ticks, pulse_cd_ticks, charm_ticks}`, `drifters`, `charms`, `wind_enabled`).
* `--inputs <path.json>`: Nạp chuỗi thao tác phím theo tick (hỗ trợ `move`, `jump`, `dash`, `interact`, `pulse`, `pause`).
* `--ticks <int>`: Số tick mô phỏng (tốc độ chuẩn 60 tick/giây). Mô phỏng một Đêm đầy đủ (21.600 ticks) chỉ trong **~2.1 giây** (vượt xa yêu cầu $\le 30$s của DoD).
* `--out <path.jsonl>`: File lưu kết quả snapshot và event định dạng JSON Lines.
* `--snapshot-every <int>`: Chu kỳ ghi snapshot (mặc định 10 tick).

---

## 3. Cách chơi & Điều khiển

| Phím | Hành động | Mô tả |
|---|---|---|
| **W, A, S, D** | Di chuyển | Mây chạy khắp đảo thu thập đom đóm (tối đa mang 10 con). Tốc độ 6.0 m/s (tăng lên 7.2 m/s khi có Bùa Gió). |
| **Space** | Nhảy (Jump) | Nhảy cao với vận tốc $7.0$ m/s, trọng lực $-20.0$ m/s$^2$. Chỉ nhảy khi chạm đất. |
| **Shift / J** | Lướt (Dash) | Lướt nhanh $14.0$ m/s trong $0.2$ s ($12$ ticks), hồi chiêu $1.5$ s ($90$ ticks). Khi có Bùa Gió: lướt không hồi chiêu. |
| **E** | Nạp đom đóm | Đến gần Đèn Lồng Lớn ($\le 2.0$m) để thắp sáng (cần 10 con/đèn, nạp nhiều lần được). |
| **Q / F** | Tỏa sáng (Pulse)| Tiêu tốn 3 đom đóm, hồi chiêu 3.0s. Làm choáng Bóng Mực trong bán kính 5.0m trong 120 ticks và đẩy lùi 4.0m trong 15 ticks đầu; khiến Gió Lạc đang bỏ chạy phải thả lại đom đóm đã cướp. |
| **Esc / P** | Tạm dừng (Pause)| Đóng băng toàn bộ thế giới mô phỏng, mở menu tạm dừng. |
| **Chuột (kéo)**| Xoay camera | Điều chỉnh góc nhìn 3D bao quát hòn đảo. |

---

## 4. Cách tính điểm (Chuẩn hóa v1.1)

* **Nạp mỗi đom đóm vào đèn:** `+10` điểm (`per_mote`).
* **Thắp sáng mỗi Đèn Lồng Lớn:** `+100` điểm (`per_lantern`).
* **Mỗi Bóng Mực trúng Tỏa Sáng:** `+5` điểm (`per_stun`).
* **Thưởng khi Chiến thắng (`all_lit`):**
  * `+2` điểm $\times \lfloor\text{giây còn lại}\rfloor$.
  * `+50` điểm $\times \text{Ngọn Lửa sinh lực còn giữ được}$.
* **Tổng điểm game:** Tổng điểm các Đêm đã vượt qua.

---

## 5. Sáng tạo của tôi (Creative Highlights)

* **Thiết kế Thế giới 3 Đêm hoàn chỉnh:**
  * **Đêm 1:** Đảo Bến huyền ảo giữa biển mây.
  * **Đêm 2:** Đảo Cau với cầu tre không lan can đầy thử thách và 2 bục nhảy trợ lực vượt đảo.
  * **Đêm 3:** Đảo Chuông đa tầng với 2 đường dốc nghiêng $30^\circ$, bục phóng lên tầng cao và các đợt gió lớn bất ngờ.
* **Hệ thống Thực thể Mới sống động:**
  * **Gió Lạc (Drifter):** Dải lụa bay lượn trên không, rình rập cướp đom đóm của người chơi khi mang nhiều hơn 5 con; có thể bị người chơi chặn đứng và đòi lại đom đóm bằng chiêu Tỏa Sáng.
  * **Bùa Gió (Wind Charm):** Lá bùa linh thiêng đỏ viền vàng giúp Mây gia tăng tốc độ và lướt liên tục không giới hạn hồi chiêu.
* **Đồ họa chuẩn Palette & Âm thanh Procedural:** Ánh sáng môi trường biến chuyển linh hoạt theo tiến độ thắp đèn: $I = 0.15 + 0.55 \times (\text{đèn sáng} / \text{tổng đèn})$. Toàn bộ âm thanh được tổng hợp thời gian thực bằng Web Audio API độc lập không cần tải tài nguyên ngoài.

---

## 6. Minh chứng kiểm chứng (Proof of Verification)

* Đặc tả chi tiết tiêu chí nghiệm thu Phase 2: [docs/spec_phase2.md](docs/spec_phase2.md).
* Báo cáo kiểm thử tự động 24 test cases: [docs/proof/phase2_test_report.txt](docs/proof/phase2_test_report.txt).
* Mẫu log output headless Test Contract v1.1: [docs/proof/phase2_headless_proof.jsonl](docs/proof/phase2_headless_proof.jsonl).
* Tổng hợp giả định & số liệu chuẩn hóa: [docs/notes/assumptions.md](docs/notes/assumptions.md).
* Nhật ký SDLC & ước tính token/chi phí: [docs/notes/ai-log.md](docs/notes/ai-log.md).
* Phân tích hồi quy & Retrospective: [docs/notes/retro.md](docs/notes/retro.md).
