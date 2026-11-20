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

# 2. Chạy kiểm thử tự động (15 test cases)
pytest

# 3. Mở game 3D trực quan
python -m src.main
```

---

## 2. Chế độ Headless (Test Contract v1.0)

Để phục vụ việc chấm tự động theo Test Contract v1.0:

```bash
python -m src.main --headless --seed 42 --night 1 --ticks 120 --out docs/proof/phase1_headless_proof.jsonl --snapshot-every 10
```

### Các tùy chọn tham số:
* `--seed <int>`: Khởi tạo bộ sinh số ngẫu nhiên (RNG seed) đảm bảo tính tất định.
* `--night 1`: Màn chơi Đêm 1 (Đảo Bến).
* `--scenario <path.json>`: Nạp tình huống kịch bản ban đầu.
* `--inputs <path.json>`: Nạp chuỗi thao tác phím theo tick.
* `--ticks <int>`: Số tick mô phỏng (tốc độ 60 tick/giây).
* `--out <path.jsonl>`: File lưu kết quả snapshot và event định dạng JSON Lines.
* `--snapshot-every <int>`: Chu kỳ ghi snapshot (mặc định 10 tick).

---

## 3. Cách chơi & Điều khiển

| Phím | Hành động | Mô tả |
|---|---|---|
| **W, A, S, D** | Di chuyển | Mây chạy khắp Đảo Bến thu thập đom đóm (tối đa mang 10 con). |
| **E** | Nạp đom đóm | Đến gần Đèn Lồng Lớn (trong bán kính 2.5m) để thắp sáng (cần 5 con/đèn). |
| **Q / F** | Tỏa sáng (Pulse) | Tiêu tốn 1 đom đóm, phát sóng ánh sáng làm choáng và đẩy lùi Bóng Mực trong bán kính 6m. |
| **Chuột (kéo)**| Xoay góc nhìn | Điều chỉnh camera 3D bao quát hòn đảo. |

---

## 4. Cách tính điểm (Scoring)

* **Nhặt đom đóm:** `+10` điểm / con.
* **Thắp sáng Đèn Lồng Lớn:** `+200` điểm / đèn.
* **Làm choáng Bóng Mực:** `+25` điểm / lần trúng.
* **Thưởng khi Chiến thắng (`all_lit`):**
  * `+5` điểm / giây còn lại trước khi trời sáng.
  * `+100` điểm / ngọn lửa sinh lực còn giữ được.

---

## 5. Sáng tạo của tôi (Creative Highlights)

* **Đồ họa WebGL 3D chân thực & nhẹ nhàng:** Sử dụng Three.js dựng toàn bộ hòn đảo giữa biển mây, nhân vật Mây đội nón lá gắn đèn lồng nhỏ, hiệu ứng đổ bóng và ánh sáng vàng cam ấm áp.
* **Âm thanh tổng hợp (Procedural Audio):** Sử dụng Web Audio API tích hợp sẵn để tạo hiệu ứng âm thanh sống động (nhặt đom đóm, thắp đèn, tiếng nổ tỏa sáng, âm thanh khi bị bóng mực va chạm) mà không phụ thuộc vào file asset âm thanh bên ngoài.
* **Hoàn toàn độc lập:** Chế độ headless thuần túy tách rời khỏi đồ họa, không làm thay đổi hay ảnh hưởng đến bất kỳ kết quả output nào của Test Contract v1.0.

---

## 6. Minh chứng kiểm chứng (Proof of Verification)

* Kết quả test tự động được lưu tại: [docs/proof/phase1_test_report.txt](docs/proof/phase1_test_report.txt).
* Mẫu log output headless đạt chuẩn tại: [docs/proof/phase1_headless_proof.jsonl](docs/proof/phase1_headless_proof.jsonl).
* Chi tiết các giả định tại: [docs/notes/assumptions.md](docs/notes/assumptions.md).
