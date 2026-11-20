"""
Phase 4 Non-functional & Release Tests (Ticket-04 / Contract v1.3)
Verifies:
  - Contract v1.3 schema requirements (contract_version, bench_cmd, soak_cmd)
  - Leaderboard logic (Top 10 sort, name validation, export)
  - Benchmark runner schema & performance metrics
  - Soak test runner schema & memory stability (no leaks, no crashes)
"""
import os
import json
import pytest
from src.core.leaderboard import add_leaderboard_entry, get_leaderboard, export_leaderboard, is_valid_name
from src.core.bench import run_benchmark
from src.core.soak import run_soak_test

def test_contract_v1_3_schema():
    with open("game.contract.json", "r", encoding="utf-8") as f:
        contract = json.load(f)
    assert contract.get("contract_version") == "1.3", "Contract version must be 1.3"
    assert "bench_cmd" in contract, "Contract v1.3 must define bench_cmd"
    assert "soak_cmd" in contract, "Contract v1.3 must define soak_cmd"
    assert "python -m src.main --benchmark" in contract["bench_cmd"]
    assert "python -m src.main --soak" in contract["soak_cmd"]

def test_leaderboard_name_validation():
    assert is_valid_name("Player1") is True
    assert is_valid_name("Đèn Lồng") is True
    assert is_valid_name("Ab") is False          # Too short (< 3)
    assert is_valid_name("A"*13) is False        # Too long (> 12)
    assert is_valid_name("Bad@Character!") is False # Invalid symbol

def test_leaderboard_top_10_and_export(tmp_path):
    # Test add entry
    add_leaderboard_entry("Tester", 1250, 3, 42)
    add_leaderboard_entry("Giang", 2100, 3, 100)
    
    export_path = str(tmp_path / "test_lb_export.json")
    export_leaderboard(export_path)
    assert os.path.exists(export_path)
    with open(export_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert "entries" in data
        assert isinstance(data["entries"], list)
        assert len(data["entries"]) <= 10
        if len(data["entries"]) >= 2:
            assert data["entries"][0]["score"] >= data["entries"][1]["score"]

def test_benchmark_runner_schema_and_threshold(tmp_path):
    out_file = str(tmp_path / "bench_test.json")
    exit_code = run_benchmark(["--seed", "42", "--duration", "2", "--out", out_file])
    assert exit_code == 0
    assert os.path.exists(out_file)

    with open(out_file, "r", encoding="utf-8") as f:
        bench_data = json.load(f)

    # Required schema checks from Ticket-04
    assert bench_data.get("contract_version") == "1.3"
    assert "avg_fps" in bench_data
    assert "p1_low_fps" in bench_data
    assert "frame_ms_p95" in bench_data
    assert "frames" in bench_data
    assert "peak_mem_mb" in bench_data
    assert "load_ms" in bench_data

    # Performance thresholds (Ticket-04: avg >= 60, p1 >= 30, load_ms <= 10000)
    assert bench_data["avg_fps"] >= 60.0
    assert bench_data["p1_low_fps"] >= 30.0
    assert bench_data["load_ms"] <= 10000

def test_soak_runner_schema_and_leak(tmp_path):
    out_file = str(tmp_path / "soak_test.json")
    # Quick soak test over 2 nights
    exit_code = run_soak_test(["--seed", "7", "--nights", "2", "--out", out_file])
    assert exit_code == 0
    assert os.path.exists(out_file)

    with open(out_file, "r", encoding="utf-8") as f:
        soak_data = json.load(f)

    # Required schema checks
    assert soak_data["nights"] == 2
    assert soak_data["crashes"] == 0
    assert "results" in soak_data
    assert len(soak_data["results"]) == 2
    assert "mem_start_mb" in soak_data
    assert "mem_end_mb" in soak_data
    # No major leak check: mem_end <= 1.2 * mem_start
    assert soak_data["mem_end_mb"] <= max(soak_data["mem_start_mb"] * 1.2, soak_data["mem_start_mb"] + 10)
