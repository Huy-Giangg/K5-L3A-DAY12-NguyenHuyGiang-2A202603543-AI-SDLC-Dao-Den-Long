"""
Main Entry Point for Dao Den Long (Phase 4 - Release v1.0.0)
Supports:
  - Interactive 3D Visual Game (Three.js Web UI)
  - Headless Verification Mode (Contract v1.3: python -m src.main --headless)
  - Benchmark Mode (Contract v1.3: python -m src.main --benchmark)
  - Soak Test Runner (Contract v1.3: python -m src.main --soak)
  - Leaderboard Export (python -m src.main --export-leaderboard <path>)
"""
import sys
import os
import http.server
import socketserver
import webbrowser

def start_visual_game(port=8080):
    web_dir = os.path.join(os.path.dirname(__file__), "web")
    os.chdir(web_dir)
    
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass # Suppress HTTP access logging in terminal
            
    try:
        with socketserver.TCPServer(("", port), QuietHandler) as httpd:
            url = f"http://localhost:{port}"
            print(f"==================================================")
            print(f"  ĐẢO ĐÈN LỒNG - 3D GAME (v1.0.0 RELEASE)")
            print(f"  Đường dẫn: {url}")
            print(f"  (Nhấn Ctrl+C để dừng game)")
            print(f"==================================================")
            webbrowser.open(url)
            httpd.serve_forever()
    except OSError:
        # Fallback to port 8081 if 8080 is in use
        with socketserver.TCPServer(("", port + 1), QuietHandler) as httpd:
            url = f"http://localhost:{port + 1}"
            print(f"Đang mở tại: {url}")
            webbrowser.open(url)
            httpd.serve_forever()

def main():
    if "--headless" in sys.argv:
        from src.core.runner import run_headless
        args = [arg for arg in sys.argv[1:] if arg != "--headless"]
        sys.exit(run_headless(args))
    elif "--benchmark" in sys.argv:
        from src.core.bench import run_benchmark
        args = [arg for arg in sys.argv[1:] if arg != "--benchmark"]
        sys.exit(run_benchmark(args))
    elif "--soak" in sys.argv:
        from src.core.soak import run_soak_test
        args = [arg for arg in sys.argv[1:] if arg != "--soak"]
        sys.exit(run_soak_test(args))
    elif "--export-leaderboard" in sys.argv:
        from src.core.leaderboard import export_leaderboard
        idx = sys.argv.index("--export-leaderboard")
        out_path = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else "leaderboard.json"
        export_leaderboard(out_path)
        print(f"Leaderboard exported successfully to {out_path}")
        sys.exit(0)
    else:
        try:
            start_visual_game()
        except KeyboardInterrupt:
            print("\nĐã đóng game.")
            sys.exit(0)

if __name__ == "__main__":
    main()
