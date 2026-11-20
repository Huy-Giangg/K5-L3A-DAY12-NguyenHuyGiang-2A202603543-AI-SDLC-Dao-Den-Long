import subprocess
import sys

def test_environment_ready():
    assert sys.version_info >= (3, 8)

def test_headless_execution():
    result = subprocess.run([sys.executable, "-m", "src.main", "--headless"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "STATUS: OK" in result.stdout
