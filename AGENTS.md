# AGENTS.md

## Lệnh dự án
- Cài đặt thư viện: `pip install -r requirements.txt`
- Chạy toàn bộ kiểm thử tự động: `pytest`
- Chạy headless (Test Contract v1.1): `python -m src.main --headless --night 1 --ticks 60 --out test.jsonl`
- Chạy game trực quan 3D: `python -m src.main`

## Quy ước kiến trúc
1. Tách biệt hoàn toàn Game Logic (`src/core/`) khỏi Presentation/Render (`src/web/`).
2. Logic cốt lõi chạy headless 60 tick/giây độc lập không phụ thuộc GPU hay cửa sổ đồ họa.
3. Đầu ra đảm bảo tính tất định (deterministic) 100% với cùng seed và chuỗi inputs.
4. Hiệu năng: Chạy một Đêm đầy đủ (21.600 ticks) phải hoàn thành trong $\le 30$ giây.

## Quy tắc bắt buộc
- Tuyệt đối không commit API key, token bí mật hoặc file `.env`.
- Không giả mạo kết quả test hay sửa tay file log bằng chứng.
- Mọi giả định kỹ thuật hoặc điểm thay thế luật phải ghi rõ ràng vào `docs/notes/assumptions.md`.
- Khi yêu cầu thay đổi (như các Ticket), test cũ bị ảnh hưởng phải được cập nhật kèm lý do cụ thể.
