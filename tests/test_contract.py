import json
import os
import subprocess
import sys
import pytest

def test_contract_json_schema():
    assert os.path.exists("game.contract.json")
    with open("game.contract.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["contract_version"] in ["1.0", "1.1"]
    assert "tuning" in data
    tuning = data["tuning"]
    assert tuning["lantern_count_night1"] == 5
    assert "player_speed" in tuning
    assert "carry_capacity" in tuning
    assert "lantern_cost" in tuning
    assert "safe_radius" in tuning
    assert "score" in tuning
    # v1.1 fields
    assert "dash_speed" in tuning
    assert "dash_duration_s" in tuning
    assert "dash_cooldown_s" in tuning

def test_headless_basic_run(tmp_path):
    out_file = str(tmp_path / "out.jsonl")
    cmd = [
        sys.executable, "-m", "src.main", "--headless",
        "--seed", "42",
        "--night", "1",
        "--ticks", "60",
        "--out", out_file,
        "--snapshot-every", "10"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0, f"Error: {res.stderr}"
    assert os.path.exists(out_file)

    lines = [json.loads(line) for line in open(out_file, encoding="utf-8")]
    assert len(lines) >= 7 # Tick 0, 10, 20, 30, 40, 50, 60 + End

    # First line must be snapshot at tick 0
    snap0 = lines[0]
    assert snap0["type"] == "snapshot"
    assert snap0["tick"] == 0
    assert snap0["state"] == "playing"
    assert snap0["player"]["pos"] == [0.0, 0.0, 0.0]
    assert len(snap0["lanterns"]) == 5

    # Last line must be end record
    end_rec = lines[-1]
    assert end_rec["type"] == "end"
    assert end_rec["ticks"] == 60
    assert end_rec["state"] == "playing"

def test_headless_determinism(tmp_path):
    out1 = str(tmp_path / "out1.jsonl")
    out2 = str(tmp_path / "out2.jsonl")
    cmd_base = [
        sys.executable, "-m", "src.main", "--headless",
        "--seed", "999",
        "--night", "1",
        "--ticks", "100",
        "--snapshot-every", "20"
    ]
    res1 = subprocess.run(cmd_base + ["--out", out1], capture_output=True, text=True)
    res2 = subprocess.run(cmd_base + ["--out", out2], capture_output=True, text=True)

    assert res1.returncode == 0
    assert res2.returncode == 0

    content1 = open(out1, "r", encoding="utf-8").read()
    content2 = open(out2, "r", encoding="utf-8").read()
    assert content1 == content2, "Runs with same seed must be 100% deterministic"

def test_invalid_input_exit_code(tmp_path):
    bad_scenario = str(tmp_path / "bad_scenario.json")
    with open(bad_scenario, "w", encoding="utf-8") as f:
        f.write("{ invalid json")
    
    out_file = str(tmp_path / "out.jsonl")
    cmd = [
        sys.executable, "-m", "src.main", "--headless",
        "--seed", "42",
        "--night", "1",
        "--scenario", bad_scenario,
        "--ticks", "10",
        "--out", out_file
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 2

def test_scenario_and_events(tmp_path):
    scenario = {
        "player": {"pos": [0, 0, 0], "carried": 0, "flames": 3},
        "random_motes": False,
        "random_shades": False,
        "motes": [[0, 0, 1.0]], # Player starts at [0,0,0], mote is at 1m -> within pickup radius (1.5)
        "shades": [{"id": "S1", "pos": [0, 0, 3.0]}],
        "lanterns": [{"id": "L1", "pos": [0, 0, 2.0], "deposited": 9, "lit": False}],
        "time_left_s": 300
    }
    inputs = {
        "frames": [
            {"tick": 0, "interact": False, "pulse": False},
            {"tick": 1, "interact": True}, # Picked up mote at tick 1, deposit at tick 2
            {"tick": 2, "interact": False, "pulse": True}
        ]
    }
    scen_path = str(tmp_path / "scen.json")
    inp_path = str(tmp_path / "inp.json")
    out_path = str(tmp_path / "out.jsonl")

    with open(scen_path, "w", encoding="utf-8") as f:
        json.dump(scenario, f)
    with open(inp_path, "w", encoding="utf-8") as f:
        json.dump(inputs, f)

    cmd = [
        sys.executable, "-m", "src.main", "--headless",
        "--seed", "123",
        "--night", "1",
        "--scenario", scen_path,
        "--inputs", inp_path,
        "--ticks", "10",
        "--out", out_path,
        "--snapshot-every", "5"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0

    lines = [json.loads(line) for line in open(out_path, encoding="utf-8")]
    event_names = [item["name"] for item in lines if item.get("type") == "event"]
    assert "mote_picked" in event_names
    assert "deposit" in event_names
    assert "lantern_lit" in event_names

