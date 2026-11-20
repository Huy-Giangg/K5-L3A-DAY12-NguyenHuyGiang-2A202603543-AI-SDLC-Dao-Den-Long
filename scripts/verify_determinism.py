#!/usr/bin/env python3
"""
Harness Tool: Automated Determinism Verifier for Dao Den Long
Runs two identical headless simulations with the same seed and input sequence,
then verifies bit-for-bit equality across all ticks, events, and state snapshots.
"""
import sys
import hashlib
import subprocess
import os

def run_simulation(seed: int, ticks: int, out_file: str):
    cmd = [
        sys.executable, "-m", "src.main",
        "--headless",
        "--night", "1",
        "--seed", str(seed),
        "--ticks", str(ticks),
        "--out", out_file,
        "--snapshot-every", "5"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Simulation failed: {res.stderr}")

def get_file_hash(filepath: str) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def main():
    seed = 42
    ticks = 300
    file1 = "docs/proof/determinism_run1.jsonl"
    file2 = "docs/proof/determinism_run2.jsonl"
    os.makedirs("docs/proof", exist_ok=True)

    print(f"[*] Running Simulation 1 (seed={seed}, ticks={ticks})...")
    run_simulation(seed, ticks, file1)
    hash1 = get_file_hash(file1)

    print(f"[*] Running Simulation 2 (seed={seed}, ticks={ticks})...")
    run_simulation(seed, ticks, file2)
    hash2 = get_file_hash(file2)

    print(f"Run 1 SHA-256: {hash1}")
    print(f"Run 2 SHA-256: {hash2}")

    if hash1 == hash2:
        print("[SUCCESS] 100% Deterministic Verification PASSED! Both runs are identical bit-for-bit.")
        return 0
    else:
        print("[FAIL] Determinism mismatch detected!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
