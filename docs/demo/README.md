# Kịch Bản Quay Video Demo Chi Tiết (Shooting Script)
**Dự án:** Đảo Đèn Lồng (Lantern Island 3D) — Bản Phát Hành v1.0.0  
**Sinh viên:** Nguyễn Huy Giang — **MSSV:** 2A202603543 — **Lớp:** K5-L3A  
**Thời lượng dự kiến:** 3 phút 45 giây (Quy định: Dưới 5 phút)  
**Định dạng xuất:** `docs/demo/demo.mp4` (1080p, H.264, âm thanh AAC)  

---

## 0. Chuẩn Bị Trước Khi Bấm Quay (Pre-recording Setup)
1. **Phần mềm quay màn hình:** OBS Studio, Windows Game Bar (`Win + G`), hoặc QuickTime.
2. **Cửa sổ chuẩn bị sẵn:**
   - Cửa sổ 1: **Terminal / VS Code** (đã mở thư mục gốc của dự án).
   - Cửa sổ 2: **Trình duyệt Web** (Google Chrome hoặc Edge mở sẵn ở tab mới).
3. **Kiểm tra môi trường:** Chạy sẵn `pip install -r requirements.txt` để không phải chờ tải thư viện trong lúc quay.

---

## KỊCH BẢN CHI TIẾT THEO TỪNG PHÂN ĐOẠN

### Phân đoạn 1: Giới thiệu & Bằng chứng Kiểm thử Tự động (00:00 — 00:45)
- **Màn hình hiển thị:** Cửa sổ Terminal và cấu trúc thư mục repo trong VS Code.
- **Thao tác thực hiện:**
  1. Show nhanh file `AGENTS.md`, `game.contract.json` (v1.3), `RUBRIC.md`.
  2. Gõ lệnh chạy kiểm thử tự động:
     ```bash
     pytest
     ```
  3. Gõ lệnh kiểm tra tính tất định:
     ```bash
     python scripts/verify_determinism.py
     ```
- **Lời bình (Voiceover Script):**
  > *"Xin chào thầy cô và các bạn, em là Nguyễn Huy Giang, sinh viên lớp K5-L3A, MSSV 2A202603543. Hôm nay em xin trình bày video nghiệm thu sản phẩm Đảo Đèn Lồng phiên bản phát hành v1.0.0 sau 4 Phase AI SDLC.*  
  > *Dự án được xây dựng với kiến trúc tách biệt tuyệt đối: Lõi mô phỏng headless chạy toán học thuần túy, không phụ thuộc GPU và tuân thủ Test Contract v1.3.*  
  > *Đầu tiên, em chạy lệnh `pytest`. Toàn bộ 36 bài kiểm thử bao phủ từ Phase 1 đến Phase 4 đều vượt qua 100% trong chưa đầy 7 giây.*  
  > *Tiếp theo, em chạy script kiểm chứng tính tất định `verify_determinism.py`. Hai lượt chạy độc lập với cùng seed cho ra mã băm SHA-256 trùng khớp từng bit, chứng minh hệ thống đạt 100% tất định."*

---

### Phân đoạn 2: Trải Nghiệm Trực Quan Gameplay 3 Đêm (00:45 — 01:50)
- **Màn hình hiển thị:** Chuyển sang trình duyệt Web chơi game 3D.
- **Thao tác thực hiện:**
  1. Trong terminal gõ: `python -m src.main` (trình duyệt tự động mở `http://localhost:8080`).
  2. **Đêm 1 (Đảo Bến):** 
     - Bấm "Bắt đầu Đêm".
     - Dùng `W, A, S, D` gom các đốm sáng đom đóm, thanh túi đom đóm đầy 10 slot.
     - Tiếp cận Đèn Lồng Lớn, bấm `E` nạp ánh sáng. Thắp sáng đèn, âm thanh Web Audio phát lên.
     - Quái vật Bóng Mực đuổi theo, bấm `Q` kích hoạt **Tỏa Sáng (Pulse)** đẩy lùi và làm choáng quái vật.
  3. **Đêm 2 (Đảo Cau) & Đêm 3 (Đảo Chuông):**
     - Thể hiện kỹ năng **Lướt (Shift)** với tốc độ 14m/s, nhảy vượt qua cầu tre.
     - Bước vào **Bục Nhảy (Jump Pad)** bay vút qua biển mây.
     - Nhặt **Bùa Gió (Wind Charm)** nhận hiệu ứng lướt không hồi chiêu.
- **Lời bình (Voiceover Script):**
  > *"Bây giờ em khởi chạy game 3D trực quan bằng lệnh `python -m src.main`. Toàn bộ đồ họa Three.js và âm thanh tổng hợp bằng Web Audio API chạy mượt mà ngay trên trình duyệt mà không cần tải bất kỳ asset ngoài nào.*  
  > *Tại Đêm 1 trên Đảo Bến, nhân vật Mây thu thập đom đóm trong đêm sương. Khi đủ đom đóm, Mây nạp ánh sáng vào Đèn Lồng Lớn. Khi bị Bóng Mực áp sát, Mây sử dụng kỹ năng Tỏa Sáng tiêu hao 3 đom đóm để làm choáng diện rộng.*  
  > *Bước sang Đêm 2 tại Đảo Cau và Đêm 3 tại Đảo Chuông, không gian mở rộng với cầu tre hiểm trở, bục nhảy vượt mây và Bùa Gió tăng tốc lướt liên tục."*

