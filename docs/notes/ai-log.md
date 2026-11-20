# Nhật ký sử dụng AI (AI Usage Log)

Theo dõi việc sử dụng công cụ AI, quản lý ngữ cảnh, ước tính token và chi phí.

## CP0: Khởi tạo và thiết lập dự án
- **Model:** Gemini 3.8 Flash (Agentic assistant)
- **Hoạt động:**
  - Khởi tạo repo, quy ước cấu trúc thư mục chuẩn theo `SUBMISSION.md`.
  - Viết file quy chuẩn `AGENTS.md`, `CREDITS.md`, `LICENSE`, `requirements.txt`.
- **Ước tính token:** ~8.000 tokens.

## CP1: Phase 1 (PRD-0)
- **Model:** Gemini 3.8 Flash
- **Hoạt động:**
  - Đọc và bóc tách tài liệu gốc PDF 6 trang `Dao_Den_Long_Phase1_PRD0.pdf`.
  - Thiết kế kiến trúc Decoupled: Tách biệt hoàn toàn `src/core/` (Simulation engine 60 tick/s, không phụ thuộc UI) và `src/web/` (Giao diện 3D trực quan).
  - Khai báo file cấu hình bắt buộc `game.contract.json` theo Test Contract v1.0.
  - Viết bộ CLI Headless với định dạng chuẩn JSON Lines: Snapshot tick 0 và chu kỳ `--snapshot-every`, ghi nhận các sự kiện (`mote_picked`, `deposit`, `lantern_lit`, `pulse`, `player_hit`, `game_over`), và dòng kết thúc `end`.
  - Xây dựng bộ test toàn diện 15 test cases (schema, determinism, scenario injection, gameplay mechanics).
  - Xây dựng giao diện trực quan 3D WebGL (Three.js) với Web Audio API procedural sound.
- **Chiến lược tiết kiệm token:**
  - Batching các lệnh đọc và viết file song song để giảm số vòng trao đổi ngữ cảnh.
  - Sử dụng prompt tập trung vào tiêu chí kiểm chứng (verification criteria) thay vì yêu cầu chung chung.
- **Ước tính token:** ~35.000 tokens.
- **Ước tính chi phí:** ~$0.015 USD.
