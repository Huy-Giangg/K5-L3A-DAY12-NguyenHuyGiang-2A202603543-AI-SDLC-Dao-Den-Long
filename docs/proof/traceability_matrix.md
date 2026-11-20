# Ma Trận Truy Vết Yêu Cầu & Bằng Chứng (Traceability Matrix)

Bảng ánh xạ toàn bộ các yêu cầu từ PRD-0 và các Ticket (Phase 1 đến Phase 4) đến kế hoạch kiểm chứng, tệp test tự động và tệp bằng chứng thực tế.

---

| Phase / Ticket | Yêu cầu cốt lõi | Phương pháp & Kế hoạch kiểm chứng | Tệp Test Tự Động | Tệp Bằng Chứng Thực Tế | Kết quả |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Phase 1 (PRD-0)** | Lõi mô phỏng headless 60Hz tách rời Web 3D; gom đom đóm; thắp 5 đèn lồng; quái vật truy đuổi; kỹ năng Tỏa Sáng | Chạy 15 test cases; chạy headless sinh JSONL; kiểm tra tính tất định | `tests/test_gameplay.py`<br>`tests/test_contract.py` | `docs/proof/phase1_headless_proof.jsonl`<br>`docs/proof/phase1_test_report.txt` | **100% ĐẠT** |
| **Phase 2 (Ticket-02)** | Chuẩn hóa bảng thông số Contract v1.1; mở rộng 3 Đêm (Đảo Bến, Đảo Cau, Đảo Chuông); kỹ năng Lướt, Nhảy, Bục Nhảy, Bùa Gió, Gió Lạc | Chạy 9 test scenarios mới cho các cơ chế vật lý và thực thể mới; chạy headless Đêm 2 & 3 | `tests/test_phase2_features.py` | `docs/proof/phase2_headless_proof.jsonl`<br>`docs/proof/phase2_test_report.txt` | **100% ĐẠT** |
| **Phase 3 (Ticket-03)** | Cơ chế đèn hao dầu ($1.0$/s), châm dầu, tắt đèn, thắp lại 5 đom đóm; Bóng Mực hút dầu (`drain`); luật thắng Bình Minh $\ge 60\%$ đèn sáng; túi mở rộng tối đa 20 | Kiểm thử tự động 7 kịch bản cạn dầu, chuyển trạng thái drain, kiểm tra tỷ lệ đèn bình minh, cập nhật test cũ theo ADR-001 | `tests/test_phase3_features.py` | `docs/proof/phase3_headless_proof.jsonl`<br>`docs/proof/phase3_test_report.txt`<br>`docs/adr/ADR-001-fuel-and-dawn-win.md` | **100% ĐẠT** |
| **Phase 4 (Ticket-04)** | Chế độ Benchmark `--benchmark` đạt $\ge 60$ FPS tải nặng (200 shades, 100 motes); Chế độ Soak Test `--soak` 10 đêm 0 crash, RAM $\le +20\%$ | Runner tự động thu thập FPS và bộ nhớ; kiểm thử schema contract v1.3; kiểm tra memory leak | `tests/test_phase4_features.py` | `bench.json`<br>`soak.json`<br>`docs/proof/phase4_headless_proof.jsonl` | **100% ĐẠT** |
| **Phase 4 (Ticket-04)** | Bảng xếp hạng Top 10 cục bộ, kiểm tra tên 3-12 ký tự, xuất JSON qua CLI `--export-leaderboard` | Test logic thêm, sắp xếp và cắt Top 10; test xuất file JSON từ dòng lệnh | `tests/test_phase4_features.py` | `leaderboard_export.json`<br>`data/leaderboard.json` | **100% ĐẠT** |
| **Phase 4 (Ticket-04)** | Tính năng Dễ tiếp cận (Accessibility): Key rebinding chống trùng phím, Reduced Motion, Large Text, Visual Subtitles | Tích hợp vào Web 3D; kiểm tra khả năng lưu trữ localStorage và hiển thị HUD | `src/web/index.html` | `docs/demo/demo.mp4`<br>`src/web/index.html` | **100% ĐẠT** |
| **All Phases** | Tính tất định (Determinism 100%) | Chạy 2 lần độc lập cùng seed và inputs; so sánh mã băm SHA-256 của toàn bộ chuỗi log | `scripts/verify_determinism.py` | `docs/proof/determinism_run1.jsonl`<br>`docs/proof/determinism_run2.jsonl` | **100% ĐẠT**<br>(SHA-256 khớp tuyệt đối) |
