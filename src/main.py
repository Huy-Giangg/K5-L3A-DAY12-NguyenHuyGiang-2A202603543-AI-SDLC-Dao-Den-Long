"""
Main Entry Point for Dao Den Long (Phase 1)
Supports both Headless Verification Mode (Test Contract v1.0) and Interactive 3D Visual Game.
"""
import sys
import os
import http.server
import socketserver
import webbrowser
from threading import Thread

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
            print(f"  ĐẢO ĐÈN LỒNG - 3D GAME ĐANG CHẠY")
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
    else:
        try:
            start_visual_game()
        except KeyboardInterrupt:
            print("\nĐã đóng game.")
            sys.exit(0)

if __name__ == "__main__":
    main()