---

### Phân đoạn 3: Cơ Chế Cạn Dầu & Luật Thắng Bình Minh (01:50 — 02:40)
- **Màn hình hiển thị:** Trực tiếp tương tác với cơ chế đèn cạn dầu và quái hút dầu.
- **Thao tác thực hiện:**
  1. Chỉ vào một đèn lồng đang sáng, chỉ số dầu giảm dần ($1.0$/s).
  2. Khi dầu còn dưới 30, đèn lồng bắt đầu chớp nháy cảnh báo 1Hz.
  3. Bóng Mực lao vào đèn lồng yếu và chuyển sang trạng thái `drain` hút dầu.
  4. Mây chạy tới bấm `Q` tỏa sáng cứu đèn, bấm `E` châm thêm dầu hồi sinh ngọn đèn.
  5. Đồng hồ đếm ngược về Bình minh: số đèn sáng $\ge 60\%$, hiển thị màn hình chiến thắng Bình Minh rực rỡ.
- **Lời bình (Voiceover Script):**
  > *"Ở Phase 3, dự án tiếp nhận Change Request quan trọng: Đèn Lồng không còn sáng vĩnh viễn mà tiêu hao dầu theo thời gian. Khi mức dầu dưới 30, đèn mất vùng an toàn và bắt đầu nhấp nháy cảnh báo.*  
  > *Bóng Mực sẽ lập tức áp sát và hút 5 đơn vị dầu mỗi giây. Mây phải nhanh chóng tỏa sáng giải cứu và bấm E để châm dầu.*  
  > *Luật thắng cũ all_lit đã được bãi bỏ và chuyển sang luật thắng Bình Minh dawn_survived: người chơi phải bảo vệ ít nhất 60% ngọn đèn sống sót đến khi trời sáng, kèm kiến trúc tài liệu ADR-001 chuẩn mực."*

---

### Phân đoạn 4: Đo Hiệu Năng Phi Chức Năng (Benchmark & Soak Test) (02:40 — 03:15)
- **Màn hình hiển thị:** Quay lại Terminal để chạy 2 lệnh non-functional theo Test Contract v1.3.
- **Thao tác thực hiện:**
  1. Chạy lệnh Benchmark:
     ```bash
     python -m src.main --benchmark --seed 42 --duration 10 --out bench.json
     ```
     Mở nhanh tệp `bench.json`: chỉ vào `avg_fps: 183.8`, `p1_low_fps: 152.0`, `load_ms: 0`.
  2. Chạy lệnh Soak Test:
     ```bash
     python -m src.main --soak --seed 7 --nights 3 --out soak.json
     ```
     Mở nhanh tệp `soak.json`: chỉ vào `crashes: 0`, RAM ban đầu 24MB $\to$ kết thúc 25MB.
- **Lời bình (Voiceover Script):**
  > *"Bước sang Phase 4, em kiểm tra các chỉ số phi chức năng theo Test Contract v1.3.*  
  > *Lệnh benchmark tải nặng với 200 quái vật và 100 đom đóm đạt tốc độ trung bình 183.8 FPS, 1% Low đạt 152 FPS, vượt xa ngưỡng yêu cầu 60 FPS.*  
  > *Lệnh soak test mô phỏng liên tục xoay vòng các đêm đạt 0 crash tuyệt đối; lượng RAM chỉ tăng nhẹ 1MB từ 24 lên 25MB, khẳng định hoàn toàn không xảy ra hiện tượng rò rỉ bộ nhớ."*

---

### Phân đoạn 5: Trợ Năng, Bảng Xếp Hạng & Lịch Sử Git (03:15 — 03:45)
- **Màn hình hiển thị:** Màn hình Web UI (menu Trợ năng & Bảng xếp hạng), sau đó chuyển sang Git log.
- **Thao tác thực hiện:**
  1. Mở menu `♿ Dễ Tiếp Cận`:
     - Thử đổi phím, bấm phím trùng để hiện cảnh báo đỏ *"Phím đã được dùng cho hành động khác!"*.
     - Bật chế độ "Giảm chuyển động", "Cỡ chữ lớn x1.25", và "Phụ đề trực quan".
  2. Mở menu `🏆 Bảng Xếp Hạng Top 10`.
  3. Mở terminal gõ:
     ```bash
     git tag -l
     git log --oneline -n 6
     ```
- **Lời bình (Voiceover Script):**
  > *"Về khía cạnh tiếp cận người dùng, game hỗ trợ tùy biến phím bấm linh hoạt với thuật toán chống trùng phím theo thời gian thực, chế độ giảm rung lắc camera, phóng to cỡ chữ UI và phụ đề thị giác.*  
  > *Bảng xếp hạng Top 10 lưu trữ cục bộ và hỗ trợ xuất báo cáo qua CLI.*  
  > *Cuối cùng, lịch sử git thể hiện quy trình phát triển kỷ luật với đầy đủ 4 tag: phase-1, phase-2, phase-3, phase-4 và Release v1.0.0 đã được đồng bộ lên remote GitHub.*  
  > *Em xin cảm ơn thầy cô và các bạn đã theo dõi!"*
