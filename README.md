# Đảo Đèn Lồng (Lantern Island 3D) — Bản Phát Hành v1.0.0

> **Dự án AI SDLC · Day 12**  
> **Sinh viên:** Nguyễn Huy Giang — **MSSV:** 2A202603543 — **Lớp:** L3A  
> **Phiên bản:** v1.0.0 (Release)  
> **Video Demo:** [Xem video demo tại đây](docs/demo/demo.mp4)  
> **Báo cáo tổng kết SDLC:** [Báo cáo Retrospective 4 Phase](docs/notes/retro.md) | [Nhật ký Token & Chi phí AI](docs/notes/ai-log.md) | [Nhật ký Thay đổi CHANGELOG](CHANGELOG.md)

---

## 1. Cài đặt và Khởi chạy (Tối đa 3 lệnh)

Dự án được xây dựng trên nền **Python 3.11+**, chạy đồng nhất trên Windows, macOS và Linux.

```bash
# 1. Cài đặt thư viện
pip install -r requirements.txt

# 2. Chạy toàn bộ kiểm thử tự động (36 test cases toàn diện)
pytest

# 3. Mở game trực quan 3D trên trình duyệt
python -m src.main
```

---

## 2. Các Lệnh Phi Chức Năng & Đánh Giá Chất Lượng (Contract v1.3)

### 2.1. Chế độ Benchmark (Kiểm thử tải nặng)
Đo hiệu năng hệ thống khi có 200 Bóng Mực, 100 Đom đóm và camera quay quỹ đạo:
```bash
python -m src.main --benchmark --seed 42 --duration 30 --out bench.json
```
- **Kết quả thực tế:** `avg_fps = 183.8` (ngưỡng $\ge 60$), `p1_low_fps = 152.0` (ngưỡng $\ge 30$), `load_ms = 0` (ngưỡng $\le 10000$).

### 2.2. Chế độ Soak Test (Kiểm thử độ bền & Rò rỉ RAM)
Mô phỏng 10 đêm liên tục xoay vòng nhằm phát hiện crash và memory leak:
```bash
python -m src.main --soak --seed 7 --nights 10 --out soak.json
```
- **Kết quả thực tế:** `crashes = 0`, `mem_start = 24MB`, `mem_end = 25MB` ($+4.1\%$, ngưỡng cho phép $\le +20\%$), chứng minh **0% rò rỉ bộ nhớ**.

### 2.3. Xuất Báo Cáo Bảng Xếp Hạng Top 10 (Leaderboard)
Xuất danh sách Top 10 kỷ lục người chơi đạt điểm cao nhất ra tệp JSON:
```bash
python -m src.main --export-leaderboard data/leaderboard_export.json
```

---

## 3. Chế độ Headless (Test Contract v1.3)

Chạy mô phỏng logic cốt lõi siêu tốc độc lập hoàn toàn với GPU và cửa sổ hiển thị:

```bash
python -m src.main --headless --seed 42 --night 1 --ticks 120 --out docs/proof/phase4_headless_proof.jsonl --snapshot-every 10
```

### Các tùy chọn tham số:
* `--seed <int>`: Khởi tạo RNG seed đảm bảo tính tất định (deterministic) 100%.
* `--night <1|2|3>`: Lựa chọn màn chơi:
  * **Đêm 1 (Đảo Bến):** 240s, 5 Đèn Lồng. Cần giữ sáng $\ge 3/5$ đèn đến bình minh để thắng.
  * **Đêm 2 (Đảo Cau):** 270s, 6 Đèn Lồng, 2 bục nhảy, Bùa Gió C1. Cần giữ sáng $\ge 4/6$ đèn.
  * **Đêm 3 (Đảo Chuông):** 300s, 7 Đèn Lồng, đảo 3 tầng, bục nhảy, 2 Bùa Gió C1 & C2, gió bão giật mỗi 30s. Cần giữ sáng $\ge 5/7$ đèn.
* `--scenario <path.json>`: Nạp trạng thái ban đầu của đèn, người chơi và quái vật.
* `--inputs <path.json>`: Nạp chuỗi thao tác phím theo tick (`move`, `jump`, `dash`, `interact`, `pulse`, `pause`).
* `--ticks <int>`: Số tick mô phỏng (tốc độ 60 tick/giây). Một Đêm đầy đủ (21.600 ticks) hoàn thành chỉ trong **~2.1 giây**.
* `--out <path.jsonl>`: File lưu snapshot và sự kiện định dạng JSON Lines v1.3.

---

## 4. Cách Chơi, Điều Khiển & Tính Năng Dễ Tiếp Cận

### 4.1. Điều Khiển Mặc Định
| Thao tác | Phím mặc định | Mô tả |
| :--- | :---: | :--- |
| **Di chuyển** | `W`, `A`, `S`, `D` | Điều khiển Mây chạy trên đảo (có hỗ trợ phím mũi tên) |
| **Nhảy cao** | `Space` | Nhảy lên gờ đá, cầu tre hoặc bục nhảy |
| **Lướt nhanh (Dash)** | `Shift` hoặc `J` | Lướt tốc độ cao $14$ m/s trong $0.2$s (hồi chiêu $1.5$s) |
| **Nạp đom đóm / Châm dầu** | `E` | Nạp $10$ con thắp mới, $5$ con thắp lại, hoặc châm thêm dầu ($10$ fuel/con) |
| **Tỏa Sáng (Pulse)** | `Q` hoặc `F` | Tiêu hao 3 đom đóm, đẩy lùi và làm choáng quái vật trong $5.0$m |
| **Xoay Camera** | `Giữ chuột trái & kéo` | Xoay góc nhìn toàn cảnh đảo |
| **Tạm dừng** | `Esc` hoặc `P` | Mở menu tạm dừng, bảng xếp hạng và cài đặt |

### 4.2. Tính Năng Dễ Tiếp Cận (Accessibility)
Người chơi có thể kích hoạt trong menu `♿ Dễ Tiếp Cận`:
- **Tùy biến phím (Key Rebinding):** Gán lại phím cho từng hành động. Tự động cảnh báo và ngăn chặn trùng phím. Nút khôi phục phím gốc.
- **Giảm chuyển động (Reduced Motion):** Giảm gia tốc quay camera, tắt rung lắc sương mù dành cho người nhạy cảm thị giác.
- **Cỡ chữ lớn (Large Text UI):** Phóng to tỷ lệ giao diện x1.25 giúp đọc rõ chữ trên màn hình lớn.
- **Chỉ báo hình ảnh / Phụ đề (Visual Subtitles):** Cảnh báo chữ nổi và viền màu khi Bóng Mực áp sát hoặc khi Đèn Lồng sắp cạn dầu.
- **Chế độ mù màu:** Tăng tương phản viền sáng và hình khối đèn lồng để phân biệt rõ ràng.

---

## 5. Quy Ước Kiến Trúc & Kỷ Luật Kỹ Nghệ

1. **Decoupled Architecture:** Logic cốt lõi độc lập tại `src/core/`, không import bất kỳ thư viện đồ họa nào.
2. **Deterministic 100%:** Cùng `seed` và chuỗi `inputs` luôn cho ra kết quả từng bit giống nhau. Có thể tự kiểm chứng bằng script:
   ```bash
   python scripts/verify_determinism.py
   ```
3. **Hiệu năng cao:** Mô phỏng 21.600 ticks trong $\le 2.5$ giây, FPS đồ họa $>180$ FPS.
4. **Bảo mật & Kỷ luật:** Tuyệt đối không commit token hay `.env`; ghi nhận đầy đủ lý do thay đổi kiểm thử vào CHANGELOG và ADR.
5. **Ma trận truy vết:** Xem đầy đủ ánh xạ từ yêu cầu đến bằng chứng tại [Ma Trận Truy Vết](docs/proof/traceability_matrix.md).

---

## 6. Sáng Tạo Của Tôi (My Innovation)

Nhằm tối ưu trải nghiệm người dùng mà **tuyệt đối không phá vỡ Test Contract** hay làm thay đổi đầu ra mô phỏng headless, dự án tích hợp 3 sáng tạo kỹ thuật độc đáo:

1. **Hệ Thống Âm Thanh Thủ Tục Thuần (Zero-Asset Procedural Audio):**
   - Thay vì tải các tệp âm thanh `.mp3` / `.wav` cồng kềnh, game áp dụng Web Audio API để tổng hợp trực tiếp tần số âm thanh từ mã JavaScript (sóng sin cho tiếng đom đóm, triangle cho tiếng nhảy bục, tam âm cho lúc thắp đèn lồng lớn).
   - *Lợi ích:* Kích thước tải trang **0 KB**, độ trễ phát âm **0 ms**, độc lập 100% không lo lỗi 404 tài nguyên mạng.

2. **Cơ Chế Trợ Năng Đa Tầng Ngăn Ngừa Xung Đột Phím (Key Conflict Prevention Engine):**
   - Bảng tùy biến phím bấm (Key Rebinding) được tích hợp thuật toán kiểm tra xung đột thời gian thực: khi gán một phím đã được dùng cho hành động khác, hệ thống cảnh báo đỏ và ngăn chặn ghi đè để bảo vệ người chơi không bị kẹt điều khiển.
   - Kết hợp chỉ báo thị giác (Visual Subtitles) phát tín hiệu chữ nổi khi Bóng Mực áp sát hoặc khi Đèn sắp cạn dầu, hỗ trợ tối đa cho game thủ khiếm thính hoặc chơi trong môi trường yên tĩnh.

3. **Chế Độ Mù Màu Trợ Năng (Colorblind Mode):**
   - Bổ sung tùy chọn chuyển đổi màu sắc có độ tương phản cao, tăng cường viền sáng phát quang cho Đèn Lồng và Bóng Mực giúp người chơi có thị giác màu kém dễ dàng phân biệt trạng thái trong đêm tối.

